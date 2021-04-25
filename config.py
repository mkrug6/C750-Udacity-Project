#The map file to use
osmfile = "wlinn_sample"

#The SQLite database name. Used in createdb.py
sqlite_file = 'wlinn.db'

#Here you can change what you want your CSV files to be named
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

#If you are using the sample_generator tool, this is where you name the output sample file
SAMPLE_FILE = "wlinn_sample"

""" It is recommended not to make changes to this. If you do, you must make
    corresponding changes to the schema table. The order of the fields here
    and quantity must match the order in the sql scheme table in schema.py.
"""
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

"""
This is a list of what should be expected to be on the end of the "v" tag for when the node is a street.
This is used in clean_map() from map_cleaning.py
If anymore street types exist, please let me know. This is an exhaustive list.
"""
expected_values = ['Avenue', 'Alley', 'Road', 'Street', 'Trail', 'Landing', 'Pointe', 'Vista', 'Woods', 'Curve', 'Path', 'Freeway', 'Grotto', 'Court', 'Northbound', 'Southbound', 'Drive', 'Boulevard', 'Lane', 'Circle', 'Highway', 'Place', 'Loop', 'Terrace', 'Way', 'Crest', 'Parkway', 'Point', 'View', 'Commons', 'Run', 'South', 'North', 'East', 'Circus', 'Summit', 'West', '99E', '224', '213', 'View', '212', 'Downs']

"""
Creates an empy dictionary. This dictionary will be filled by map_cleaning.py
and will be used to create CSV files with the create_csvs.py file.
"""
corrected_names = {} 
