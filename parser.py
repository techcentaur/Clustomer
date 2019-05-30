import kml2geojson
import json
import pprint
import gdaltools

kml2geojson.main.convert('kml_files/3G_mumbai_grid_WK18.kml', 'json_files')
pp = pprint.PrettyPrinter(indent=4)


with open('json_files/3G_mumbai_grid_WK18.geojson', 'r+') as f:
    data = json.load(f)
    features = data["features"]
    n = len(features)

    for feature in features:
        feature["properties"]["stroke"] =  "#0000ff"
        feature["properties"]["fill-opacity"] =  "1.0"

    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()


ogr = gdaltools.ogr2ogr()
ogr.set_encoding("UTF-8")
ogr.set_input("json_files/3G_mumbai_grid_WK18.geojson", srs="EPSG:4326")
ogr.set_output("kml_files/updated_3G_mumbai_grid_WK18.kml")
ogr.execute()