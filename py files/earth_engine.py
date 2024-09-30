import ee
import google.auth
import sys
import json

def main(latitude, longitude):
    credentials, project = google.auth.default()
    ee.Initialize(credentials, project=project)

    point = ee.Geometry.Point([longitude, latitude])

    landsatSR = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
        .filterBounds(point) \
        .filterDate('2021-01-01', '2021-12-31') \
        .sort('CLOUD_COVER') \
        .first()

    if landsatSR:
        SRbands = landsatSR.select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6','SR_B7','ST_B10'])

        SRvalue = SRbands.reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=30)

        print(json.dumps(SRvalue.getInfo()))
    else:
        print(json.dumps({'error': 'No Landsat Surface Reflectance image found for the given location and date.'}))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python earth_engine.py <latitude> <longitude>")
        sys.exit(1)

    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    main(latitude, longitude)