import xml.etree.cElementTree as ET
from collections import defaultdict
from config import *
import re

"""
The purpose of map_cleaning.py is to take the dictionary values created from the audit file .
The audit file creates a dictionary of node values that are valid streets. The below functions
will apply "cleaning" functions to the values in the dictionary. For example, adding "Road" to 
a street name when that term is missing or expanding "St." to "Street".
"""

#create empty dictionary for below functions
corrected_names = {}   

#the regex pattern to match against street names
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)

"""
This is a list of what we want to see as the last word on a street name.
If a value is comparted against expected_values and a value is missing, it will be 
placed into a dictionary.
"""

expected_values = ['Avenue', 'Alley', 'Road', 'Street', 'Trail', 'Landing', 'Pointe', 'Vista', 'Woods', 'Curve', 'Path', 'Freeway', 'Grotto', 'Court', 'Northbound', 'Southbound', 'Drive', 'Boulevard', 'Lane', 'Circle', 'Highway', 'Place', 'Loop', 'Terrace', 'Way', 'Crest', 'Parkway', 'Point', 'View', 'Commons', 'Run', 'South', 'North', 'East', 'Circus', 'Summit', 'West', '99E', '224', '213', 'View', '212', 'Downs']

"""
This maps an incorrect abbreviation to its expanded version. This dictionary will be used
to correct errors in the OSM map file.
"""


abbr_mapping = {'Ave': 'Avenue',
                'TRL': 'Trail',
                'Hwy': 'Highway',
                'Rd': 'Road',
                'Ave': 'Avenue',
                'Ct': 'Court',
                'Dr': 'Drive',
                'Pl': 'Place',
                'place': 'Place',
                'Pkwy': 'Parkway',
                'rd.': 'Road',
                'Sq.': 'Square',
                'St': 'Street',
                'st': 'Street',
                'ST': 'Street',
                'St,': 'Street',
                'St.': 'Street',
                'street': 'Street',
                'Street.': 'Street'
                }

"""
These are specific values that have been discovered with the audit function.
They will be one-to-one replacements of the incorrect value.
"""

spelling_fix = { 
                'Falstaff': 'Falstaff Road',
                'Pimlico': 'Pimlico Drive',
                'Hotspur': 'Hotspur Road',
                'Pericles': 'Pericles Loop',
                'El Greco': 'El Greco Street',
                '8202 SE Flavel St, Portland, OR 97266': 'SE Flavel Street',
                'Cervantes': 'Cervantes Street',
                'Touchstone': 'Touchstone Road',
                'Polonius': 'Polonius Street',
                'Spinosa': 'Spinosa Road',
                'Boticelli': 'Boticelli Street',
                'Southwest Wheatland': 'Southwest Wheatland Road',
                'Hotspur': 'Hotspur Road',
                'Southwest Miami': 'Southwest Miami Street',
                'Wheatherstone': 'Wheatherstone Street',
                'Southeast Fieldcrest': 'Southeast Fieldcrest Road'    
               }

def is_street_name(elem):
    #Checks to see if the tag value that we are looking at is a street and not anything else
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def print_sorted_dict(d, expression):
    """
    This function will be called on by clean_map(). Its purpose is
    to sort the streets that were corrected alphabetically to aid
    in readabilitiy.
    """
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print (expression % (k, v))

def update_name(name):
    
    """
    This function iteratively tests to see if the last characters of a street name match
    what is in the abbr_mapping dictionary. If it is, it pulls the corrected value from 
    the dictionary to replace the incorrect value. For example, replaces "Rd." with "Road".
    If a street name does not match against abbr_mapping, the below elif
    statements check to see if the street name matches against the spelling_fix dictionary.
    If a match is found, the name is replaced with the corrected name. If no match is found, the 
    name of the street returns unchanged.
    """
    
    street_type = name.split(' ')[-1]
    street_name = name.rsplit(' ', 1)[0]
    if street_type in abbr_mapping:
        name = street_name + ' ' + abbr_mapping[street_type]
    elif street_type in spelling_fix:
        if 'Falstaff' in street_name:
            name = 'Falstaff Road'
        elif 'Pimlico' in street_name:
            name = 'Pimlico Drive'
        elif 'Hotspur' in street_name:
            name = 'Hostspur Road'
        elif 'Pericles' in street_name:
            name = 'Pericles Loop'
        elif 'Polonius' in street_name:
            name = 'Polonius Loop'
        elif 'El Greco' in street_name:
            name = 'El Greco Street'
        elif '8202 SE Flavel St, Portland, OR 97266' in street_name:
            name = 'SE Flavel Street'
        elif 'Cervantes' in street_name:
            name = 'Cervantes Street'
        elif 'Touchstone' in street_name:
            name = 'Touchstone Road'
        elif 'Spinosa' in street_name:
            name = 'Spinosa Road'            
    return name    

def audit_abbreviations(filename):
    
    """
    This function audits to see if a street name value matches against the
    expected_street_type dictionary. It adds the incorrect value to a dictionary
    and returns the dictionary full of incorrect values.
    """
    
    problem_street_types = defaultdict(set)
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            expected_street_type(problem_street_types, elem.attrib['v'])
    return problem_street_types

def expected_street_type(street_types, street_name):
    
    """
    If a match is found against the street_type_re regex pattern, this function
    adds to teh street_types dictionary values that are not in expected_values.
    """
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_values:
            street_types[street_type].add(street_name)

def run_updates(filename):

    """
    This function returns corrected_names. corrected_names is iteratively added to 
    by matching to see if there is a better name. If better_name is not in corrected_names, 
    it is added to that dictionary.
    """
    
    st_types = audit_abbreviations(osmfile)
    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name)
            if better_name != name:
                corrected_names[name] = better_name
    return corrected_names

def clean_map(osmfile):
    
    """
    This function sorts the expected_values dictionary alphabetically for readabilitiy.
    It also prints the corrected_names and matches each name against their incorrect value 
    so it's easy to see what was changed.
    
    For example, if "Main St." was the incorrect name, you
    will see this output: "Main St.: Main Street".
    """
    
    global expected_values
    expected_values = sorted(expected_values)
    corrected_names = run_updates(osmfile)
    return print_sorted_dict(corrected_names, "%s: %s")

