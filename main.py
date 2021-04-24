from map_cleaning import *
from audit import *
from create_csvs import *
from theschema import *
import re

mapfile = osmfile
expression = ""


#Runs the main function in audit.py
audit(mapfile)

#Runs the main function in map_cleaning.py
clean_map(mapfile)

#Makes the CSV files
process_map(osmfile, validate=False)
