# Importing the libararies
import kml2geojson
import json
import pprint
import gdaltools

pp = pprint.PrettyPrinter(indent=4)

# Converting the kml file to GeoJSON
print("Converting KML to Geo JSON")
kml2geojson.main.convert('kml_files/3G_mumbai_grid_WK18.kml', 'json_files')

# Updating the GeoJSON file the preffiing the code
with open('json_files/3G_mumbai_grid_WK18.geojson', 'r+') as f:
    data = json.load(f)
    features = data["features"]
    n = len(features)

    print("Updating Geo JSON")
    for feature in features:
        feature["properties"]["stroke"] =  "#0000ff"
        feature["properties"]["fill-opacity"] =  "1.0"

    print("Prettify Geo JSON")
    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()

# Converting the updated JSON to KML file 
print("Converting Geo JSON to KML")
ogr = gdaltools.ogr2ogr()
ogr.set_encoding("UTF-8")
ogr.set_input("json_files/3G_mumbai_grid_WK18.geojson", srs="EPSG:4326")
ogr.set_output("kml_files/updated_3G_mumbai_grid_WK18.kml")
ogr.execute()