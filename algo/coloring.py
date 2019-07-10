"""Coloring the KML file on the basis of clusters of geo-grids on google maps"""

import sys
import seaborn as sns

from .cluster import (get_dict, Logic)
from collections import OrderedDict

class ColorKML:
    def __init__(self, params, logger=None, logic=None, process=False):
        """Initialise attributes:
        @params: params (dict): kml_file_path (str): file path of kml geo-location file
                                                        data_file_path (str): file path of data in excel format
                                                        number_of_clusters (int): number of clusters to be needed (for clustering)

                         logger (object): Logger object for logs
                         logic (object): Logic object for dataframe query support
                         process (bool): Tells where should the algorithm be run and file be saved without a manual function call

        if process=True: Run the code and save the output kml file in apt directory
        """

        self.kml_file_path = params["kml_file_path"]
        self.data_file_path = params["data_file_path"]
        self.number_of_clusters = params["number_of_clusters"]

        self.logger = logger
        self.logic = logic

        self.logger.info(
            "[*] Running ColorKML class with process=True \n {}".format(str(self.__repr__)))
        self.out_kml_file_path = "./outfiles/" + "updated_" + \
            params["kml_file_path"].rsplit("/", 1)[1]

        if process:
            self.logger.info("[*] Coloring the map:")
            self.__perform_coloring__(self.kml_file_path)
            self.color_the_clusters()
            string = ""
            for key in self.biglist:
                string += "\n".join(self.biglist[key])
                string += "\n"

            self.logger.info(
                "[*] Saving the output file with name: {}".format(self.out_kml_file_path))
            self.save_file(string, self.out_kml_file_path)

    def get_saved_outfile_name(self):
        """return a string that would be the output file name as `updated_` + KML input file name"""

        return "updated_" + self.kml_file_path.rsplit("/", 1)[1]

    def __repr__(self):
        """__repr__ of the object"""

        string = "\n"
        string += "[*] KML-Layer file path: {}\n".format(
            str(self.kml_file_path))
        string += "[*] Data file path: {}\n".format(str(self.data_file_path))
        return string

    def __perform_coloring__(self, file_name):
        """ Divide the kml content string into a list of strings for different grids
                @params: `file_name`: KML file path

                Note: private attribute
        """

        with open(file_name, 'r') as f:
            content = f.readlines()

        content = ("".join(content)).split("\n")

        biglist = OrderedDict()
        smollist = []

        temp_key = 'no_name'
        for i in content:
            if i.find('<description>') == -1:
                pass
            else:
                biglist[temp_key] = smollist
                temp_key = (i.split("<description>")[1]).split(
                    "</description>")[0]

                smollist = []
            smollist.append(i)
        biglist["last_name"] = smollist

        self.biglist = biglist

    def __color_argb_list_to_hex__(self, list_argb):
        """ convert a color given in argb (list) format to hex
                Note: private attribute
        """

        hexcolor = ""
        for i in list_argb:
            j = int(round(i * 255))
            hexcolor += (j).to_bytes(1, byteorder='big').hex().upper()

        return hexcolor

    def color_the_clusters(self):
        """On the basis of clusters of geo-grids taken from `get_dict` in cluster module, colorize the kml string."""

        data_frame = self.logic.get_data_frame()
        cluster_dict, weight_dict = get_dict(
            data_frame, self.number_of_clusters)

        self.logger.debug("[.] Using red-shade palette")
        temp = sns.dark_palette(
            "red",
            n_colors=self.number_of_clusters,
            reverse=True)
        # temp = sns.cubehelix_palette(n_colors=self.number_of_clusters, reverse=True)
        color_palettes = [
            self.__color_argb_list_to_hex__(
                list(x)) for x in temp]

        for i, key in enumerate(cluster_dict):
            for block in cluster_dict[key]:
                self.color_the_block(block, color_palettes[i])

        return True

    def color_the_block(self, block, color):
        """Add color tag in a styled line description of KML: Color a KML grid block
        @params: `block`: block number in grid e.g. A34, BF5
                         `color`: color in 4-hex format: FF001122 (alpha-r-g-b)
        """

        try:
            for idx, i in enumerate(self.biglist[block]):
                if i.find("</fill>") != -1:
                    j = i.split("</fill>")
                    j[0] = j[0][:-1] + "1"
                    j[1] = "<color>{c}</color>".format(c=color) + j[1]
                    j = "</fill>".join(j)

                    self.biglist[block][idx] = j
                    break

        except Exception as e:
            self.logger.critical("[!] Exception Occured: {}".format(e))
            return False

        return True

    def save_file(self, kml_string, out_file_name):
        """Give content in string and out file name, save the file
        @params: `kml_string`: kml data in string format
                         `out_file_name`: output kml file name
        """

        if (out_file_name.rsplit(".", 1)[1]).lower() != 'kml':
            out_file_name += ".kml"

        try:
            with open(out_file_name, 'w') as f:
                f.write(kml_string)
        except Exception as e:
            self.logger.critical("[!] Exception Occured: {}".format(e))
            return False
        return True
