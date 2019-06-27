# Importing the libararies
import json
import pprint
import gdaltools
import kml2geojson
import xml.etree.ElementTree as ET

import random

from .cluster import *

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
                kml2geojson.main.convert(self.kml_filepath, 'json_files')
                self.update_Geo_JSON()

        def update_Geo_JSON(self):
                """Updating the GeoJSON file the processing the code"""

                filename = self.kml_filepath.split(".")[-2]
                geojson_file_with_path = './json_files/' + filename + '.geojson'

                with open(geojson_file_with_path, 'r+') as f:
                        data = json.load(f)
                        features = data["features"]

                        # print("[*] Updating Geo JSON")
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
                        # print("[*] Prettify Geo JSON")
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()

                self.convert_GeoJSON_2_kml(filename)

        def convert_GeoJSON_2_kml(self, filename):
                """ Converting the updated GeoJSON to KML file """

                # print("[*] Converting Geo JSON to KML")

                # Reading and saving a copy of KML file in respective locations
                ogr = gdaltools.ogr2ogr()
                ogr.set_encoding("UTF-8")

                updated_kml_file_with_path = "output_"+filename+'.kml'
                geojson_file_with_path = 'json_files/'+filename+'.geojson'

                ogr.set_input(geojson_file_with_path, srs="EPSG:4326")
                ogr.set_output(updated_kml_file_with_path)
                ogr.execute()

                # Coloring the KML file using XML Element Tree
                # self.modify_kml_according_to_clusters(updated_kml_file_with_path)
                self.test_function(updated_kml_file_with_path)

        def modify_kml_according_to_clusters(self, updated_kml_file_with_path):
                """
                Coloring the grid according to the cluster they lie
                """

                r = lambda: random.randint(0, 255)

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
                        random_color = '%02X%02X%02X%02X' % (
                            r(), r(), r(), r())

                        # Making the ref for Style tag
                        colorId = '#'+random_color

                        # Generating the Style tag for each cluster
                        style = ET.SubElement(documentTag, 'Style')
                        style.set('id', random_color)
                        polystyle = ET.SubElement(style, 'PolyStyle')

                        color = ET.SubElement(polystyle, 'color')
                        color.text = random_color

                        # Looping thorough the Cluster
                        for j in y[i]:
                                count = 0
                                for child in folderTag:
                                        count = count + 1
                                        if count < total_folder_tags:
                                                # Coloring the grids according to the cluster in which they lie
                                                if(folderTag[count][0].text == j):
                                                        styleUrl = ET.SubElement(
                                                            child, 'styleUrl')
                                                        styleUrl.text = colorId

                # Writing the updated version of KMl file
                tree.write(updated_kml_file_with_path)
                # print("[*] Grids colored!\n")

                print(
                    "[*] Output file saved with name {}".format(updated_kml_file_with_path))

        def test_function(self, updated_kml_file_with_path):
                file_content = open(updated_kml_file_with_path, 'r')
                soup = BeautifulSoup(file_content, 'lxml')
                r = lambda: random.randint(0, 255)
                y = get_dict(self.xlsx_filepath, self.clusters)

                for i in range(len(y)):

                        random_color = '%02X%02X%02X%02X' % (r(), r(), r(), r())
                        random_color_id = "#"+random_color
                        schema_tag = soup.find('schema')
                        style_tag = soup.new_tag("Style") 
                        style_tag['id'] =  random_color
                        schema_tag.insert_after(style_tag)
                        style_tag_find = soup.find('Style')
                        polystyle_tag = soup.new_tag("PolyStyle") 
                        style_tag_find.insert(1,polystyle_tag)
                        polystyle_tag_find = soup.find('PolyStyle')
                        color_tag = soup.new_tag("color") 
                        color_tag.append(random_color)
                        polystyle_tag_find.insert(1,color_tag)

                        for j in y[i]:
                                for desc in soup.find_all('description'):
                                        if(desc.get_text() == j):
                                                style_url_tag = soup.new_tag("styleUrl")                       
                                                style_url_tag.append(random_color_id)
                                                desc.insert_after(style_url_tag)

                soup_string = str(soup.body.next)
                f = open("demofile2.kml", "w")
                f.write(soup_string)
                f.close()