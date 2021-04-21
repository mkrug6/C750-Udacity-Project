import re

lowercase = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
uppercase = re.compile(r'^([A-Z]|_)*$')
upper_colon = re.compile(r'^([A-Z]|_)*:([a-z]|_)*$')
problem = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

"""
    This funtion will create a dictionary telling us how many entries in the
    dataset contain all lower case for "k=" values, all uppercase, if the "k="
    value contains any problem characters, values with either all lower or all
    upper with at least 1 colon, or if there are any characters not
    convered in the REGEX
"""

def k_type(element, key):
            
        if element.tag == 'tag': #find only elements named tag
            
            if lowercase.search(element.attrib['k']): #finds the "k" value in the tag
                key['lowercase'] +=1
            elif lower_colon.search(element.attrib['k']):
                key['lower_colon'] +=1
            elif uppercase.search(element.attrib['k']):
                key['uppercase'] +=1
            elif upper_colon.search(element.attrib['k']):
                key['upper_colon'] +=1
            elif problem.search(element.attrib['k']):
                key['problem'] += 1
            else:
                key['other'] += 1
        return key


"""This fuction will parse through an XML file (the OSM file) and will
    execute the above function to count the different types of k values 
    that we have.
"""

def process_tag(filename):
    
    # sets the key variable with 0 in all indexes
    key = {"lowercase": 0, "lower_colon": 0, "uppercase": 0, "upper_colon": 0, "problem": 0, "other": 0} 
    
    for _, element in ET.iterparse(filename):
        key = k_type(element, key)
        
    return key

tag_dictionary = process_tag(osmfile)
print (tag_dictionary)


from collections import defaultdict

#we are using defaultdict incase we access a key that doesn't exist yet

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

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
    
every_type = check(osmfile)
every_type

from collections import defaultdict

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1

def print_sorted_dict(d, expression):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print (expression % (k, v))

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit(filename):
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])
    print(street_types, "%s: %d")
    return(street_types)

all_types = audit(osmfile)
all_types


