"""Summarize published Haiti totals and inspect consistency, without accepting estimates."""
import csv,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent;p=root/'crp_scc';prefix='crp_scc'
tables={}
for level in range(3):
 with (p/f'{prefix}_tco2e_adm{level}.csv').open() as f: tables[f'adm{level}']=[r for r in csv.DictReader(f) if r['adm0_id']=='HTI']
(p/'haiti_tables.json').write_text(json.dumps(tables,indent=2,ensure_ascii=False)+'\n')
summary={'record_counts':{k:len(v) for k,v in tables.items()},'national':tables['adm0'],'administrative_sums':{}}
for level,rows in tables.items():
 summary['administrative_sums'][level]={}
 for field in [prefix+'_tco2e',prefix+'_ha']:
  values=[float(r[field]) for r in rows if r[field] not in ['NA','']]
  summary['administrative_sums'][level][field]={'valid_records':len(values),'sum':sum(values)}
inspection=json.loads((p/'inspection.json').read_text());r=inspection['rasters'][0]
summary['raster']=r
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
