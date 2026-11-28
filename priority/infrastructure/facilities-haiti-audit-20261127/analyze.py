"""Reproducible facility coverage/duplicate diagnostics, not institution reconciliation."""
import collections
import hashlib
import io
import json
import sys
import unicodedata
import zipfile
from pathlib import Path
import shapefile
from shapely import normalize, STRtree
from shapely.geometry import shape
from shapely.ops import unary_union, transform
from pyproj import Transformer

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE/'config.json').read_text())

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def name_key(value):
    text = ''.join(c for c in unicodedata.normalize('NFKD',str(value or '')) if not unicodedata.combining(c)).casefold()
    return ' '.join(''.join(c if c.isalnum() else ' ' for c in text).split())
def theme(cls): return 'school' if cls in CONFIG['school_classes'] else 'health'
def groups(records, key):
    found = collections.defaultdict(list)
    for r in records:
        value = key(r)
        if value not in ('',None): found[value].append(r['key'])
    return [v for v in found.values() if len(v)>1]


def main():
    facility, national, scratch, boundary_path, output = map(Path,sys.argv[1:])
    boundary = unary_union([shape(f['geometry']) for f in json.loads(boundary_path.read_text())['features']])
    departments_json = json.loads((scratch/'departments.geojson').read_text())
    assert departments_json['totalFeatures'] == len(departments_json['features']) == 10
    departments = [(f['properties']['nom2_dep'],shape(f['geometry'])) for f in departments_json['features']]
    assert boundary.is_valid and all(g.is_valid and not g.is_empty for _,g in departments)
    assert len({n for n,_ in departments}) == 10
    national_boundary = unary_union([g for _,g in departments])
    all_records = []
    input_paths = [boundary_path, scratch/'departments.geojson', HERE/'config.json']
    def add(source, index, identity, cls, name, geom, extra=None):
        r = {'key':f'{source}:{index}', 'source':source,'source_id':str(identity) if identity is not None else '',
             'class':cls,'name':str(name or ''),'name_key':name_key(name),'geometry':geom, 'extra':extra or {}}
        if geom is None or geom.is_empty: r['state']='missing_geometry'
        elif not geom.is_valid: r['state']='invalid_geometry'
        elif geom.geom_type not in ('Point','Polygon','MultiPolygon'): r['state']='unsupported_geometry'
        elif geom.geom_type=='Point': r['state']='in_haiti' if boundary.covers(geom) else 'outside_pinned_boundary'
        else: r['state']='in_haiti' if geom.intersection(boundary).area>0 else 'outside_pinned_boundary'
        if geom is not None and not geom.is_empty and geom.is_valid:
            r['national_boundary_intersects'] = national_boundary.covers(geom) if geom.geom_type=='Point' else geom.intersection(national_boundary).area>0
            if r['national_boundary_intersects']:
                anchor = geom if geom.geom_type=='Point' else geom.intersection(national_boundary).representative_point()
                matches = [n for n,g in departments if g.covers(anchor)]
                r['national_department'] = matches[0] if len(matches)==1 else 'AMBIGUOUS' if matches else 'UNMATCHED'
        if r['state']=='in_haiti':
            anchor = geom if geom.geom_type=='Point' else geom.intersection(boundary).representative_point()
            matches = [n for n,g in departments if g.covers(anchor)]
            r['department'] = matches[0] if len(matches)==1 else 'AMBIGUOUS' if matches else 'UNMATCHED'
        all_records.append(r)
    for label,stem in [('osm_point','gis_osm_pois_free_1'),('osm_polygon','gis_osm_pois_a_free_1')]:
        input_paths += sorted(facility.glob(stem+'.*'))
        for i,row in enumerate(shapefile.Reader(str(facility/stem),encoding='utf-8').iterShapeRecords(),1):
            d=row.record.as_dict()
            if d['fclass'] in CONFIG['osm_classes']:
                add(label,i,d['osm_id'],d['fclass'],d['name'],shape(row.shape.__geo_interface__) if row.shape.points else None)
    paho_path=facility/'paho_haiti_health_sites.zip';input_paths.append(paho_path)
    with zipfile.ZipFile(paho_path) as z:
        shp=next(n for n in z.namelist() if n.endswith('.shp'));stem=shp[:-4]
        reader=shapefile.Reader(shp=io.BytesIO(z.read(shp)),dbf=io.BytesIO(z.read(stem+'.dbf')),encoding='latin-1')
        for i,row in enumerate(reader.iterShapeRecords(),1):
            d=row.record.as_dict()
            add('paho',i,d['Institut_2'],'health_unspecified',d['Institutio'],shape(row.shape.__geo_interface__) if row.shape.points else None,{'native_department':d['adm1_fr']})
    for code,name_field,id_field in [('29','NOM_DE_L_ECOLE','CODE_ECOLE'),('83','Name','fid')]:
        path=national/f'school_{code}.geojson';input_paths.append(path)
        for i,f in enumerate(json.loads(path.read_text())['features'],1):
            d=f['properties'];add('cnigs_school_'+code,i,d.get(id_field),'school',d.get(name_field),shape(f['geometry']) if f.get('geometry') else None)
    summary={}
    queue={'automatic_merge':False,'records':[], 'osm_point_polygon':[], 'osm_polygon_overlap':[],
           'paho_osm_same_name':[], 'cnigs_osm_same_name':[], 'paho_department_mismatches':[]}
    sources=sorted({r['source'] for r in all_records})
    for source in sources:
        rows=[r for r in all_records if r['source']==source];inside=[r for r in rows if r['state']=='in_haiti']
        located=[r for r in rows if r['geometry'] is not None and not r['geometry'].is_empty and r['geometry'].is_valid]
        exact=groups(inside,lambda r:normalize(r['geometry']).wkb)
        repeated=groups(rows,lambda r:r['source_id'])
        summary[source]={'records':len(rows),'states':dict(collections.Counter(r['state'] for r in rows)),
            'inside_national_department_union':sum(r.get('national_boundary_intersects',False) for r in rows),
            'inside_national_but_outside_pinned':sum(r.get('national_boundary_intersects',False) and r['state']=='outside_pinned_boundary' for r in rows),
            'inside_pinned_but_outside_national':sum(r['state']=='in_haiti' and not r.get('national_boundary_intersects',False) for r in rows),
            'classes_in_haiti':dict(collections.Counter(r['class'] for r in inside)),
            'classes_in_national_boundary':dict(collections.Counter(r['class'] for r in rows if r.get('national_boundary_intersects',False))),
            'national_department_counts':dict(collections.Counter(r['national_department'] for r in rows if r.get('national_boundary_intersects',False))),
            'department_class_counts':{n:dict(collections.Counter(r['class'] for r in inside if r['department']==n)) for n in sorted({n for n,_ in departments}|{'UNMATCHED','AMBIGUOUS'})},
            'blank_names_in_haiti':sum(not r['name_key'] for r in inside),
            'missing_source_ids_all_records':sum(not r['source_id'] for r in rows),
            'repeated_source_id_groups_all_records':repeated,
            'exact_geometry_groups_in_haiti':exact,
            'exact_geometry_excess_in_haiti':sum(len(g)-1 for g in exact),
            'distinct_located_coordinates_all_records':len({r['geometry'].wkb for r in located}) if all(r['geometry'].geom_type=='Point' for r in located) else None}
    osm=[r for r in all_records if r['source'].startswith('osm_') and r['state']=='in_haiti']
    points=[r for r in osm if r['source']=='osm_point'];polygons=[r for r in osm if r['source']=='osm_polygon']
    tree=STRtree([r['geometry'] for r in polygons])
    def relation(a,b):
        if not a['name_key'] or not b['name_key']:return 'missing_name'
        return 'same_normalized_name' if a['name_key']==b['name_key'] else 'different_names'
    for p in points:
        for i in tree.query(p['geometry'],predicate='intersects'):
            g=polygons[int(i)]
            if theme(p['class'])==theme(g['class']) and g['geometry'].covers(p['geometry']):
                queue['osm_point_polygon'].append({'point':p['key'],'polygon':g['key'],'theme':theme(p['class']),
                    'name_relation':relation(p,g),'same_native_class':p['class']==g['class']})
    for i,a in enumerate(polygons):
        for j in tree.query(a['geometry'],predicate='intersects'):
            j=int(j)
            if j<=i:continue
            b=polygons[j]
            if theme(a['class'])==theme(b['class']) and a['geometry'].intersection(b['geometry']).area>0:
                queue['osm_polygon_overlap'].append({'a':a['key'],'b':b['key'],'theme':theme(a['class']),'name_relation':relation(a,b)})
    # Repeated names flag candidates, including distant institutions; no proximity cutoff.
    queue['osm_repeated_name_groups']=groups(osm,lambda r:(theme(r['class']),r['name_key']) if r['name_key'] else '')
    paho=[r for r in all_records if r['source']=='paho' and r['state']=='in_haiti']
    utm=Transformer.from_crs(4326,32618,always_xy=True).transform
    osm_by_name=collections.defaultdict(list)
    for r in osm:
        if theme(r['class'])=='health' and r['name_key']:osm_by_name[r['name_key']].append(r)
    for r in paho:
        if r['department'] not in ('UNMATCHED','AMBIGUOUS') and name_key(r['extra']['native_department'])!=name_key(r['department']):
            queue['paho_department_mismatches'].append({'key':r['key'],'native':r['extra']['native_department'],'spatial':r['department']})
        for o in osm_by_name.get(r['name_key'],[]):
            distance=transform(utm,r['geometry']).distance(transform(utm,o['geometry']))
            queue['paho_osm_same_name'].append({'paho':r['key'],'osm':o['key'],'distance_to_geometry_m':round(distance,3)})
    for r in [r for r in all_records if r['source'].startswith('cnigs_school_') and r['state']=='in_haiti' and r['name_key']]:
        for o in osm:
            if theme(o['class'])=='school' and o['name_key']==r['name_key']:
                distance=transform(utm,r['geometry']).distance(transform(utm,o['geometry']))
                queue['cnigs_osm_same_name'].append({'cnigs':r['key'],'osm':o['key'],'distance_to_geometry_m':round(distance,3)})
    for r in all_records:
        if r['state']=='in_haiti' or r['source']=='paho':
            queue['records'].append({k:v for k,v in r.items() if k!='geometry'})
    for key in ('osm_point_polygon','osm_polygon_overlap','paho_osm_same_name','cnigs_osm_same_name','paho_department_mismatches'):
        queue[key]=sorted(queue[key],key=lambda x:json.dumps(x,sort_keys=True))
    output.mkdir(parents=True,exist_ok=True)
    qpath=output/'review_queue.json';qpath.write_text(json.dumps(queue,indent=2,ensure_ascii=False)+'\n')
    def grouped_pairs(key):
        return dict(collections.Counter(p['theme']+' / '+p['name_relation'] for p in queue[key]))
    result={'runtime_ready':False,'automatic_merge':False,'exposure_computed':False,
        'input_sha256':{('boundary.json' if p==boundary_path else p.name):sha(p) for p in input_paths},
        'department_features':len(departments),'sources':summary,
        'osm_point_polygon_pairs':len(queue['osm_point_polygon']),
        'osm_point_polygon_by_theme_name':grouped_pairs('osm_point_polygon'),
        'osm_polygon_overlap_pairs':len(queue['osm_polygon_overlap']),
        'osm_polygon_overlap_by_theme_name':grouped_pairs('osm_polygon_overlap'),
        'osm_repeated_nonblank_name_groups':len(queue['osm_repeated_name_groups']),
        'paho_osm_same_name_pairs':len(queue['paho_osm_same_name']),
        'cnigs_osm_same_name_pairs':len(queue['cnigs_osm_same_name']),
        'paho_department_mismatch_count':len(queue['paho_department_mismatches']),
        'review_queue_sha256':sha(qpath)}
    (output/'inspection.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    records_by_key = {r['key']:r for r in queue['records']}
    strong = []
    for group in summary['osm_point']['exact_geometry_groups_in_haiti']:
        rows = [records_by_key[key] for key in group]
        if len({r['name_key'] for r in rows}) == 1 and rows[0]['name_key'] and len({r['class'] for r in rows}) == 1:
            strong.append(group)
    def distance_range(key):
        values = [pair['distance_to_geometry_m'] for pair in queue[key]]
        return [min(values),max(values)] if values else []
    review = {'decision':'unresolved_candidates_not_deleted',
        'same_name_class_exact_point_groups':strong,
        'same_name_point_polygon_pairs':[p for p in queue['osm_point_polygon'] if p['name_relation']=='same_normalized_name'],
        'point_polygon_pair_counts':result['osm_point_polygon_by_theme_name'],
        'polygon_overlap_pair_counts':result['osm_polygon_overlap_by_theme_name'],
        'cross_source_name_distance_range_m':{'paho_osm':distance_range('paho_osm_same_name'),'cnigs_osm':distance_range('cnigs_osm_same_name')}}
    (output/'review_summary.json').write_text(json.dumps(review,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('input_sha256','sources')},indent=2))
    for key,value in summary.items():print(key,value['states'],value['classes_in_haiti'])

if __name__=='__main__':main()
