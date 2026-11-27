"""Inspect producer 120 m means and prediction quantiles at stratified Haiti points."""
from pathlib import Path
import json, math, concurrent.futures
import rasterio
from rasterio.windows import Window
p=Path(__file__).resolve().parent
features=json.loads((p/'stratified_points.geojson').read_text())['features']
selected=[]
for cls,n in [(10,4),(20,4),(30,4),(40,4),(90,2),(95,2)]:
 candidates=[f for f in features if f['properties']['landcover']==cls]
 chosen=[candidates[0]]
 while len(chosen)<min(n,len(candidates)):
  chosen.append(max((f for f in candidates if f not in chosen),key=lambda f:min(sum((a-b)**2 for a,b in zip(f['geometry']['coordinates'],g['geometry']['coordinates'])) for g in chosen)))
 selected.extend(chosen)
(p/'uncertainty_points.geojson').write_text(json.dumps({'type':'FeatureCollection','features':selected},indent=2))
base='https://s3.opengeohub.org/global-soil/global_soil_props_v20250204_mosaics/'
tasks=[(period,stat,base+f'oc_iso.10694.1995.mg.cm3_{stat}_120m_b0cm..30cm_{period}_g_epsg.4326_v20250204.tif') for period in ['20000101_20051231','20200101_20221231'] for stat in ['m','p16','p84']]
def run(task):
 period,stat,url=task
 try:
  with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',GDAL_HTTP_TIMEOUT='30'),rasterio.open(url) as ds:
   samples=[]
   for f in selected:
    x,y=f['geometry']['coordinates'];row,col=ds.index(x,y)
    a=ds.read(1,window=Window(col,row,1,1),masked=True)
    value=None if a.mask.all() else float(a[0,0])
    samples.append({'id':f['id'],'landcover':f['properties']['landcover'],'coordinate':[x,y],'raw':value,'scaled':None if value is None else value*ds.scales[0]+ds.offsets[0]})
   result={'period':period,'stat':stat,'url':url,'crs':str(ds.crs),'transform':list(ds.transform),'nodata':ds.nodata,'scales':ds.scales,'offsets':ds.offsets,'samples':samples}
 except Exception as e:result={'period':period,'stat':stat,'url':url,'error':str(e)}
 (p/f'soil_uncertainty_{period}_{stat}.json').write_text(json.dumps(result,indent=2))
 print(period,stat,'samples',len(result.get('samples',[])),'error',result.get('error',''),flush=True)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(run,tasks))
(p/'soil_uncertainty_all.json').write_text(json.dumps(results,indent=2))
