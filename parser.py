# Importing the libararies
import kml2geojson
import json
import pprint
import gdaltools
import xml.etree.ElementTree as ET
from cluster import *


# Converting the kml file to GeoJSON
def convert_KML_2_GeoJSON(filename):
        print("[#] Converting KML to Geo JSON")

        # Defining the file name and its path.
        kml_file_with_path = 'kml_files/'+filename+'.kml'  

        # Inbuilt library function to convert the file. 
        kml2geojson.main.convert(kml_file_with_path, 'json_files')

        #Calling the next function  
        update_Geo_JSON(filename)

# Updating the GeoJSON file the processing the code
def update_Geo_JSON(filename):
    
        # Defining the file name and its path.
        geojson_file_with_path = 'json_files/'+filename+'.geojson'

        # Opening the file to modify it.
        with open(geojson_file_with_path, 'r+') as f:
                data = json.load(f)
                features = data["features"]

                print("[#] Updating Geo JSON")
                for feature in features:

                        # Making the grid opaque to color it. 
                        feature["properties"]["fill-opacity"] = "1.0"

                        # Making the uniform tree for further processing
                        if(feature["geometry"]["type"] == "Polygon"):
                                feature["geometry"]["type"] = "GeometryCollection"
                                feature["geometry"]["geometries"] = []
                                feature["geometry"]["geometries"].append(
                                        {"type": "Polygon", "coordinates": feature["geometry"]["coordinates"]})
                                del feature["geometry"]["coordinates"]

                # Preffing the JSON and saving it.
                print("[#] Prettify Geo JSON")
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        
        #Calling the next function  
        convert_GeoJSON_2_kml(filename)

# Converting the updated GeoJSON to KML file
def convert_GeoJSON_2_kml(filename):
        print("[#] Converting Geo JSON to KML")

        # Reading and saving a copy of KML file in respective locations 
        ogr = gdaltools.ogr2ogr()
        ogr.set_encoding("UTF-8")
        updated_kml_file_with_path = 'kml_files/'+'updated_'+filename+'.kml'
        geojson_file_with_path = 'json_files/'+filename+'.geojson'
        ogr.set_input(geojson_file_with_path, srs="EPSG:4326")
        ogr.set_output(updated_kml_file_with_path)
        ogr.execute()

        # Coloring the KML file using XML Element Tree
        modify_kml_according_to_clusters(updated_kml_file_with_path)

        # Further function can be called here for further changes in updated KML file 

# Coloring the grid according to the cluster they lie
def modify_kml_according_to_clusters(updated_kml_file_with_path):

        print("[#] Assigning colors to grids")

        # Color Array in hex format for KML grid color
        colorArray = ['7dff0000', '7d0000ff','7d00ff00', '7dffffff', '7d234131']

        # Respective Id's for style element
        colorArrayId = ['transBluePoly','transRedPoly','transGreenPoly','transBlackPoly','transRandomPoly']

        # Modifing the KML file according to clusters
        tree = ET.parse(updated_kml_file_with_path)
        root = tree.getroot()
        documentTag = root[0]
        folderTag = documentTag[1]
        
        # Child is placemark Tag
        total_folder_tags = len(folderTag)

        # y is dictionary of clusters
        y=get_dict()
        
        for i in range(len(y)):

                # Making the ref for Style tag
                colorId = '#'+colorArrayId[i]

                # Generating the Style tag for each cluster 
                style = ET.SubElement(documentTag, 'Style')
                style.set('id',colorArrayId[i])
                polystyle = ET.SubElement(style, 'PolyStyle')
                color = ET.SubElement(polystyle, 'color')
                color.text=colorArray[i]

                # Looping thorough the Cluster
                for j in y[i]:
                        count =0
                        for child in folderTag:
                                count = count +1
                                if count < total_folder_tags:
                                        
                                        # Coloring the grids according to the cluster in which they lie 
                                        if(folderTag[count][0].text == j):
                                                styleUrl = ET.SubElement(child, 'styleUrl')
                                                styleUrl.text = colorId

        # Writing the updated version of KMl file  
        tree.write(updated_kml_file_with_path)
        print("[#] Grids are now colored")


# Define your file name here without any extension
filename = '3G_mumbai_grid_WK18'

# Function called to convert the file
convert_KML_2_GeoJSON(filename)
