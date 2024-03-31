import psycopg2
import time

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="bangarang19"
)
cur = conn.cursor()

# This file will run every monday night

# Add the previous weeks games to the games table

# Update the trends table with results from the previous week

# Delete all tables for individual games from the previous week

# Pull new lines from the sportsbook API

# Update the upcoming games table with the new games and new lines

#######################################################################
# Update all_time_config with new unique values from the trends table #
#######################################################################
table = 'trends'
columns = ['month', 'day_of_week', 'divisional', 'spread', 'total']
unique_values = {}
all_time_config_start_time = time.time()
print(f'Updating unique all time config values...')

# Retrieve the unqiue elements from designated columns and add to dictionary
for column in columns:
    cur.execute(f'SELECT DISTINCT {column} FROM {table}')
    unique_values[f'{column.upper()}S'] = [row[0] for row in cur.fetchall() if row[0] is not None]
    if column == 'day_of_week':
        # Sort columns in weekday order
        unique_values[f'{column.upper()}S'] = sorted(unique_values[f'{column.upper()}S'], key=lambda x: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].index(x))
    elif column == 'month':
        # Sort columns in month order
        unique_values[f'{column.upper()}S'] = sorted(unique_values[f'{column.upper()}S'], key=lambda x: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].index(x))
    elif column == 'spread':
        # Sort columns in the following order: exact values, "or more" values, "or less" values (by numeric value)
        contains_or_more = []
        contains_or_less = []
        for value in unique_values[f'{column.upper()}S']:
            if 'or more' in value:
                contains_or_more.append(value)
            elif 'or less' in value:
                contains_or_less.append(value)
        without_or_more_or_less = [value for value in unique_values[f'{column.upper()}S'] if 'or more' not in value and 'or less' not in value]
        without_or_more_or_less.sort(key=lambda x: float(x))
        contains_or_more.sort(key=lambda x: float(x.split(' ')[0]))
        contains_or_less.sort(key=lambda x: float(x.split(' ')[0]))
        unique_values[f'{column.upper()}S'] = without_or_more_or_less + contains_or_more + contains_or_less
    elif column == 'total':
        # Sort columns in the following order: exact values, "or more" values, "or less" values (by numeric value)
        contains_or_more = []
        contains_or_less = []
        for value in unique_values[f'{column.upper()}S']:
            if 'or more' in value:
                contains_or_more.append(value)
            elif 'or less' in value:
                contains_or_less.append(value)
        contains_or_more.sort(key=lambda x: float(x.split(' ')[0]))
        contains_or_less.sort(key=lambda x: float(x.split(' ')[0]))
        unique_values[f'{column.upper()}S'] = contains_or_more + contains_or_less

# Write new unique weekly values to weekly_config file
with open('src/config/all_time_config.py', 'w') as f:
    for key, values in unique_values.items():
        f.write(f'{key} = {values}\n')

all_time_config_end_time = time.time()
print(f'Updating unique all time config values took {all_time_config_end_time - all_time_config_start_time}')
