# A case study of data wrangling using the City of West Linn, Oregon with Open Street Map data

# HOW TO RUN AND USE THESE FILES
1. Download all files and unnzip into a directory of your choice
2. run 'python your_directory/main.py'
3. The python scripts will output .csv files in your_directory
4. To create the connection to sqlite, you must use the jupyter notebook.
5. Note that the jupyter notebook is where the SQLite commands are executed and it is fully available in report.pdf

The full file is available as wlinn.rar. Note that this is a RAR file. You must use unrar on Linux/Mac or WinRar on windows to properly unpack this file otherwise it will appear corrupt. This file is the full data set and is ~400 MB uncompressed. It is not needed for the scripts as they use the wlinn_sample file. Recommend opening the Jupyter notebook file for ease of use and readability. The region I chose was West Linn, Oregon, my hometown. The original file was nearly 400 MB and the .ipynb file was written to reflect that. The project explores the City of West Linn, Oregon using the information available in the Open Street Map. The purpose of the project is to use Data Wrangling techniques in Python to load, audit, clean and export an Open Street Map file, for further analysis using SQLite and Python data analysis libraries. 

## The repository contains the following files:

C750.ipynb: Jupyter notebook containing the results and the code used to audit, clean, and process the Open Street Map file.

SQL Commands.txt: list of queries used in this project

audit.py: the audit functions used in this project

create_csvs.py: this script creates the CSV from the sample dataset

link_file.txt: a file containing a link to the target map area

main.py: runs the audit, cleaning, and CSV creation functions

map_cleaning.py: the map cleaning functions used in this project

report.pdf: PDF document containing answers to rubric questions

sample_generator.py: script to turn the full OSM into a sample file. Not needed but exists as FYI

theschema.py: schema used to validate the database before writing it in a CSV file

wlinn: sample file used for this project. This is what the scripts will reference

wlinn.rar: compressed file of the full data. Not needed for the project. Used purely for the curious and exists as FYI

