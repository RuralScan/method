from pathlib import Path
import json,statistics,collections
p=Path(__file__).resolve().parent
names={10:'Tree cover',20:'Shrubland',30:'Grassland',40:'Cropland',50:'Built-up',60:'Bare/sparse',80:'Permanent water',90:'Herbaceous wetland',95:'Mangroves'}
data={f.name.split('_samples')[0]:{x['properties']['sample_id']:x['properties'] for x in json.loads(f.read_text())['features']} for f in p.glob('*_samples.geojson')}
rows=[]
for cls,label in names.items():
 ids=[k for k,v in data['soil_2000_2005'].items() if v['landcover']==cls]
 soil=[(data['soil_2000_2005'][i]['mg_cm3'],data['soil_2020_2022'][i]['mg_cm3']) for i in ids]
 soil=[(a,b) for a,b in soil if a>=0 and b>=0 and a!=32767 and b!=32767]
 agb=[(data['ctrees_2000'][i]['agb'],data['ctrees_2022'][i]['agb'],data['ctrees_2025'][i]['agb']) for i in ids]
 agb=[v for v in agb if all(x>=0 for x in v)]
 row={'landcover':cls,'label':label,'n':len(ids),'soil_valid_pairs':len(soil),'agb_valid_triplets':len(agb),'soil_median_stock_difference_tC_ha':round(statistics.median([(b-a)*.3 for a,b in soil]),2) if soil else None,'soil_negative_difference_n':sum(b<a for a,b in soil),'agb_median_difference_2000_2022_Mg_ha':round(statistics.median([(b-a)*.1 for a,b,c in agb]),2) if agb else None,'agb_median_difference_2000_2025_Mg_ha':round(statistics.median([(c-a)*.1 for a,b,c in agb]),2) if agb else None,'agb_negative_difference_2000_2025_n':sum(c<a for a,b,c in agb)}
 rows.append(row)
 print(json.dumps(row))
unc=json.loads((p/'soil_uncertainty_all.json').read_text())
assert all('error' not in r for r in unc)
lookup={(r['period'],r['stat']):{v['id']:v for v in r['samples']} for r in unc}
for r in unc:print('unc encoding',r['period'],r['stat'],r['scales'],r['nodata'],r['transform'][:6])
results=[]
for pid,s in lookup[('20000101_20051231','m')].items():
 vals={f'{period}_{stat}':lookup[(period,stat)][pid]['scaled'] for period in ['20000101_20051231','20200101_20221231'] for stat in ['m','p16','p84']}
 if any(v is None for v in vals.values()):results.append({'sample_id':pid,'landcover':s['landcover'],'valid':False});continue
 a,l0,h0=[vals['20000101_20051231_'+v] for v in ['m','p16','p84']];b,l1,h1=[vals['20200101_20221231_'+v] for v in ['m','p16','p84']]
 assert l0<=h0 and l1<=h1
 results.append({'sample_id':pid,'landcover':s['landcover'],'valid':True,'mean_stock_difference_tC_ha':round((b-a)*3,2),'period_quantile_intervals_overlap':max(l0,l1)<=min(h0,h1),'stock_difference_quantile_corner_envelope':[round((l1-h0)*3,2),round((h1-l0)*3,2)],'values_kgC_m3':vals})
print('UNCERTAINTY',json.dumps(results,indent=2))
(p/'summary.json').write_text(json.dumps({'design':'Equal allocation 160 points per present WorldCover-2021 class on 100m UTM18N sampling grid; native image samples. Not area-weighted. Land cover labels are 2021 only.','coverage_rows':rows,'uncertainty_diagnostics':results,'uncertainty_warning':'20 deliberately spatially spread points, not random validation. Marginal prediction-interval overlap and corner envelopes are descriptive; neither is a confidence interval/test for temporal change.'},indent=2))
