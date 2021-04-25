# A case study of data wrangling using the City of West Linn, Oregon with Open Street Map data

## How to run and use these files
1. Download all files and unnzip into a directory of your choice
2. run 'python your_directory/main.py'
3. The python scripts will output .csv files in your_directory and create a DB
4. The files will not run SQLite queries
5. Note that the jupyter notebook is where the SQLite commands are executed and it is fully available in report.pdf

The .py scripts are written to use the wlinn_sample file. If you wish to use the full file, edit the osmfile variable in config.py to point to the OSM file you wish to use.

The region I chose was West Linn, Oregon, my hometown. The original file was nearly 400 MB and the Report file was written to reflect that. The project explores the City of West Linn, Oregon using the information available in the Open Street Map. The purpose of the project is to use Data Wrangling techniques in Python to load, audit, clean and export an Open Street Map file for analysis using SQLite and Python data analysis libraries. 

## The repository contains the following files:

* C750.ipynb: Jupyter notebook containing the results and the code used to audit, clean, and process the OSM file.
* SQL Commands.txt: list of queries used in this project
* audit.py: the audit functions used in this project
* create_csvs.py: this script creates the CSV from the sample dataset
* createdb.py: creates the SQLite DB and creates tables with schema
* link_file.txt: a file containing a link to the target map area
* main.py: runs the audit, cleaning, and CSV creation functions
* config.py: contains global variables such as map file location and more
* map_cleaning.py: the map cleaning functions used in this project
* report.pdf: PDF document containing answers to rubric questions
* sample_generator.py: script to turn the full OSM into a sample file. Not needed but exists as FYI
* schema.py: schema used to validate the database before writing it in a CSV file
* wlinn: sample file used for this project. This is what the scripts will reference
* wlinn.rar: compressed file of the full data. Not needed for the project. Used purely for the curious and exists as FYI. Must unpack with WinRar or unrar otherwise it will appear corrupted
