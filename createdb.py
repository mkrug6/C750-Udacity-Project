import sqlite3 
import csv
from config import *

"""
The purpose of this file is to create and connect to a database instance using SQLite.
It drops the table if it already exists and then creates the table structure in accordance
with the CSV structure for easy importing.
"""

def create_connection():
    #Creates connection to the databse
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return

def drop_if_exists():

    #Creates connection to the databse
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    #If table already exists, drop it.
    c.execute('''DROP TABLE IF EXISTS nodes''')
    c.execute('''DROP TABLE IF EXISTS nodes_tags''')
    c.execute('''DROP TABLE IF EXISTS ways''')
    c.execute('''DROP TABLE IF EXISTS ways_tags''')
    c.execute('''DROP TABLE IF EXISTS ways_nodes''')
    conn.commit()
    return

def create_table_structure():

    #Creates connection to the databse
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    """
    This function creates the table scheme. We will use this as the template to
    insert our data from the CSV files we generated earlier.
    """
    
    #Creates the NODES table with appropriate columns and column types
    QUERY_NODES = """
    CREATE TABLE nodes (
        id INTEGER NOT NULL,
        lat REAL,
        lon REAL,
        user TEXT,
        uid INTEGER,
        version INTEGER,
        changeset INTEGER,
        timestamp TEXT
    );
    """
    
    #Creates the NODES_TAGS table with appropriate columns and column types
    QUERY_NODES_TAGS = """
    CREATE TABLE nodes_tags (
        id INTEGER,
        key TEXT,
        value TEXT,
        type TEXT,
        FOREIGN KEY (id) REFERENCES nodes(id)
    );
    """
    
    #Creates the WAYS table with appropriate columns and column types
    QUERY_WAYS = """
    CREATE TABLE ways (
        id INTEGER NOT NULL,
        user TEXT,
        uid INTEGER,
        version INTEGER,
        changeset INTEGER,
        timestamp TEXT
    );
    """
    
    #Creates the WAYS_TAGS table with appropriate columns and column types
    QUERY_WAYS_TAGS = """
    CREATE TABLE ways_tags (
        id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        type TEXT,
        FOREIGN KEY (id) REFERENCES ways(id)
    );
    """
    
    #Creates the WAYS_NODES table with appropriate columns and column types
    QUERY_WAYS_NODES = """
    CREATE TABLE ways_nodes (
        id INTEGER NOT NULL,
        node_id INTEGER NOT NULL,
        position INTEGER NOT NULL,
        FOREIGN KEY (id) REFERENCES ways(id),
        FOREIGN KEY (node_id) REFERENCES nodes(id)
    );
    """
    
    #execute the above commands in SQLite
    c.execute(QUERY_NODES)
    c.execute(QUERY_NODES_TAGS)
    c.execute(QUERY_WAYS)
    c.execute(QUERY_WAYS_TAGS)
    c.execute(QUERY_WAYS_NODES)

    #Commit the above changes
    conn.commit()
    return    

def import_csv_data():
    
    """
    This funtion actually inserts data from the CSV files into the database.
    This is the moment we've been waiting for.
    """
    
    #Creates connection to the databse
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    #These statements open the CSV files and prepares them for data insertion
    
    with open('nodes.csv','rt', encoding='utf-8') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db1 = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]
        
    with open('nodes_tags.csv','rt', encoding='utf-8') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db2 = [(i['id'], i['key'], i['value'], i['type']) for i in dr]
        
    with open('ways.csv','rt', encoding='utf-8') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db3 = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]
        
    with open('ways_tags.csv','rt', encoding='utf-8') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db4 = [(i['id'], i['key'], i['value'], i['type']) for i in dr]
        
    with open('ways_nodes.csv','rt', encoding='utf-8') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db5 = [(i['id'], i['node_id'], i['position']) for i in dr]

    #The below statements actually import the CSV data into the database
    
    c.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db1)
    c.executemany("INSERT INTO nodes_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_db2)
    c.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db3)
    c.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_db4)
    c.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db5)
    conn.commit()
    
    return

#Executes the above functions when called
def create_db():
    create_connection()
    drop_if_exists()
    create_table_structure()
    import_csv_data()
    return
    
