"""Inspect published Soil Revealed component assets without filling masks."""
import ee,json,hashlib
from pathlib import Path
ee.Initialize();ee.data.setDeadline(60000)
root=Path(__file__).resolve().parent
region=ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017').filter(ee.Filter.eq('country_na','Haiti')).geometry()
points_path=root.parent/'haiti-diagnostic-inputs-20261126/stratified_points.geojson'
points=json.loads(points_path.read_text());fc=ee.FeatureCollection([ee.Feature(ee.Geometry.Point(f['geometry']['coordinates']),dict(f['properties'],sample_id=f['id'])) for f in points['features']])
out={'source_commit':'9eb9e12a434d997edaacd52f935d0d5fe9a819d7','boundary':'USDOS/LSIB_SIMPLE/2017; Haiti','points_sha256':hashlib.sha256(points_path.read_bytes()).hexdigest(),'scenarios':[]}
images={}
for name in ['crop_MG','crop_I','crop_MGI']:
 asset='projects/soils-revealed-307010/assets/Future/scenario_'+name+'_dSOC'
 rec={'scenario':name,'collection':asset}
 try:
  c=ee.ImageCollection(asset);rec['image_ids']=c.aggregate_array('system:id').getInfo();rec['times']=c.aggregate_array('system:time_start').getInfo()
  print(name,'images',len(rec['image_ids']),flush=True)
  img=ee.Image(c.filterDate('2038-01-01','2039-01-01').first());rec['metadata']=img.getInfo();proj=img.select(0).projection().getInfo();rec['projection']=proj;images[name]=img
  kw={'geometry':region,'crs':proj['crs'],'crsTransform':proj['transform'],'maxPixels':10000000}
  rec['unmasked_counts']=img.reduceRegion(ee.Reducer.count(),**kw).getInfo()
  rec['positive_counts']=img.gt(0).reduceRegion(ee.Reducer.sum().unweighted(),**kw).getInfo()
  rec['zero_counts']=img.eq(0).reduceRegion(ee.Reducer.sum().unweighted(),**kw).getInfo()
  rec['negative_counts']=img.lt(0).reduceRegion(ee.Reducer.sum().unweighted(),**kw).getInfo()
  rec['range']=img.reduceRegion(ee.Reducer.minMax(),**kw).getInfo()
  samples=img.reduceRegions(collection=fc,reducer=ee.Reducer.first(),crs=proj['crs'],crsTransform=proj['transform']).getInfo()
  (root/(name+'_samples.json')).write_text(json.dumps(samples,indent=2))
  print(name,{k:rec[k] for k in ['unmasked_counts','positive_counts','zero_counts','negative_counts','range']},flush=True)
 except Exception as e:rec['error']=str(e);print(name,str(e)[:500],flush=True)
 out['scenarios'].append(rec);(root/'component_checks.json').write_text(json.dumps(out,indent=2))
if len(images)==3:
 d=images['crop_MGI'].subtract(images['crop_MG']).subtract(images['crop_I'])
 proj=images['crop_MGI'].projection().getInfo();kw={'geometry':region,'crs':proj['crs'],'crsTransform':proj['transform'],'maxPixels':10000000}
 out['combined_minus_sum']={'range':d.reduceRegion(ee.Reducer.minMax(),**kw).getInfo(),'valid':d.reduceRegion(ee.Reducer.count(),**kw).getInfo(),'nonzero':d.neq(0).reduceRegion(ee.Reducer.sum().unweighted(),**kw).getInfo()}
(root/'component_checks.json').write_text(json.dumps(out,indent=2))
