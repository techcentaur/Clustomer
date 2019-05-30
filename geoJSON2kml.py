import gdaltools

ogr = gdaltools.ogr2ogr()
ogr.set_encoding("UTF-8")
ogr.set_input("json_files/tets.geojson", srs="EPSG:4326")
ogr.set_output("tet1s.kml")
ogr.execute()