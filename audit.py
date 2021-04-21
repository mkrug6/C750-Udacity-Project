import re
from collections import defaultdict
import xml.etree.cElementTree as ET

osmfile = 'wlinn'

# Setting global variables and values
street_types = defaultdict(int)
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)

def check_street_types(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1

def print_sorted_dictionary(d, expresssion):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print (expression % (k, v))
        
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def check(filename):
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            check_street_types(street_types, elem.attrib['v'])
    print(street_types, "%s: %d")
    return(street_types)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit(filename):
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])
    print(street_types, "%s: %d")
    return(street_types)

every_type = check(osmfile)
every_type

all_types = audit(osmfile)
all_types