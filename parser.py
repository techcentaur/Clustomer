import kml2geojson
import json
import pprint

kml2geojson.main.convert('tets.kml', 'json_files')
pp = pprint.PrettyPrinter(indent=4)


with open('json_files/tets.geojson', 'r+') as f:
    data = json.load(f)
    features = data["features"]
    n = len(features)

    for feature in features:
        feature["properties"]["stroke"] =  "#000000"
        feature["properties"]["fill-opacity"] =  "1.0"

    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()
# pp.pprint(features)