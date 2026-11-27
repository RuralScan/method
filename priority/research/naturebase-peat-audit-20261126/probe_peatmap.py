"""Inspect PEATMAP intersections; counts describe features, never eligible hectares."""
import argparse,hashlib,json,zipfile
from pathlib import Path
import fiona
from shapely.geometry import shape
from shapely.ops import unary_union,transform
from pyproj import Transformer
ap=argparse.ArgumentParser();ap.add_argument('package');ap.add_argument('boundary');ap.add_argument('output');args=ap.parse_args()
zpath=Path(args.package).resolve();boundary=Path(args.boundary)
haiti=unary_union([shape(f['geometry']) for f in json.loads(boundary.read_text())['features']])
report={'source_url':'https://archive.researchdata.leeds.ac.uk/251/11/North_America.zip','zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'boundary_sha256':hashlib.sha256(boundary.read_bytes()).hexdigest(),'layers':[]}
with zipfile.ZipFile(zpath) as z: members=[n for n in z.namelist() if n.lower().endswith('.shp')]
for n in members:
 with fiona.open('zip://'+str(zpath)+'!'+n) as d:
  crs=str(d.crs);total=len(d)
  target=transform(Transformer.from_crs('EPSG:4326',d.crs,always_xy=True).transform,haiti)
  candidates=list(d.filter(bbox=target.bounds));matches=[]
  for f in candidates:
   g=shape(f['geometry'])
   if g.intersects(target): matches.append({'id':f.id,'properties':dict(f['properties']),'positive_area_intersection':g.intersection(target).area>0})
  report['layers'].append({'member':n,'crs':crs,'schema':d.schema,'total_features_before_filter':total,'bounds':d.bounds,'bbox_candidates':len(candidates),'haiti_intersection_count':len(matches),'positive_area_intersection_count':sum(m['positive_area_intersection'] for m in matches),'haiti_intersections':matches})
Path(args.output).write_text(json.dumps(report,indent=2))
print([(r['member'],r['total_features_before_filter'],r['haiti_intersection_count'],r['positive_area_intersection_count']) for r in report['layers']])
