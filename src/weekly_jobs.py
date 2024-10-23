# This file will run every monday night

# Add the previous weeks games to the games table
# Update the trends table with results from the previous week
# Delete all tables for individual games from the previous week
# Pull new lines from the sportsbook API
# Update the upcoming games table with the new games and new lines
# Update the all_time_config file with updated unique values

import psycopg2
from psycopg2.extras import execute_values
import time
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import config.all_time_config as all_time_config
import config.db_config as db_config
from models.game import Game
import psutil  # Importing psutil for memory tracking

# Function to track memory usage
def print_memory_usage(step):
    process = psutil.Process()
    mem_info = process.memory_info()
    print(f"{step} - Memory used: {mem_info.rss / (1024 ** 2):.2f} MB")  # Memory in MB

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_config.DB_HOST,
    port=db_config.DB_PORT,
    database=db_config.DB_NAME,
    user=db_config.DB_USER,
    password=db_config.DB_PASSWORD
)
cur = conn.cursor()

print_memory_usage("After database connection")  # Check memory after DB connection

def download_updated_data():
    url = 'https://www.aussportsbetting.com/historical_data/nfl.xlsx'
    local_filename = 'datafiles/nfl.xlsx'

    response = requests.get(url)

    if response.status_code == 200:
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        print('File downloaded successfully')
    else:
        print('Failed to download file')

    print_memory_usage("After downloading data")  # Memory after file download

def get_last_weeks_games():
    data = pd.read_excel('datafiles/nfl.xlsx')

    week_start_date = datetime.strptime(all_time_config.WEEK_START, '%Y-%m-%dT%H:%M:%SZ').date()
    week_end_date = datetime.strptime(all_time_config.WEEK_END, '%Y-%m-%dT%H:%M:%SZ').date()

    data['Date'] = pd.to_datetime(data['Date']).dt.date

    last_weeks_games = data[(data['Date'] >= week_start_date) & (data['Date'] < week_end_date)]

    print_memory_usage("After loading last week's games")  # Memory after loading games
    return last_weeks_games

def format_dataframe(dataframe):
    # Change date entered from date object to just "YYYY-MM-DD" format
    dataframe['Date'] = dataframe['Date'].astype(str).str[:10]

    # Reverse dataframe so oldest game is indexed first
    dataframe = dataframe.iloc[::-1].reset_index(drop=True)

    # If 'Home Line Close' and 'Away Line Close' are empty, replace them
    dataframe['Home Line Close'].fillna(dataframe['Home Line Open'], inplace=True)
    dataframe['Total Score Close'].fillna(dataframe['Total Score Open'], inplace=True)

    # Delete unnecessary columns
    dataframe.drop(columns=[
        'Home Odds Open', 'Home Odds Min', 'Home Odds Max', 'Home Odds Close',
        'Away Odds Open', 'Away Odds Min', 'Away Odds Max', 'Away Odds Close',
        'Home Line Open', 'Home Line Min', 'Home Line Max',
        'Away Line Open', 'Away Line Min', 'Away Line Max', 'Away Line Close',
        'Home Line Odds Open', 'Home Line Odds Min', 'Home Line Odds Max', 'Home Line Odds Close',
        'Away Line Odds Open', 'Away Line Odds Min', 'Away Line Odds Max', 'Away Line Odds Close',
        'Total Score Open', 'Total Score Min', 'Total Score Max',
        'Total Score Over Open', 'Total Score Over Min', 'Total Score Over Max', 'Total Score Over Close',
        'Total Score Under Open', 'Total Score Under Min', 'Total Score Under Max', 'Total Score Under Close',
        'Overtime?', 'Neutral Venue?', 'Playoff Game?', 'Notes'
    ], inplace=True)

    # Replace
    dataframe.rename(columns={
        'Home Line Close': 'Home Spread', 
        'Total Score Close': 'Total',
        'Neutral Venue?': 'Neutral Venue'
    }, inplace=True)

    # Replace Y and N (or NaN) with True and False
    dataframe.fillna(False, inplace=True)
    dataframe.replace('Y', True, inplace=True)

    # Keep team names and locations consistent
    name_change_dict = {
        'Washington': 'Washington Commanders', 
        'Rams': 'Los Angeles Rams',
        'Raiders': 'Las Vegas Raiders',
        'Chargers': 'Los Angeles Chargers'
    }

    for key, value in name_change_dict.items():
        home_mask = dataframe['Home Team'].str.contains(key)
        away_mask = dataframe['Away Team'].str.contains(key)
        dataframe.loc[home_mask, 'Home Team'] = value
        dataframe.loc[away_mask, 'Away Team'] = value

    print_memory_usage("After formatting dataframe")  # Memory after formatting
    return dataframe

def process_game_trends(game_trends, trends_dict, game):
    for trend in game_trends:
        trend_to_update = trends_dict.get(trend.trend_id)
        if trend_to_update is None:
            trends_dict[trend.trend_id] = trend
            trend_to_update = trends_dict[trend.trend_id]
        trend_to_update.update_record(game)

    print_memory_usage("After processing game trends")  # Memory after processing trends

def process_game_rows(cur, conn, dataframe):
    trends = {}
    games = []

    print_memory_usage("Start of process_game_rows")  # Memory at the start of the function

    for _, row in dataframe.iterrows():
        game = Game(
            row['Date'],
            row['Home Team'], row['Away Team'],
            row['Home Score'], row['Away Score'],
            row['Home Spread'],
            row['Total'], True
        )

        print(f'Processing game: {game.id_string}')
        start_time = time.time()
        
        process_game_trends(game.trends, trends, game)  # Process game trends
        games.append(game.to_dict())  # Add game to the list
        
        end_time = time.time()
        print(f'Game processed in {end_time - start_time} seconds')

        print_memory_usage(f"After processing game {game.id_string}")  # Memory after each game processing

    trends_arr = [trend.to_tuple() for trend in trends.values()]

    print_memory_usage("Before adding games to database")  # Memory before inserting into DB

    # Add games to database
    print('Adding games to database...')
    start_time = time.time()
    sql_games_insert = '''
        INSERT INTO games VALUES (
            %(game_id)s, %(id_string)s, %(date)s, %(month)s, %(day)s, %(year)s, %(season)s, 
            %(day_of_week)s, %(home_team)s, %(home_abbreviation)s, %(home_division)s, 
            %(away_team)s, %(away_abbreviation)s, %(away_division)s, %(divisional)s, %(home_score)s, 
            %(away_score)s, %(combined_score)s, %(tie)s, %(winner)s, %(loser)s, %(spread)s, 
            %(home_spread)s, %(home_spread_result)s, %(away_spread)s, %(away_spread_result)s, 
            %(spread_push)s, %(pickem)s, %(total)s, %(total_push)s, %(home_favorite)s, %(away_underdog)s, 
            %(away_favorite)s, %(home_underdog)s, %(home_win)s, %(away_win)s, %(favorite_win)s, 
            %(underdog_win)s, %(home_favorite_win)s, %(away_underdog_win)s, %(away_favorite_win)s, 
            %(home_underdog_win)s, %(home_cover)s, %(away_cover)s, %(favorite_cover)s, 
            %(underdog_cover)s, %(home_favorite_cover)s, %(away_underdog_cover)s, %(away_favorite_cover)s, 
            %(home_underdog_cover)s, %(over_hit)s, %(under_hit)s
        )
    '''
    cur.executemany(sql_games_insert, games)  # Insert games into the DB
    conn.commit()
    
    end_time = time.time()
    print(f'Games added to database in {end_time - start_time} seconds')

    print_memory_usage("After adding games to database")  # Memory after inserting games

    return trends_arr

def update_trends_in_db(cur, conn, trends_arr):
    print(f'Updating {len(trends_arr)} trends in the database...')
    batch_size = 1000
    total_start_time = time.time()

    print_memory_usage("Start of update_trends_in_db")  # Memory at the start

    # Process trends in batches
    for i in range(0, len(trends_arr), batch_size):
        batch = trends_arr[i:i + batch_size]
        upsert_data = []

        for trend in batch:
            trend_id = trend[0]
            wins = trend[9]
            losses = trend[10]
            pushes = trend[11]
            total_games = wins + losses + pushes
            upsert_data.append((trend_id, trend[1], trend[2], trend[3], trend[4], trend[5], trend[6], trend[7], trend[8], wins, losses, pushes, total_games, 0.0))

        # Perform upsert operation
        query = """
            INSERT INTO trends (id, id_string, category, month, day_of_week, divisional, spread, total, seasons, wins, losses, pushes, total_games, win_percentage)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                wins = trends.wins + EXCLUDED.wins,
                losses = trends.losses + EXCLUDED.losses,
                pushes = trends.pushes + EXCLUDED.pushes,
                total_games = trends.total_games + EXCLUDED.total_games,
                win_percentage = ROUND(
                    (trends.wins + EXCLUDED.wins) / 
                    (trends.wins + EXCLUDED.wins + trends.losses + EXCLUDED.losses + (trends.pushes + EXCLUDED.pushes) / 2.0) * 100, 2)
        """
        batch_start_time = time.time()
        execute_values(cur, query, upsert_data)  # Execute the upsert query
        batch_end_time = time.time()
        print(f'Processed batch {i // batch_size + 1} in {batch_end_time - batch_start_time:.2f} seconds')

        print_memory_usage(f"After processing batch {i // batch_size + 1}")  # Memory after processing each batch

    # Commit the transaction
    conn.commit()

    total_end_time = time.time()
    print(f'Updated all trends in {total_end_time - total_start_time:.2f} seconds')

    print_memory_usage("After updating trends in database")  # Memory after updating trends

def update_all_time_config(cur):
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

    # Add the week start and end dates to the dictionary
    today = datetime.now(timezone.utc)
    week_start = today.strftime('%Y-%m-%dT00:00:00Z')
    one_week_later = today + timedelta(weeks=1)
    week_end = one_week_later.strftime('%Y-%m-%dT00:00:00Z')

    unique_values['WEEK_START'] = str(week_start)
    unique_values['WEEK_END'] = str(week_end)

    # Write new unique weekly values to weekly_config file
    with open('src/config/all_time_config.py', 'w') as f:
        for key, values in unique_values.items():
            if key == 'WEEK_START' or key == 'WEEK_END':
                f.write(f'{key} = \'{values}\'\n')
            else:
                f.write(f'{key} = {values}\n')

    all_time_config_end_time = time.time()
    print(f'Updating unique all time config values took {all_time_config_end_time - all_time_config_start_time}')

def drop_last_week_tables(cur, conn, tables_to_exclude):
    # Query to get all table names except the ones in exclude_tables
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
    AND table_name NOT IN %s;
    """
    cur.execute(query, (tuple(tables_to_exclude),))
    tables = cur.fetchall()

    # Drop each table
    for table in tables:
        table_name = table[0]
        drop_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        cur.execute(drop_query)
        print(f"Dropped table {table_name}")

    # Commit the transaction
    conn.commit()

#############################################################################
# Download spreadsheet from aussportsbetting and add it to datafiles folder #
#############################################################################
download_updated_data()

##########################################################
# Extract only games from the last week into a dataframe #
##########################################################
last_weeks_games = get_last_weeks_games()

######################################################
# Format the dataframe to match the games table data #
######################################################
data = format_dataframe(last_weeks_games)

############################################################
# Process the game rows and insert games into the database #
############################################################
trends_arr = process_game_rows(cur, conn, data)

##############################################################
# Update the trends table with the new trends from the games #
##############################################################
update_trends_in_db(cur, conn, trends_arr)

#######################################################################
# Update all_time_config with new unique values from the trends table #
#######################################################################
update_all_time_config(cur)

#######################################################
# Drop the tables for individual games from last week #
#######################################################
tables_to_exclude = ['games', 'trends']
drop_last_week_tables(cur, conn, tables_to_exclude)

conn.close()
