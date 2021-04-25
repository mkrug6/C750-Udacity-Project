from map_cleaning import *
from audit import audit
from create_csvs import *
from config import *
import re


#Runs the audit function in audit.py
audit(osmfile)

#Runs the main function in map_cleaning.py
clean_map(osmfile)

#Makes the CSV files from create_csvs.py
process_map(osmfile, validate=False)
