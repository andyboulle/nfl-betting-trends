#################################################################################
# data_generator.py                                                             #
#                                                                               #
# This file will convert the original Excel file to a dataframe in a format     #
# that will allow us to easily analyze it. It will convert the file from Excel  #
# to CSV then clean the data, and add/remove columns as needed.                 # 
#                                                                               #
# Excel File Link:                                                              #
# https://www.aussportsbetting.com/data/historical-nfl-results-and-odds-data/   #
#################################################################################
import pandas as pd
from datetime import datetime
import data_cleaner
import column_editor
import time

excel_file_name = 'datafiles/excel/nfl.xlsx'
csv_file_name = 'datafiles/csv/nfl.csv'

# Start measuring the total time
total_start_time = time.time()

# Read Excel file and convert to CSV
start_time = time.time()
df = pd.read_excel(excel_file_name)
df.to_csv(csv_file_name, sep='\t', index=False)
read_excel_time = time.time() - start_time

# Data Cleaning
start_time = time.time()
df = data_cleaner.clean_data(df)
data_cleaning_time = time.time() - start_time

# Column Editing
start_time = time.time()
df = column_editor.edit_columns(df)
column_editing_time = time.time() - start_time

# Save dataframe with edited columns to CSV
start_time = time.time()
df.to_csv('datafiles/csv/analysis_data.csv', index=False)
save_to_csv_time = time.time() - start_time

# Calculate total time
total_time = time.time() - total_start_time

# Print execution times
print(f"Read Excel time: {read_excel_time} seconds")
print(f"Data Cleaning time: {data_cleaning_time} seconds")
print(f"Column Editing time: {column_editing_time} seconds")
print(f"Save to CSV time: {save_to_csv_time} seconds")
print(f"Total process time: {total_time} seconds")



