# MSDS_SERA_capstone

## Getting Started:

- Add the data folder to root directory for python files to read properly
- Data can then be read in the format `pd.read_excel("../data/<filename>')`

## File Structure:

- Data
  - Ignored Directory, where python files will assume the csv files will be read from
- Stata Replication
  - Replication of STATA cleaning and randomization in python. It includes:
    - scripts
      - This is where the actualy python cleaning code is
    - utils.py
      - This is where generic functions will go, broken down by portion of the pipeline
    - constants.py
      - This is where generic constants will go (repeated lists of column names, csv names), broken down by portion of the pipeline
- Stata
  - Original STATA files
