"""Helper classes for forming refrence frame and reading grid data from excel"""

import re
from collections import Counters


class ReferenceFrame:
    """Form relative refrence frame and co-ordinate structure of grid-like-data
    @params: rd is Data object (ReadData)
    """

    def __init__(self, rd):
        self.read_data = rd

        self.x_min = self.read_data.min_glob
        self.y_name_list = {}
        for idx, l in enumerate(rd.names_list):
            self.y_name_list[l] = idx

    def __str__(self):
        """string representation of class"""

        ret = "[*] Origin Refrences\n"
        ret += "[.] X-axis : -" + str(self.x_min) + "\n"
        ret += "[.] Y-axis : " + str(self.y_name_list) + "\n"
        return ret

    def get_coordinate(self, name):
        """get coordinate from the name of grid: G34 (e.g.)

        @params: `name`(str): Name of the grid of which you want to get coord and weight
        @return: As a tuple (x-coord, y-coord, weight)
        """

        tmp = re.split(r'(\d.*)', name)

        x = int(tmp[1]) - self.x_min
        y = self.y_name_list[tmp[0]]

        return {'x': x, 'y': y, 'w': self.read_data.__get_weight__(name)}

    def get_names_from_points(self, points):
        """Get a list of (x-coord, y-coord, weight) like (2, 12, 3.2) given a list of grid string point names (like G23)

        @params: `points` (list of str): List of grid string names
        @return: a list of tuples
        """

        is_list = isinstance(points, list)
        if not is_list:
            points = [points]

        inv_map = {v: k for k, v in self.y_name_list.items()}

        strs = []
        for p in points:
            string = "" + str(inv_map[round(p[1])])
            string += str(round(p[0] + self.x_min))
            strs.append(string)

        if not is_list:
            return strs[0]

        return strs


class ReadGridData:
    """Data read of data frame consisting grid as column
    ---
    @params: `data_frame` (pandas dataframe): Data in the pandas data structure
    ---
    Usable public attributes:

    `min_glob`(int):
    `names_list`: List of all possible names in Y-axis (Grid names)
    `c_grids`: Dict of (key, value): (grid, weight)
    `grid_list`: Dict of (key, value): (grid, weight) but sorted (with ordereddict)
    """

    def __init__(self, data_frame):
        # Getting the Grid column only form excel file
        val = list(data_frame['Grid'])

        # Filtering
        grids = []
        for l in val:
            if not isinstance(l, float):
                grids.append(l)

        # making the Dictionary of the number of occurances of grids
        c_grids = Counter(grids)
        grid_list = sorted(c_grids)

        len4 = []
        len3 = []

        for l in grid_list:
            if (len(l)) == 3:
                len3.append(l)
            else:
                len4.append(l)

        d3 = self.__max_and_min__(len3)
        d4 = self.__max_and_min__(len4)
        min_glob = min(d3['min'], d4['min'])

        self.min_glob = min_glob
        self.names_list = d3['names'] + d4['names']

        self.c_grids = c_grids
        self.grid_list = grid_list

    def __max_and_min__(self, _list):
        len3_new = []
        lister = []
        for l in _list:
            tmp = re.split(r'(\d.*)', l)
            len3_new.append(int(tmp[1]))
            lister.append(tmp[0])
        return {'max': (max(len3_new)), 'min': (min(len3_new)),
                'names': sorted(list(set(lister)))}

    def __get_weight__(self, name):
        return self.c_grids[name]


if __name__ == '__main__':
    # example usage

    rd = ReadGridData("Book8.xlsx")
    rf = ReferenceFrame(rd)
    print(rf.get_coordinate('R22'))
