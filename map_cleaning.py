osmfile = 'wlinn_sample'

import xml.etree.cElementTree as ET

expected_values = ['Avenue', 'Alley', 'Road', 'Street', 'Trail', 'Landing', 'Pointe', 
                   'Vista', 'Woods', 'Curve', 'Path', 'Freeway', 'Grotto', 'Court', 
                   'Northbound', 'Southbound', 'Drive', 'Boulevard', 'Lane', 'Circle',
                   'Highway', 'Place', 'Loop', 'Terrace', 'Way', 'Crest', 'Parkway',
                   'Point']

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

typo_full_names = {}

def audit_street_name(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if (all_types[street_type] < 20) and (street_type not in expected_values) and (street_type not in abbr_mapping):
            if street_type in typo_full_names:
                typo_full_names[street_type].append(street_name)
            else:
                typo_full_names.update({ street_type:[street_name] })

def audit_name(filename):
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_name(street_types, elem.attrib['v'])    
    return typo_full_names

audit_name(osmfile)


expected_values.extend([
    'View', 'Commons', 'Run', 'South', 'North', 'East', 'Circus', 'Summit', 'West', 
    '99E', '224', '213', 'View', '212', 'Downs'
                       ])


name_fix = { 
                'Boticelli': 'Boticelli Street',
                'Southwest Wheatland': 'Southwest Wheatland Road',
                'Falstaff': 'Falstaff Road',
                'Pimlico': 'Pimlico Drive',
                'Hotspur': 'Hotspur Road',
                'Southwest Miami': 'Southwest Miami Street',
                'Pericles': 'Pericles Loop',
                'Polonius': 'Polonius Loop',
                'El Greco': 'El Greco Street',
                'Wheatherstone': 'Wheatherstone Street',
                '8202 SE Flavel St, Portland, OR 97266': 'SE Flavel Street',
                'Cervantes': 'Cervantes Street',
                'Touchstone': 'Touchstone Road',
                'Polonius': 'Polonius Street',
                'Spinosa': 'Spinosa Road',
                'Southeast Fieldcrest': 'Southeast Fieldcrest Road'
               }

spelling_fix = { 
                'Falstaff': 'Falstaff Road',
                'Pimlico': 'Pimlico Drive',
                'Hotspur': 'Hotspur Road',
                'Pericles': 'Pericles Loop',
                'Polonius': 'Polonius Loop',
                'El Greco': 'El Greco Street',
                '8202 SE Flavel St, Portland, OR 97266': 'SE Flavel Street',
                'Cervantes': 'Cervantes Street',
                'Touchstone': 'Touchstone Road',
                'Polonius': 'Polonius Street',
                'Spinosa': 'Spinosa Road',
               }

# Let's sort our expected variable to aid in readability

expected_values = sorted(expected_values)
expected_values


def update_name(name):
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
    problem_street_types = defaultdict(set)
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            expected_street_type(problem_street_types, elem.attrib['v'])
    return problem_street_types

def expected_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_values:
            street_types[street_type].add(street_name)

def run_updates(filename):
    st_types = audit_abbreviations(osmfile)
    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name)
            if better_name != name:
                corrected_names[name] = better_name
    return corrected_names
            
corrected_names = {}           
corrected_names = run_updates(osmfile)
print_sorted_dict(corrected_names, "%s: %s")
