"""Native-grid Haiti check; values are Mg C/year/pixel, not per hectare."""
from pathlib import Path
import json,hashlib
import rasterio,numpy as np
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds,transform
root=Path(__file__).resolve().parent
boundary=root.parent/'haiti-diagnostic-inputs-20261126/boundary.json';points=root.parent/'haiti-diagnostic-inputs-20261126/stratified_points.geojson'
geom=[f['geometry'] for f in json.loads(boundary.read_text())['features']];features=json.loads(points.read_text())['features']
report={'boundary_sha256':hashlib.sha256(boundary.read_bytes()).hexdigest(),'points_sha256':hashlib.sha256(points.read_bytes()).hexdigest(),'boundary_convention':'cell centres; totals are diagnostics, not exact administrative totals','rasters':[]};values={}
for name in ['bc_100_tech.tif','bc_100_constrained.tif']:
 p=root/name
 with rasterio.open(p) as d:
  assert d.crs.to_epsg()==4326
  w=from_bounds(-74.6,18,-71.5,20.2,d.transform).round_offsets().round_lengths();a=d.read(1,window=w,masked=True)
  inside=geometry_mask(geom,out_shape=a.shape,transform=transform(w,d.transform),invert=True,all_touched=False)
  v=a[inside].compressed();values[name]=a
  rec={'file':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'md5':hashlib.md5(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'crs':str(d.crs),'transform':list(d.transform),'shape':[d.height,d.width],'nodata':('NaN' if d.nodata is not None and np.isnan(d.nodata) else d.nodata),'dtype':d.dtypes,'units':d.units,'scales':d.scales,'offsets':d.offsets,'tags':d.tags(),'band_tags':d.tags(1),'boundary_cells':int(inside.sum()),'valid':len(v),'missing':int(np.ma.getmaskarray(a)[inside].sum()),'positive':int((v>0).sum()),'zero':int((v==0).sum()),'negative':int((v<0).sum()),'min':float(v.min()),'max':float(v.max()),'sum_MgC_per_year_cell_centre_diagnostic':float(v.sum(dtype=np.float64))}
  samples=[]
  for f,val in zip(features,d.sample([f['geometry']['coordinates'] for f in features],masked=True)):
   row,col=d.index(*f['geometry']['coordinates']);samples.append({'id':f['id'],'landcover':f['properties']['landcover'],'row':row,'col':col,'value':None if np.ma.is_masked(val[0]) else float(val[0])})
  rec['sample_count']=len(samples);rec['unique_sample_cells']=len({(x['row'],x['col']) for x in samples});rec['crop_samples']={'n':sum(x['landcover']==40 for x in samples),'positive':sum(x['landcover']==40 and x['value'] is not None and x['value']>0 for x in samples),'missing':sum(x['landcover']==40 and x['value'] is None for x in samples)}
  (root/(name+'_samples.json')).write_text(json.dumps(samples,indent=2));report['rasters'].append(rec)
report['constrained_exceeds_technical_cells']=int(np.ma.filled((values['bc_100_constrained.tif']>values['bc_100_tech.tif'])[inside],False).sum())
(root/'biochar_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
