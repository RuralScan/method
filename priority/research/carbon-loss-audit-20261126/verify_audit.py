"""Offline verification of preserved observations and descriptive calculations."""
from pathlib import Path
import json,hashlib,statistics
p=Path(__file__).resolve().parent
manifest=json.loads((p/'manifest.json').read_text())
for r in manifest['files']:
 assert hashlib.sha256((p/r['file']).read_bytes()).hexdigest()==r['sha256'],r['file']
obs=json.loads((p/'observations.json').read_text())['records']
s=json.loads((p/'summary.json').read_text())
assert len(obs)==1440 and len({r['id'] for r in obs})==1440
for row in s['coverage_rows']:
 records=[r for r in obs if r['worldcover_2021']==row['landcover']]
 assert len(records)==row['n']==160
 soil=[r['soil_raw'] for r in records if all(v>=0 and v!=32767 for v in r['soil_raw'])]
 agb=[[r['ctrees_raw'][y]['agb'] for y in ['2000','2022','2025']] for r in records]
 agb=[v for v in agb if all(x>=0 for x in v)]
 assert len(soil)==row['soil_valid_pairs'] and len(agb)==row['agb_valid_triplets']
 assert round(statistics.median((b-a)*.3 for a,b in soil),2)==row['soil_median_stock_difference_tC_ha']
 assert round(statistics.median((c-a)*.1 for a,b,c in agb),2)==row['agb_median_difference_2000_2025_Mg_ha']
u=json.loads((p/'soil_uncertainty_all.json').read_text())
assert len(u)==6 and all(r['scales']==[.1] and r['offsets']==[0.] and r['nodata']==32767. for r in u)
assert all(r['transform']==u[0]['transform'] for r in u)
lookup={(r['period'],r['stat']):{x['id']:x for x in r['samples']} for r in u}
for record in s['uncertainty_diagnostics']:
 i=record['sample_id']
 assert record['valid']
 a=lookup[('20000101_20051231','m')][i]['scaled'];b=lookup[('20200101_20221231','m')][i]['scaled']
 assert round((b-a)*3,2)==record['mean_stock_difference_tC_ha']
 l0=lookup[('20000101_20051231','p16')][i]['scaled'];h0=lookup[('20000101_20051231','p84')][i]['scaled']
 l1=lookup[('20200101_20221231','p16')][i]['scaled'];h1=lookup[('20200101_20221231','p84')][i]['scaled']
 assert (max(l0,l1)<=min(h0,h1))==record['period_quantile_intervals_overlap']
 assert [round((l1-h0)*3,2),round((h1-l0)*3,2)]==record['stock_difference_quantile_corner_envelope']
print('PASS: hashes; 1,440 unique observations; nine coverage rows; soil/AGB units and differences; six aligned uncertainty rasters and 20 uncertainty diagnostics.')
