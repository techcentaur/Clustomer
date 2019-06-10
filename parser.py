# Importing the libararies
import kml2geojson
import json
import pprint
import gdaltools
import xml.etree.ElementTree as ET

# Converting the kml file to GeoJSON
def convert_KML_2_GeoJSON(filename):
    print("Converting KML to Geo JSON")
    kml_file_with_path = 'kml_files/'+filename+'.kml'
    kml2geojson.main.convert(kml_file_with_path, 'json_files')
    update_Geo_JSON(filename)


def update_Geo_JSON(filename):
    # Updating the GeoJSON file the processing the code
    geojson_file_with_path = 'json_files/'+filename+'.geojson'
    with open(geojson_file_with_path, 'r+') as f:
        data = json.load(f)
        features = data["features"]

        print("Updating Geo JSON")
        for feature in features:
            # Add your cluster condition here
            # call your property by feature["properties"]["description"] 
            feature["properties"]["stroke"] =  "7dff0000"
            # Condition ends here
            feature["properties"]["fill-opacity"] =  "1.0"
            if(feature["geometry"]["type"]=="Polygon"):
                feature["geometry"]["type"]="GeometryCollection"
                feature["geometry"]["geometries"]=[]
                feature["geometry"]["geometries"].append({"type": "Polygon","coordinates": feature["geometry"]["coordinates"]})
                del feature["geometry"]["coordinates"]
            

        print("Prettify Geo JSON")
        f.seek(0)        
        json.dump(data, f, indent=4)
        f.truncate()
        convert_GeoJSON_2_kml(filename)

# Converting the updated JSON to KML file 
def convert_GeoJSON_2_kml(filename):
        print("Converting Geo JSON to KML")
        ogr = gdaltools.ogr2ogr()
        ogr.set_encoding("UTF-8")

        updated_kml_file_with_path = 'kml_files/'+'updated_'+filename+'.kml'

        geojson_file_with_path = 'json_files/'+filename+'.geojson'

        ogr.set_input(geojson_file_with_path, srs="EPSG:4326")
        ogr.set_output(updated_kml_file_with_path)
        ogr.execute()
        tree = ET.parse(updated_kml_file_with_path)
        root = tree.getroot()
        folder = root[0][1]
        document = root[0]
        style = ET.SubElement(document, 'Style')
        style.set('id',"transBluePoly")
        polystyle = ET.SubElement(style, 'PolyStyle')
        color = ET.SubElement(polystyle, 'color')
        color.text="7dff0000"
        for child in folder:
                styleUrl = ET.SubElement(child, 'styleUrl')
                styleUrl.text = "#transBluePoly"
        tree.write(updated_kml_file_with_path)

filename = '3G_mumbai_grid_WK18'

convert_KML_2_GeoJSON(filename)
    
        
