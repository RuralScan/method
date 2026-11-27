"""Acquire only public top-level scientific members using HTTP byte ranges."""
import hashlib,json,zipfile,urllib.request
from pathlib import Path
from remotezip import RemoteZip
root=Path(__file__).resolve().parent
records=json.loads((root/'catalogue_records.json').read_text())['data']
for record in records:
 prefix=record['short_name'].replace('_total','');folder=root/prefix;folder.mkdir(exist_ok=True)
 url=record['download_links'][0]['url']
 with urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=30) as response:
  headers={k:response.headers[k] for k in ['Content-Length','Last-Modified','ETag','Content-Type']}
 manifest={'url':url,'headers':headers,'acquisition':'HTTP ranges; top-level CSV/TXT/TIF only; original whole archive not downloaded or SHA256-hashed','members':[],'selected':[]}
 with RemoteZip(url,timeout=40) as source,zipfile.ZipFile(folder/(prefix+'_selected.zip'),'w',compression=zipfile.ZIP_DEFLATED) as subset:
  for entry in source.infolist():
   manifest['members'].append({'name':entry.filename,'size':entry.file_size,'compressed_size':entry.compress_size,'crc32':entry.CRC})
   if entry.is_dir() or '/' in entry.filename or Path(entry.filename).suffix.lower() not in ['.csv','.txt','.tif']:continue
   data=source.read(entry.filename)
   subset.writestr(entry.filename,data)
   manifest['selected'].append({'name':entry.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc32_checked':True})
 (folder/'acquisition.json').write_text(json.dumps(manifest,indent=2))
 print(prefix,[(x['name'],x['bytes']) for x in manifest['selected']],flush=True)
