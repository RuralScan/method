"""Inspect source metadata and unresampled diagnostics; no national exposure claim."""
import csv,hashlib,json,math,os
from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import Window,from_bounds
ROOT=Path(os.environ.get('EROSION_AUDIT_ROOT', Path(__file__).resolve().parent))
METHOD=Path(os.environ.get('EROSION_METHOD_ROOT', ROOT.parent/'method'))
files=list((ROOT/'extracted').rglob('SOIL_DISPLACEMENT_ESTIMATE_2019.tif'))
assert len(files)==1,files
path=files[0]
rules=list(csv.DictReader((METHOD/'priority/classifications/rules.csv').open()))
rule=next(r for r in rules if r['rule_set_id']=='soil_erosion_published')
cuts=[float(rule[k]) for k in ['none_upper','low_upper','medium_upper']]
assert rule['unit']=='tonnes_per_ha_per_year'
print('Approved cutoffs loaded',cuts,flush=True)
def digest_file(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def summary(a):
 v=a.compressed();finite=v[np.isfinite(v)]
 return {'cells':int(a.size),'masked':int(np.ma.getmaskarray(a).sum()),'valid':int(v.size),'unmasked_nonfinite':int((~np.isfinite(v)).sum()),'negative':int((finite<0).sum()),'zero':int((finite==0).sum()),'min':float(finite.min()) if finite.size else None,'max':float(finite.max()) if finite.size else None,'quantiles':{str(q):float(np.quantile(finite,q)) for q in [0.05,0.5,0.95,0.99]} if finite.size else {}}
with rasterio.open(path) as ds:
 nodata=ds.nodata
 result={'file':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'crs':str(ds.crs),'bounds':list(ds.bounds),'shape':ds.shape,'resolution':ds.res,'count':ds.count,'dtype':ds.dtypes,'nodata':'NaN' if nodata is not None and math.isnan(nodata) else nodata,'scales':ds.scales,'offsets':ds.offsets,'block_shapes':ds.block_shapes,'tags':ds.tags(),'band_tags':ds.tags(1),'diagnostics':[]}
 print('Native metadata',json.dumps(result),flush=True)
 assert ds.count==1
 assert ds.crs.to_epsg()==4326
 assert tuple(ds.scales)==(1.0,) and tuple(ds.offsets)==(0.0,), 'Explicit scaling review needed'
 # Native-pixel windows around three previously checked crop-support sites.
 for index,(lon,lat) in enumerate([(-72.325,18.54),(-74.1,18.64),(-72.2,19.5)]):
  row,col=ds.index(lon,lat);w=Window(col-2,row-2,5,5);a=ds.read(1,window=w,masked=True)
  crop=ROOT/f'erosion_point_{index}.npy';np.save(crop,a.filled(nodata))
  result['diagnostics'].append({'lon':lon,'lat':lat,'row':row,'col':col,'summary':summary(a),'values_with_missing_null':[[None if np.ma.is_masked(v) or not np.isfinite(v) else float(v) for v in row_values] for row_values in a],'sample_file':crop.name,'sha256':digest_file(crop)})
 # This bbox includes ocean and adjacent Dominican Republic; never Haiti national statistics.
 requested=[-74.5,18,-71.6,20.1];w=from_bounds(*requested,ds.transform).round_offsets().round_lengths();a=ds.read(1,window=w,masked=True)
 sample=ROOT/'haiti_bbox_erosion_native.tif';profile={'driver':'GTiff','width':a.shape[1],'height':a.shape[0],'count':1,'dtype':ds.dtypes[0],'crs':ds.crs,'transform':ds.window_transform(w),'nodata':nodata,'compress':'deflate','tiled':True,'blockxsize':128,'blockysize':128}
 with rasterio.open(sample,'w',**profile) as out:out.write(a.filled(nodata),1)
 v=a.compressed();v=v[np.isfinite(v)&(v>=float(rule['domain_min']))];counts=np.bincount(np.searchsorted(cuts,v,side='left'),minlength=4).tolist()
 result['haiti_bbox']={'class_counts_0_1_2_3':counts,'cutoffs_from_rule_csv':cuts,'requested_bounds':requested,'actual_bounds':list(rasterio.windows.bounds(w,ds.transform)),'summary':summary(a),'file':sample.name,'sha256':digest_file(sample),'scope':'Diagnostic bounding box includes ocean and neighboring territory; not a national coverage or area estimate.'}
 # Sparse native windows across the raster check encoding, not representative global statistics.
 samples=[]
 for row in np.linspace(0,ds.height-256,12,dtype=int):
  for col in np.linspace(0,ds.width-256,24,dtype=int):
   b=ds.read(1,window=Window(int(col),int(row),256,256),masked=True);samples.append({'row':int(row),'col':int(col),'summary':summary(b)})
 result['sparse_global_windows']=samples
(ROOT/'erosion_raster_inspection.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print('Diagnostics saved; hashing extracted TIFF',flush=True)
result['sha256']=digest_file(path)
(ROOT/'erosion_raster_inspection.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print('DONE',json.dumps(result['haiti_bbox']),flush=True)
