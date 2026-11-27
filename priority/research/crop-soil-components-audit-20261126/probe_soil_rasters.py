"""Inspect approved original soil scenarios; diagnostic statistics, not analytical rules."""
from pathlib import Path
import json,hashlib
import numpy as np
import rasterio
from rasterio.features import geometry_mask,bounds
from rasterio.windows import from_bounds,transform
from rasterio.warp import transform_geom,transform as transform_xy
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parent)
parser.add_argument('--scenario',choices=['crop_MG','crop_I','crop_MGI'])
parser.add_argument('--haiti-windows',action='store_true',help='Use range-acquired Haiti subsets for input and joint scenarios')
args=parser.parse_args()
root=args.data_dir.resolve()
boundary=root.parent/'haiti-diagnostic-inputs-20261126/boundary.json';points=root.parent/'haiti-diagnostic-inputs-20261126/stratified_points.geojson'
geometries=[f['geometry'] for f in json.loads(boundary.read_text())['features']];features=json.loads(points.read_text())['features']
files={'crop_MG':'scenario_crop_MG_dSOC_Y20.tif','crop_I':'scenario_crop.I_dSOC_Y20.tif','crop_MGI':'scenario_crop.MGI_dSOC_Y20.tif'}
if args.haiti_windows:
 files.update(crop_I='crop_I_haiti_native_window.tif',crop_MGI='crop_MGI_haiti_native_window.tif')
sample_suffix='_window_samples.json' if args.haiti_windows else '_original_samples.json'
def checksum(p,algorithm):
 h=hashlib.new(algorithm)
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def stats(v):
 v=np.asarray(v,dtype=np.float64);v=v[np.isfinite(v)]
 return {'valid':len(v),'positive':int((v>0).sum()),'zero':int((v==0).sum()),'negative':int((v<0).sum()),'min':float(v.min()) if len(v) else None,'median':float(np.median(v)) if len(v) else None,'max':float(v.max()) if len(v) else None,'mean':float(v.mean()) if len(v) else None}
report={'acquisition_scope':'full no-till plus native Haiti input/joint subsets' if args.haiti_windows else 'three full original global files','boundary_sha256':checksum(boundary,'sha256'),'points_sha256':checksum(points,'sha256'),'boundary_convention':'native cell centres','units':'Mg C/ha stock change over 20 years, depth 0-30 cm; not annual observations','rasters':[]};arrays={};grids={}
for scenario,name in files.items():
 if args.scenario and scenario!=args.scenario:continue
 p=root/name
 with rasterio.open(p) as d:
  geom=[transform_geom('EPSG:4326',d.crs,g) for g in geometries];box=bounds({'type':'GeometryCollection','geometries':geom});pad=max(abs(d.res[0]),abs(d.res[1]));box=(box[0]-pad,box[1]-pad,box[2]+pad,box[3]+pad)
  w=from_bounds(*box,d.transform).round_offsets().round_lengths();a=d.read(1,window=w,masked=True);wt=transform(w,d.transform);inside=geometry_mask(geom,out_shape=a.shape,transform=wt,invert=True,all_touched=False)
  values=np.ma.masked_invalid(a[inside]);arrays[scenario]=values;grids[scenario]=(str(d.crs),tuple(wt),a.shape)
  nodata=d.nodata
  rec={'scenario':scenario,'file':name,'sha256':checksum(p,'sha256'),'md5':checksum(p,'md5'),'bytes':p.stat().st_size,'crs':str(d.crs),'transform':list(d.transform),'shape':[d.height,d.width],'bands':d.count,'dtype':d.dtypes,'compression':str(d.compression),'block_shapes':d.block_shapes,'nodata':('NaN' if nodata is not None and np.isnan(nodata) else nodata),'scales':d.scales,'offsets':d.offsets,'units_tag':d.units,'tags':d.tags(),'band_tags':d.tags(1),'boundary_cells':int(inside.sum()),'missing':int(np.ma.getmaskarray(values).sum()),'haiti_statistics':stats(values.compressed())}
  xy=[f['geometry']['coordinates'] for f in features];xx,yy=transform_xy('EPSG:4326',d.crs,[c[0] for c in xy],[c[1] for c in xy]);samples=[]
  for f,x,y,val in zip(features,xx,yy,d.sample(list(zip(xx,yy)),masked=True)):
   row,col=d.index(x,y);v=None if np.ma.is_masked(val[0]) or not np.isfinite(val[0]) else float(val[0]);samples.append({'id':f['id'],'landcover':f['properties']['landcover'],'row':row,'col':col,'value':v})
  rec['unique_sample_cells']=len({(x['row'],x['col']) for x in samples});rec['sample_statistics']={str(c):dict(stats([x['value'] for x in samples if x['landcover']==c and x['value'] is not None]),missing=sum(x['landcover']==c and x['value'] is None for x in samples)) for c in sorted({x['landcover'] for x in samples})}
  (root/(scenario+sample_suffix)).write_text(json.dumps(samples,indent=2,allow_nan=False)+'\n');report['rasters'].append(rec)
  print(scenario,rec['boundary_cells'],rec['haiti_statistics'],'cropland',rec['sample_statistics']['40'],flush=True)
if args.scenario:
 (root/(args.scenario+'_raster_checks.json')).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
 raise SystemExit(0)
assert len(set(grids.values()))==1,'Native grids differ; do not compare without an explicit alignment'
mg,inp,joint=[arrays[k].astype(np.float64) for k in ['crop_MG','crop_I','crop_MGI']]
mask=np.ma.getmaskarray(mg)|np.ma.getmaskarray(inp)|np.ma.getmaskarray(joint)
m,i,j=[np.asarray(a)[~mask] for a in [mg,inp,joint]]
diff=j-m-i;both=(m+i)>0
positive_all=(m>0)&(i>0)&(j>0)
report['joint_vs_sum']={'mask_disagreement_cells':int(((np.ma.getmaskarray(mg)!=np.ma.getmaskarray(inp))|(np.ma.getmaskarray(mg)!=np.ma.getmaskarray(joint))).sum()),'common_valid_cells':len(diff),'joint_minus_MG_minus_I':stats(diff),'within_1e_minus_5_MgC_per_ha':int((np.abs(diff)<=1e-5).sum()),'tolerance_role':'floating-point diagnostic only; no analytical class boundary','joint_over_sum_when_sum_positive':stats(j[both]/(m[both]+i[both])),'all_three_positive_cells':int(positive_all.sum()),'joint_minus_sum_on_all_positive':stats(diff[positive_all]),'joint_below_either_single_beyond_tolerance':int(((j<m-1e-5)|(j<i-1e-5)).sum())}
(root/('soil_window_checks.json' if args.haiti_windows else 'soil_raster_checks.json')).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps(report['joint_vs_sum'],indent=2))
