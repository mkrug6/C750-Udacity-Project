# A case study of data wrangling using the City of West Linn, Oregon with Open Street Map data

# HOW TO RUN AND USE THESE FILES
1. Download all files and unnzip into a directory of your choice
2. run 'python your_directory/main.py'
3. The python scripts will output .csv files in your_directory


Recommend opening the Jupyter notebook file for ease of use and readability. The region I chose was West Linn, Oregon, my hometown. The original file was nearly 400 MB and the .ipynb file was written to reflect that. The project explores the City of West Linn, Oregon using the information available in the Open Street Map. The purpose of the project is to use Data Wrangling techniques in Python to load, audit, clean and export an Open Street Map file, for further analysis using SQLite and Python data analysis libraries. 

## The repository contains the following files:

C750.ipynb: Jupyter notebook containing the results and the code used to audit, clean, and process the Open Street Map file.

SQL Commands.txt: list of queries used in this project

link_file.txt: a file containing a link to the target map area

wlinn_sample: sample file used for this project.

schema.py: Schema used to validate the database before writing it in a CSV file.

report.pdf: PDF document containing answers to rubric questions.

audit.py: the audit functions used in this project

map_cleaning.py: the map cleaning functions used in this project

sample_generator.py: a way to generate a small sample of the original OSM file. Note that this is for demonstration purposes and is not needed for this project. 
