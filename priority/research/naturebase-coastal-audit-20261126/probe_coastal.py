"""Read-only Naturebase package inspection; no accepted analytical rules."""
import argparse,hashlib,json,zipfile
from pathlib import Path
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds, transform as window_transform

ap=argparse.ArgumentParser();ap.add_argument('package');ap.add_argument('points');ap.add_argument('boundary');ap.add_argument('output');args=ap.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def stats(a):
 a=np.asarray(a);a=a[np.isfinite(a)]
 return {'valid':len(a),'zero':int((a==0).sum()),'positive':int((a>0).sum()),'negative':int((a<0).sum()),'min':float(a.min()) if len(a) else None,'median':float(np.median(a)) if len(a) else None,'max':float(a.max()) if len(a) else None}
points=json.loads(Path(args.points).read_text())['features'];boundary=json.loads(Path(args.boundary).read_text());geom=[f['geometry'] for f in boundary['features']]
meta={'package':{'name':Path(args.package).name,'sha256':sha(args.package)},'input_hashes':{'points':sha(args.points),'boundary':sha(args.boundary)},'members':[],'rasters':[]}
with zipfile.ZipFile(args.package) as z:
 for i in z.infolist():
  meta['members'].append({'name':i.filename,'bytes':i.file_size,'crc32':i.CRC})
  if i.is_dir() or '/' in i.filename or Path(i.filename).suffix.lower() not in ('.csv','.txt','.tif'):continue
  target=out/Path(i.filename).name
  if not target.exists():
   with z.open(i) as src,target.open('wb') as dst:
    import shutil;shutil.copyfileobj(src,dst)
  if not target.suffix.lower()=='.tif':continue
  with rasterio.open(target) as d:
   m={'member':i.filename,'sha256':sha(target),'crs':str(d.crs),'transform':list(d.transform),'shape':[d.height,d.width],'bands':d.count,'dtype':d.dtypes,'nodata':d.nodata,'scales':d.scales,'offsets':d.offsets,'units':d.units,'descriptions':d.descriptions,'tags':d.tags(),'band_tags':d.tags(1),'bounds':list(d.bounds),'blocks':d.block_shapes}
   assert str(d.crs)=='EPSG:4326','Transform Haiti coordinates before sampling other CRS'
   samples=[]
   for f,v in zip(points,d.sample([p['geometry']['coordinates'] for p in points],masked=True)):
    xy=f['geometry']['coordinates'];row,col=d.index(*xy);val=None if np.ma.is_masked(v[0]) else float(v[0])
    samples.append({'id':f['id'],'landcover':f['properties']['landcover'],'lon':xy[0],'lat':xy[1],'row':row,'col':col,'value':val})
   for xy in [(-74.04,18.38),(-72.29,18.35),(-72.5,19.2),(-73,18)]:
    v=next(d.sample([xy],masked=True));samples.append({'id':'diagnostic_'+str(xy),'lon':xy[0],'lat':xy[1],'value':None if np.ma.is_masked(v[0]) else float(v[0])})
   m['stratified_summary']={str(c):stats([x['value'] for x in samples if x.get('landcover')==c and x['value'] is not None]) for c in sorted(set(f['properties']['landcover'] for f in points))}
   m['unique_sample_pixels']=len(set((x['row'],x['col']) for x in samples if 'row' in x))
   w=from_bounds(-74.6,18,-71.5,20.2,d.transform).round_offsets().round_lengths();a=d.read(1,window=w,masked=True);inside=geometry_mask(geom,out_shape=a.shape,transform=window_transform(w,d.transform),invert=True,all_touched=False)
   m['haiti_cell_centre_summary']=stats(a[inside].compressed());m['haiti_cell_centres']=int(inside.sum());m['haiti_missing_cells']=int(np.ma.getmaskarray(a)[inside].sum());m['sample_file']=target.stem+'_samples.json'
   (out/m['sample_file']).write_text(json.dumps(samples,indent=2));meta['rasters'].append(m)
(out/'inspection.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
