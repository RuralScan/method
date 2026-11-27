"""Read-only Haiti support checks; retain masks, do not infer absence."""
import ee,json
from pathlib import Path
ee.Initialize();ee.data.setDeadline(60000)
root=Path(__file__).resolve().parent
region=ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017').filter(ee.Filter.eq('country_na','Haiti')).geometry()
c=ee.ImageCollection('FAO/GHG/1/DROSA_A').filterDate('2018-01-01','2019-01-01')
out={'boundary':'USDOS/LSIB_SIMPLE/2017; country_na=Haiti','fao_images_2018':c.aggregate_array('system:id').getInfo(),'results':[]}
for label,img in [('FAO_2018',ee.Image(c.first())),('GPD_2022',ee.Image('projects/sat-io/open-datasets/GLOBAL-PEATLAND-DATABASE'))]:
 info=img.getInfo();proj=img.select(0).projection().getInfo();kw={'geometry':region,'crs':proj['crs'],'crsTransform':proj['transform'],'maxPixels':1000000}
 rec={'label':label,'metadata':info,'projection':proj,'unmasked_counts':img.reduceRegion(ee.Reducer.count(),**kw).getInfo(),'positive_cell_counts':img.gt(0).reduceRegion(ee.Reducer.sum().unweighted(),**kw).getInfo(),'native_grid_cell_count':ee.Image.constant(1).reduceRegion(ee.Reducer.count(),**kw).getInfo()}
 if label=='GPD_2022':rec['value_histogram']=img.reduceRegion(ee.Reducer.frequencyHistogram().unweighted(),**kw).getInfo()
 else:rec['sum_raw_hectares']=img.reduceRegion(ee.Reducer.sum().unweighted(),**kw).getInfo()
 out['results'].append(rec);print(json.dumps({k:v for k,v in rec.items() if k!='metadata'},indent=2),flush=True)
 (root/'drainage_checks.json').write_text(json.dumps(out,indent=2))
