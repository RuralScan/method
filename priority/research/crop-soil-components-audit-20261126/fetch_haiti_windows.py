"""Read only Haiti windows from approved public originals; never treat clips as global files."""
from pathlib import Path
import json
import rasterio
from rasterio.features import bounds
from rasterio.windows import from_bounds,transform
root=Path(__file__).resolve().parent
geometries=[f['geometry'] for f in json.loads((root.parent/'haiti-diagnostic-inputs-20261126/boundary.json').read_text())['features']]
box=bounds({'type':'GeometryCollection','geometries':geometries})
for key,fileid in [('crop_I',4202142),('crop_MGI',4202145)]:
 import subprocess
 url=subprocess.check_output(['curl','-fsSL','--max-time','30','--range','0-0','--output','/dev/null','--write-out','%{url_effective}',f'https://dataverse.harvard.edu/api/access/datafile/{fileid}'],text=True)
 with rasterio.Env(CPL_VSIL_CURL_USE_HEAD='NO',GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',GDAL_HTTP_TIMEOUT='60',GDAL_HTTP_USERAGENT='curl/8.7.1'):
  with rasterio.open('/vsicurl/'+url) as src:
   assert str(src.crs)=='EPSG:4326' and src.count==1, 'Unexpected source grid; revise window transformation explicitly'
   pad=max(src.res);window=from_bounds(box[0]-pad,box[1]-pad,box[2]+pad,box[3]+pad,src.transform).round_offsets().round_lengths()
   print(key,'reading Haiti window',list(window.flatten()),flush=True)
   array=src.read(1,window=window)
   profile=src.profile.copy();profile.update(width=array.shape[1],height=array.shape[0],transform=transform(window,src.transform),compress='LZW')
   out=root/(key+'_haiti_native_window.tif')
   with rasterio.open(out,'w',**profile) as dst:dst.write(array,1)
   record={'file_id':fileid,'original_shape':[src.height,src.width],'original_transform':list(src.transform),'original_crs':str(src.crs),'window':list(window.flatten()),'clip_file':out.name,'method':'HTTP Range GET through official public Dataverse datafile endpoint; native-grid subset only; signed transport URL not retained'}
   (root/(key+'_window_provenance.json')).write_text(json.dumps(record,indent=2)+'\n')
   print(key,'saved',out.stat().st_size,flush=True)
