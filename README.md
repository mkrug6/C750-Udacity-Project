# A case study of data wrangling using the City of West Linn, Oregon with Open Street Map data

# HOW TO RUN AND USE THESE FILES
1. Download all files and unnzip into a directory of your choice
2. run 'python your_directory/main.py'
3. The python scripts will output .csv files in your_directory
4. To create the connection to sqlite, you must use the jupyter notebook.
5. Note that the jupyter notebook is where the SQLite commands are executed and it is fully available in report.pdf

The full file is available as wlinn.rar. Note that this is a RAR file. You must use unrar on Linux/Mac or WinRar on windows to properly unpack this file otherwise it will appear corrupt. This file is the full data set and is ~400 MB uncompressed. It is not needed for the scripts as they use the wlinn sample file. If you wish to use the full database, you must delete the "wlinn" fill and unpack the wlinn.rar file with the same name in the current directory. Recommend opening the Jupyter notebook file for ease of use and readability. The region I chose was West Linn, Oregon, my hometown. The original file was nearly 400 MB and the .ipynb file was written to reflect that. The project explores the City of West Linn, Oregon using the information available in the Open Street Map. The purpose of the project is to use Data Wrangling techniques in Python to load, audit, clean and export an Open Street Map file, for further analysis using SQLite and Python data analysis libraries. 

## The repository contains the following files:

1.C750.ipynb: Jupyter notebook containing the results and the code used to audit, clean, and process the Open Street Map file.
2.SQL Commands.txt: list of queries used in this project
3.audit.py: the audit functions used in this project
4.create_csvs.py: this script creates the CSV from the sample dataset
5.link_file.txt: a file containing a link to the target map area
6.main.py: runs the audit, cleaning, and CSV creation functions
7.config.py: contains global variables such as map file location and more
8.map_cleaning.py: the map cleaning functions used in this project
9.report.pdf: PDF document containing answers to rubric questions
10. sample_generator.py: script to turn the full OSM into a sample file. Not needed but exists as FYI
11. schema.py: schema used to validate the database before writing it in a CSV file
12. wlinn: sample file used for this project. This is what the scripts will reference
13. wlinn.rar: compressed file of the full data. Not needed for the project. Used purely for the curious and exists as FYI
