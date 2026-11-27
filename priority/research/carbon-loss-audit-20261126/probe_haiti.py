"""Exploratory land-cover-stratified access probe, not a production analytical rule."""
from pathlib import Path
import json, collections
import ee
p=Path(__file__).resolve().parent
ee.Initialize(); ee.data.setDeadline(90000)
boundary=ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017').filter(ee.Filter.eq('country_na','Haiti'))
region=boundary.geometry()
(p/'boundary.json').write_text(json.dumps(boundary.getInfo(),indent=2))
land=ee.ImageCollection('ESA/WorldCover/v200').first().select('Map').rename('landcover')
classes=[10,20,30,40,50,60,80,90,95,100]
points=land.stratifiedSample(numPoints=160,classBand='landcover',region=region,scale=100,projection='EPSG:32618',seed=20261126,classValues=classes,classPoints=[160]*len(classes),geometries=True,tileScale=4)
if (p/'stratified_points.geojson').exists():
 raw=json.loads((p/'stratified_points.geojson').read_text())
elif (p/'observations.json').exists():
 saved=json.loads((p/'observations.json').read_text())['records']
 raw={'type':'FeatureCollection','features':[{'type':'Feature','id':r['id'],'geometry':{'type':'Point','coordinates':r['lon_lat']},'properties':{'landcover':r['worldcover_2021']}} for r in saved]}
else:
 raw=points.getInfo()
(p/'stratified_points.geojson').write_text(json.dumps(raw,indent=2))
print('POINTS',dict(collections.Counter(x['properties']['landcover'] for x in raw['features'])),flush=True)
# Preserve all points: masked image values are sentinels, not dropped records.
points=ee.FeatureCollection([ee.Feature(ee.Geometry.Point(f['geometry']['coordinates'],proj=f['geometry'].get('crs',{}).get('properties',{}).get('name','EPSG:4326')),dict(f['properties'],sample_id=f['id'])) for f in raw['features']])
soilroot='projects/global-pasture-watch/assets/gsm-30m/v1/oc_iso_10694_1995_mg_cm3/'
ids=[(f'soil_{period}',soilroot+period+'_b0_30cm') for period in ['2000_2005','2020_2022']]
root='projects/sat-io/open-datasets/CTREES-GLOBAL-AGB-100M/'
ids += [(f'ctrees_{year}',root+f'ctrees_global_agb_100m_{year}') for year in [2000,2022,2025]]
outputs=[]
for name,aid in ids:
 im=ee.Image(aid)
 result=im.toFloat().unmask(-9999,sameFootprint=False).sampleRegions(collection=points,projection=im.select(0).projection(),geometries=True,tileScale=4).getInfo()
 (p/(name+'_samples.geojson')).write_text(json.dumps(result,indent=2))
 (p/(name+'_metadata.json')).write_text(json.dumps(ee.data.getAsset(aid),indent=2))
 print(name,'samples',len(result['features']),flush=True)
 outputs.append({'label':name,'asset':aid,'samples':len(result['features'])})
(p/'probe_index.json').write_text(json.dumps(outputs,indent=2))
