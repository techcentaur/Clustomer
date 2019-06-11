# Importing the libararies
import json
import pprint
import gdaltools
import kml2geojson
import xml.etree.ElementTree as ET

from cluster import *


class Parser:
        def __init__(self, params):
                """params dict:
                [kml_filepath, xlsx_filepath, outfile, cluster]
                """

                self.kml_filepath = params["kml_filepath"]
                self.xlsx_filepath = params["xlsx_filepath"]
                self.clusters = params["clusters"]
                
                self.convert_KML_2_GeoJSON()


        # Converting the kml file to GeoJSON
        def convert_KML_2_GeoJSON(self):
                print("[*] Converting KML to Geo-JSON")

                # Inbuilt library function to convert the file. 
                kml2geojson.main.convert(self.kml_filepath, 'json_files')
                self.update_Geo_JSON()


        def update_Geo_JSON(self):
                """Updating the GeoJSON file the processing the code"""
                
                filename = self.kml_filepath.split(".")[-2]
                geojson_file_with_path = './json_files/' + filename + '.geojson'

                with open(geojson_file_with_path, 'r+') as f:
                        data = json.load(f)
                        features = data["features"]

                        print("[*] Updating Geo JSON")
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
                        print("[*] Prettify Geo JSON")
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                
                self.convert_GeoJSON_2_kml(filename)

        def convert_GeoJSON_2_kml(self, filename):
                """ Converting the updated GeoJSON to KML file """
                
                print("[*] Converting Geo JSON to KML")

                # Reading and saving a copy of KML file in respective locations 
                ogr = gdaltools.ogr2ogr()
                ogr.set_encoding("UTF-8")

                updated_kml_file_with_path = 'kml_files/'+'updated_'+filename+'.kml'
                geojson_file_with_path = 'json_files/'+filename+'.geojson'
                
                ogr.set_input(geojson_file_with_path, srs="EPSG:4326")
                ogr.set_output(updated_kml_file_with_path)
                ogr.execute()

                # Coloring the KML file using XML Element Tree
                self.modify_kml_according_to_clusters(updated_kml_file_with_path)


        def modify_kml_according_to_clusters(self, updated_kml_file_with_path):
                """
                Coloring the grid according to the cluster they lie
                """

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
                y = get_dict(self.xlsx_filepath, self.clusters)
                
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
                print("[*] Grids are now colored")
