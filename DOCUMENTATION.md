# Documentation

## Scripts and Classes

### `cluster.py`
```python
"""Weighted Clustering Algorithm and Support for Logical Queries from Dataframe"""

class Cluster:
    """
    @params: n(int): Number of clusters to be formed
    """

    def get_points_from_names(self, rd, rf):
        """Get a list of points as a tuple of (x-cord, y-cord, weight) where x-cord and y-cord \
        are based on `rf` reference frame.
        With input as the grid_list public attribute from `rd` object.

        @params: rd (object): ReadGridData
                         rf (object): ReferenceFrame
        """
        pass


    def get_clusters(self, data):
        """	Run clustering algorithm and save the result in self as below written attributes.
            self.centroids: The last calculated centroids
            self.prev_clusters: The last formed clusters

            @params: data: List of all points in a format (x-cord, y-cord, weight) or as an output of public method of this class: `get_points_from_names()`
        """
        pass

        def weighted_distance(i, j):
            """ weighted distance: (((j[0] - i[0])**2 + (j[1] - i[1])**2)/(j[2] + i[2]))**0.5
                @params: i, j: tuples with (x-cord, y-cord, weight)
            """
            pass
        

class Logic:
    """Support wrapper for query logic from pandas dataframe"""

    def __init__(self, data_file_path, query, logger):
        """ Read excel data and set up self attributes

            @params: data_file_path: file path of the excel data file
                             query: query as a dict in particular format (look for app.py doc for more)
                             logger: logger object for logs
        """
     	pass


    def get_query_string(self, query):
        """ If the query is of type discrete convert it to a dataframe support query
                for e.g. [4, 5, 6] -> (col==4 | col==5 | col==6) for a column col

            @params: query: dict with column as keys
        """

  		pass


    def get_data_frame(self):
        """ @return: updated dataframe, based on `self.query`
                query type supported: time, date, discrete
        """
        pass
  

def get_dict(data_frame, no_of_clusters):
    """	Run clustering algorithm and get data in the form of dicts:

        1. Create ReadGridData and ReferenceFrame object with give dataframe as data
        2. Run `get_clusters` function from Cluster with the data
        3. Form ordered dict information from the calculated clusters

        @params:
        `data_frame` (pandas dataframe): Data
        `no_of_clusters` (int): No of clusters to be formed

        @return: (Both dicts are `OrderedDict`)
        `weight_dict`: weights of the centroids in decreasing order
        `dict_data`: corresponding grid names of the x, y coordinates
    """
    pass

```

### `coloring.py`
```python
"""Coloring the KML file on the basis of clusters of geo-grids on google maps"""

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
        pass


    def get_saved_outfile_name(self):
        """return a string that would be the output file name as `updated_` + KML input file name"""
        pass

    def __repr__(self):
        """__repr__ of the object"""
        pass

    def __perform_coloring__(self, file_name):
        """ Divide the kml content string into a list of strings for different grids
                @params: `file_name`: KML file path

                Note: private attribute
        """
        pass

    def __color_argb_list_to_hex__(self, list_argb):
        """ convert a color given in argb (list) format to hex
                Note: private attribute
        """
        pass

    def color_the_clusters(self):
        """On the basis of clusters of geo-grids taken from `get_dict` in cluster module, colorize the kml string."""
        pass


    def color_the_block(self, block, color):
        """Add color tag in a styled line description of KML: Color a KML grid block
        @params: `block`: block number in grid e.g. A34, BF5
                         `color`: color in 4-hex format: FF001122 (alpha-r-g-b)
        """
        pass

    def save_file(self, kml_string, out_file_name):
        """Give content in string and out file name, save the file
        @params: `kml_string`: kml data in string format
                         `out_file_name`: output kml file name
        """
        pass

```

### `github_wrapper.py`
```python
"""GitHub Wrapper for File Upload"""

def post_on_github(params, logger=None):
    """ Post a file on Github | API wrapper

    @params: params: A dictionary with these required keys:
            user: GitHub handle,
            password: Password without encryption,
            repo: Name of the repository,
            branch: Name of the branch (default is 'master')
            to_be_uploaded_file_list: List of files to be uploaded,
            commit_message: Message for the commit (default is a random message)

            logger: Logger object for logs
    """
    pass
```

### `script.py`
```python
"""Helper classes for forming refrence frame and reading grid data from excel"""


class ReferenceFrame:
    """Form relative refrence frame and co-ordinate structure of grid-like-data
    @params: rd is Data object (ReadData)
    """

    def __str__(self):
        """string representation of class"""
        pass

    def get_coordinate(self, name):
        """get coordinate from the name of grid: G34 (e.g.)

        @params: `name`(str): Name of the grid of which you want to get coord and weight
        @return: As a tuple (x-coord, y-coord, weight)
        """
        pass

    def get_names_from_points(self, points):
        """Get a list of (x-coord, y-coord, weight) like (2, 12, 3.2) given a list of grid string point names (like G23)

        @params: `points` (list of str): List of grid string names
        @return: a list of tuples
        """
        pass


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
    pass
```

## Methods and Routes of Web-Application

```python
@app.route('/', methods=["POST", "GET"])
def upload_file():
    """Home route:
    @utilities:
    1. Upload new data and kml base file
    2. Select data and kml base file from already uploaded file
    3. Select already analysed updated kml file
    """


@app.route('/select/<filename>', methods=['GET', 'POST'])
def select_content(filename):
    """Select column from filename route:
    @utilities:
    1. Select a new grid column 'Grid' selected by-default
    2. Select a new column on basis of which the data will be analysed
    """
    pass


@app.route('/select/<filename>/<grid>/<col>/', methods=['POST', 'GET'])
def select_values(filename, grid, col):
    """Select value(s) route:
    @utilities:
    1. Select value(s) from a particular column
    2. Input number of clusters to needed (main call to clustering algorithm exists here)
    """
    pass

@app.route('/result_page/<out_file_name>', methods=["GET"])
def result_page(out_file_name):
    """Display result route
    @utilites:
    1. Save the new and updated KML file in database
    2. Download the new and updated KML file
    3. View the KML file in Google Maps
    """
    pass

@app.route('/kml_viewer/<out_file_name>', methods=["GET"])
def show_kml(out_file_name):
    """View KML route: File in Google MAP with public url of kml data by-passing through github raw user content
    @utilites:
    1. Show KML in Google MAPs
    2. Save the KML file in database
    """
    pass
```