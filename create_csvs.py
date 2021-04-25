import csv
import codecs
import re
import xml.etree.cElementTree as ET
from schema import *
from config import *
import cerberus

"""
This purpose of this file is to create the CSV files that will later be imported
into the SQLite database. It takes the values from the corrected_names dictionary that was
created from map_cleaning.py and uses the corrected value to create XML tags for 
our CSV files. These CSV files will later be used to create the SQLite database.
"""

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def correct_element(v):
    """
    The purpose of this is to check and see if a value has been corrected.
    If the value has been corrected, it will insert the corrected name
    instead of the incorrect name.
    """
    
    if v in corrected_names:
        correct_value = corrected_names[v]
    else:
        correct_value = v
    return correct_value

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    #creates the node tags in the CSV file
    if element.tag == 'node':
        node_attribs['id'] = element.attrib['id']
        node_attribs['user'] = element.attrib['user']
        node_attribs['uid'] = element.attrib['uid']
        node_attribs['version'] = element.attrib['version']
        node_attribs['lat'] = element.attrib['lat']
        node_attribs['lon'] = element.attrib['lon']
        node_attribs['timestamp'] = element.attrib['timestamp']
        node_attribs['changeset'] = element.attrib['changeset']
        
        #creates the sub tags within the node element
        for node in element:
            tag_dict = {}
            tag_dict['id'] = element.attrib['id']
            if ':' in node.attrib['k']:
                tag_dict['type'] = node.attrib['k'].split(':', 1)[0]
                tag_dict['key'] = node.attrib['k'].split(':', 1)[-1]
                tag_dict['value'] = correct_element(node.attrib['v'])
            else:
                tag_dict['type'] = 'regular'
                tag_dict['key'] = node.attrib['k']
                tag_dict['value'] = correct_element(node.attrib['v'])
            tags.append(tag_dict)
    #creates the way tags       
    elif element.tag == 'way':
        way_attribs['id'] = element.attrib['id']
        way_attribs['user'] = element.attrib['user']
        way_attribs['uid'] = element.attrib['uid']
        way_attribs['version'] = element.attrib['version']
        way_attribs['timestamp'] = element.attrib['timestamp']
        way_attribs['changeset'] = element.attrib['changeset']
        n = 0
        for node in element:
            if node.tag == 'nd':
                way_dict = {}
                way_dict['id'] = element.attrib['id']
                way_dict['node_id'] = node.attrib['ref']
                way_dict['position'] = n
                n += 1
                way_nodes.append(way_dict)
            if node.tag == 'tag':
                tag_dict = {}
                tag_dict['id'] = element.attrib['id']
                if ':' in node.attrib['k']:
                    tag_dict['type'] = node.attrib['k'].split(':', 1)[0]
                    tag_dict['key'] = node.attrib['k'].split(':', 1)[-1]
                    tag_dict['value'] = correct_element(node.attrib['v'])
                else:
                    tag_dict['type'] = 'regular'
                    tag_dict['key'] = node.attrib['k']
                    tag_dict['value'] = correct_element(node.attrib['v'])
                tags.append(tag_dict)
    
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def validate_element(element, validator, schema=theschema):

    """
        Raise ValidationError if element does not match schema.
        Note that setting validate to true will significantly 
        increase the time to process the map file.
    """
    
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# ================================================== #
#               Main Function                        #
# ================================================== #

def process_map(file_in, validate):
    
    """
    Iteratively process each XML element and write to csv files.
    This is the function that actually writes to the files using the above helper
    functions.
    """

    with codecs.open(NODES_PATH, 'w', encoding="utf-8") as nodes_file, \
    codecs.open(NODE_TAGS_PATH, 'w', encoding="utf-8") as nodes_tags_file, \
    codecs.open(WAYS_PATH, 'w', encoding="utf-8") as ways_file, \
    codecs.open(WAY_NODES_PATH, 'w', encoding="utf-8") as way_nodes_file, \
    codecs.open(WAY_TAGS_PATH, 'w', encoding="utf-8") as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow((el['way']))
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
                    
