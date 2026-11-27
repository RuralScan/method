"""Acquire bounded native Aqueduct vectors for Haiti; inspection, not runtime release."""
from pathlib import Path
import ee,json,hashlib,datetime,sys
p=Path(__file__).resolve().parent
boundary_path=Path(sys.argv[1]); boundary=json.loads(boundary_path.read_text())
ee.Initialize();ee.data.setDeadline(90000)
aoi=ee.FeatureCollection(boundary).geometry()
asset='WRI/Aqueduct_Water_Risk/V4/baseline_annual'
fc=ee.FeatureCollection(asset).filterBounds(aoi)
fields=['pfaf_id','aqid','string_id','gid_0','gid_1','bws_raw','bws_score','bws_cat','bws_label']
meta={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'asset':asset,'boundary_sha256':hashlib.sha256(boundary_path.read_bytes()).hexdigest(),'count':fc.size().getInfo(),'asset_metadata':ee.data.getAsset(asset)}
print('intersecting features',meta['count'],flush=True)
meta['all_property_names']=fc.first().propertyNames().getInfo()
(p/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
data=fc.select(fields).getInfo()
(p/'haiti_intersecting_native.geojson').write_text(json.dumps(data,indent=2)+'\n')
print('saved',len(data['features']),'features',flush=True)
