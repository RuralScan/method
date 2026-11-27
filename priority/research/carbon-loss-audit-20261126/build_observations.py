from pathlib import Path
import json,statistics,hashlib,datetime
p=Path(__file__).resolve().parent
points=json.loads((p/'stratified_points.geojson').read_text())['features']
data={f.name.split('_samples')[0]:{x['properties']['sample_id']:x['properties'] for x in json.loads(f.read_text())['features']} for f in p.glob('*_samples.geojson')}
ids={f['id'] for f in points}
assert len(ids)==1440 and all(set(rows)==ids for rows in data.values())
records=[]
for f in points:
 i=f['id'];record={'id':i,'lon_lat':f['geometry']['coordinates'],'worldcover_2021':f['properties']['landcover'],'soil_raw':[data['soil_2000_2005'][i]['mg_cm3'],data['soil_2020_2022'][i]['mg_cm3']],'ctrees_raw':{year:{k:data['ctrees_'+year][i][k] for k in ['agb','uncertainty']} for year in ['2000','2022','2025']}}
 records.append(record)
(p/'observations.json').write_text(json.dumps({'design':{'boundary':'USDOS/LSIB_SIMPLE/2017','country_filter':{'country_na':'Haiti'},'landcover':'ESA/WorldCover/v200','stratified_sampling_grid':'EPSG:32618, 100 m, nearest class sampling','seed':20261126,'points_per_present_class':160,'native_sampling':'Each carbon image sampled at its native projection with nearest-neighbour lookup; output pixel-centre geometry differs between products. Records retain original sample coordinates.','missing_sentinel':-9999,'soil_period_order':['2000–2005','2020–2022'],'soil_depth_cm':[0,30],'soil_scale':0.1,'soil_native_nodata':32767,'ctrees_scale':0.1,'warning':'Equal class allocation is not area weighting. 2021 land cover is not historical land use. Negative/unknown values must not be scored zero.'},'records':records},separators=(',',':'))+'\n')
s=json.loads((p/'summary.json').read_text())
extra=[]
for cls in [10,20,30,40,90,95]:
 valid=[r for r in records if r['worldcover_2021']==cls and all(r['ctrees_raw'][y]['agb']>=0 and r['ctrees_raw'][y]['uncertainty']>=0 for y in ['2000','2025'])]
 extra.append({'landcover':cls,'n':len(valid),'median_absolute_AGB_difference_Mg_ha':round(statistics.median(abs(r['ctrees_raw']['2025']['agb']-r['ctrees_raw']['2000']['agb'])*.1 for r in valid),2),'median_uncertainty_2000_Mg_ha':round(statistics.median(r['ctrees_raw']['2000']['uncertainty']*.1 for r in valid),2),'median_uncertainty_2025_Mg_ha':round(statistics.median(r['ctrees_raw']['2025']['uncertainty']*.1 for r in valid),2)})
s['ctrees_uncertainty_scale_check']=extra
s['ctrees_uncertainty_warning']='Comparison of stock-change magnitude with marginal stock uncertainty only; not a temporal-change significance test. Cross-time covariance not supplied in inspected bands.'
(p/'summary.json').write_text(json.dumps(s,indent=2)+'\n')
print('Verified 1440 unique matching point IDs across five images; compact observations bytes:',(p/'observations.json').stat().st_size)
