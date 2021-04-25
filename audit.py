import re
from collections import defaultdict
import xml.etree.cElementTree as ET
from config import *

#creates the dictionary street_types for the functions below
street_types = defaultdict(int)

#the regex expression to map against possibly invalid street names
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
 
def check_street_types(street_types, street_name):
    
    """
    Uses regex search pattern to increment the dictionary
    street_type up by 1 when a match is found.
    """
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1
  
def is_street_name(elem):
    
    """
    This functions finds the areas where a node has a tag with
    the value of "addr:street". If that value is found, the function
    returns true.
    """
    
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def check(filename):
    """
    The purpose of thsi is to check if there is a match in a nodes' street value
    against the dictionary of values that was created. If a match is found,
    it outputs the following:
        old_value: new_value
    If a match was found, street_types is returned
    """
    
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            check_street_types(street_types, elem.attrib['v'])
    print(street_types, "%s: %d")
    return(street_types)

def audit_street_type(street_types, street_name):
    
    """
    Uses regular expressions to search for specific patterns 
    found in street_type_re. If it mathces, it increments 
    the dictionary value up by 1.
    """
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1

def audit(filename):

    """
    This is the main audit function. The purpose of the audit function is to iteratively run 
    through the OSM file. It starts first by running the every_type function (see above).
    """

    every_type = check(osmfile)
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])
    return(street_types)
