"""
Module: db.py

This module contains functions for processing game data and storing it in a PostgreSQL database. 
It includes methods for formatting DataFrames, creating database tables, processing game trends, 
inserting game data into the database, and executing the data processing pipeline.

Functions:
- format_dataframe(dataframe): Format the DataFrame containing game data.
- make_games_table(cur, conn): Create the 'games' table in the database.
- make_trends_table(cur, conn): Create the 'trends' table in the database.
- process_game_trends(game_trends, trends_dict, game): Process game trends 
  and update trends dictionary.
- process_game_rows(cur, conn, dataframe): Process game rows and insert data into the database.

Execution:
The module also contains execution code to read game data from an Excel file, 
connect to a PostgreSQL database, create necessary tables, process game data, 
and store it in the database.

Usage:
To use this module, import it into your Python script and call the necessary functions.

Example:
    import pandas as pd
    from data_processing import format_dataframe, make_games_table,
      make_trends_table, process_game_rows

    # Read game data from Excel file
    data = pd.read_excel('datafiles/nfl.xlsx')

    # Format the DataFrame
    data = format_dataframe(data)

    # Connect to PostgreSQL database
    # (Assuming the database parameters are properly configured)

    # Create 'games' table
    make_games_table(cursor, connection)

    # Create 'trends' table
    make_trends_table(cursor, connection)

    # Process game rows and insert data into the database
    process_game_rows(cursor, connection, data)
"""

import time
import psycopg2
import pandas as pd
from models.game import Game

#########################
### DATAFRAME METHODS ###
#########################

def format_dataframe(dataframe):
    """
    Format the DataFrame containing game data.

    Args:
    - dataframe (pd.DataFrame): DataFrame containing game data.

    Returns:
    - pd.DataFrame: Formatted DataFrame.
    """

    # Change date entered from date object to just "YYYY-MM-DD" format
    dataframe['Date'] = dataframe['Date'].astype(str).str[:10]

    # Reverse dataframe so oldest game is indexed first
    dataframe = dataframe.iloc[::-1].reset_index(drop=True)

    # If 'Home Line Close' and 'Away Line Close' are empty, replace them
    # with 'Home Line Open' and 'Home Line Open * -1'
    dataframe['Home Line Close'].fillna(dataframe['Home Line Open'], inplace=True)
    dataframe['Total Score Close'].fillna(dataframe['Total Score Open'], inplace=True)

    # Delete unnecessary columns
    dataframe.drop(columns=[
        # Don't need any moneyline odds columns
        'Home Odds Open', 'Home Odds Min', 'Home Odds Max', 'Home Odds Close',
        'Away Odds Open', 'Away Odds Min', 'Away Odds Max', 'Away Odds Close',

        # Don't need spread columns besides closing home lines
        'Home Line Open', 'Home Line Min', 'Home Line Max',
        'Away Line Open', 'Away Line Min', 'Away Line Max', 'Away Line Close',

        # Don't need any spread odds columns
        'Home Line Odds Open', 'Home Line Odds Min', 'Home Line Odds Max', 'Home Line Odds Close',
        'Away Line Odds Open', 'Away Line Odds Min', 'Away Line Odds Max', 'Away Line Odds Close',

        # Don't need any total columns besides closing total
        'Total Score Open', 'Total Score Min', 'Total Score Max',

        # Don't need any total score odds columns
        'Total Score Over Open', 'Total Score Over Min',
        'Total Score Over Max', 'Total Score Over Close',
        'Total Score Under Open', 'Total Score Under Min',
        'Total Score Under Max', 'Total Score Under Close',

        # Don't need overtime, neutral venue, or notes
        'Overtime?', 'Neutral Venue?', 'Playoff Game?', 'Notes'
    ], inplace = True)

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

    return dataframe

########################
### DATABASE METHODS ###
########################

def make_games_table(cur, conn):
    """
    Create the 'games' table in the database.

    Args:
    - cur (psycopg2.extensions.cursor): Database cursor.
    - conn (psycopg2.extensions.connection): Database connection.
    """

    cur.execute('''
       DROP TABLE IF EXISTS games         
    ''')
    cur.execute(
    '''
        CREATE TABLE IF NOT EXISTS games (
            id VARCHAR(64) PRIMARY KEY,
            id_string VARCHAR(14),
            date VARCHAR(10),
            month VARCHAR(10),
            day INT,
            year INT,
            season VARCHAR(9),
            day_of_week VARCHAR(9),
            home_team VARCHAR(25),
            home_abbreviation VARCHAR(3),
            home_division VARCHAR(9),
            away_team VARCHAR(25),
            away_abbreviation VARCHAR(3),
            away_division VARCHAR(9),
            divisional BOOLEAN,
            home_score INT,
            away_score INT,
            combined_score INT,
            tie BOOLEAN,
            winner VARCHAR(25),
            loser VARCHAR(25),
            spread DECIMAL(4, 1),
            home_spread DECIMAL(4, 1),
            home_spread_result INT,
            away_spread DECIMAL(4, 1),
            away_spread_result INT,
            spread_push BOOLEAN,
            pk BOOLEAN,
            total DECIMAL(4, 1),
            total_push BOOLEAN,
            home_favorite BOOLEAN,
            away_underdog BOOLEAN,
            away_favorite BOOLEAN,
            home_underdog BOOLEAN,
            home_win BOOLEAN,
            away_win BOOLEAN,
            favorite_win BOOLEAN,
            underdog_win BOOLEAN,
            home_favorite_win BOOLEAN,
            away_underdog_win BOOLEAN,
            away_favorite_win BOOLEAN,
            home_underdog_win BOOLEAN,
            home_cover BOOLEAN,
            away_cover BOOLEAN,
            favorite_cover BOOLEAN,
            underdog_cover BOOLEAN,
            home_favorite_cover BOOLEAN,
            away_underdog_cover BOOLEAN,
            away_favorite_cover BOOLEAN,
            home_underdog_cover BOOLEAN,
            over_hit BOOLEAN,
            under_hit BOOLEAN
        )
    ''')
    conn.commit()

def make_trends_table(cur, conn):
    """
    Create the 'trends' table in the database.

    Args:
    - cur (psycopg2.extensions.cursor): Database cursor.
    - conn (psycopg2.extensions.connection): Database connection.
    """

    cur.execute('''
       DROP TABLE IF EXISTS trends         
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            id VARCHAR(64),
            id_string VARCHAR(250),
            category VARCHAR(25),
            month VARCHAR(10),
            day_of_week VARCHAR(10),
            divisional BOOLEAN,
            spread VARCHAR(15),
            total VARCHAR(15),
            seasons VARCHAR(15),
            wins INT,
            losses INT,
            pushes INT,
            total_games INT,
            win_percentage DECIMAL(5, 2)
        )
    ''')
    conn.commit()

def process_game_trends(game_trends, trends_dict, game):
    """
    Process game trends and update trends dictionary.

    Args:
    - game_trends (list): List of trend objects for the game.
    - trends_dict (dict): Dictionary to store trends.
    - game (Game): Game object.

    Returns:
    - None
    """

    for trend in game_trends:
        trend_to_update = trends_dict.get(trend.id)
        if trend_to_update is None:
            trends_dict[trend.id] = trend
            trend_to_update = trends_dict[trend.id]
        trend_to_update.update_record(game)

def process_game_rows(cur, conn, dataframe):
    """
    Process game rows and insert data into the database.

    Args:
    - cur (psycopg2.extensions.cursor): Database cursor.
    - conn (psycopg2.extensions.connection): Database connection.
    - dataframe (pd.DataFrame): DataFrame containing game data.

    Returns:
    - None
    """

    trends = {}
    games = []

    for _, row in dataframe.iterrows():
        game = Game(
            row['Date'],
            row['Home Team'], row['Away Team'],
            row['Home Score'], row['Away Score'],
            row['Home Spread'],
            row['Total'], True
        )

        process_game_trends(game.trends, trends, game)
        games.append(game.to_dict())

    trends_arr = [trend.to_tuple() for trend in trends.values()]

    sql_trends_insert = '''
        INSERT INTO trends (id, id_string, category, month, day_of_week, divisional, spread, total, seasons, wins, losses, pushes, total_games, win_percentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    sql_games_insert = '''
        INSERT INTO games VALUES (
            %(id)s, %(id_string)s, %(date)s, %(month)s, %(day)s, %(year)s, %(season)s, 
            %(day_of_week)s, %(home_team)s, %(home_abbreviation)s, %(home_division)s, 
            %(away_team)s, %(away_abbreviation)s, %(away_division)s, %(divisional)s, %(home_score)s, 
            %(away_score)s, %(combined_score)s, %(tie)s, %(winner)s, %(loser)s, %(spread)s, 
            %(home_spread)s, %(home_spread_result)s, %(away_spread)s, %(away_spread_result)s, 
            %(spread_push)s, %(pk)s, %(total)s, %(total_push)s, %(home_favorite)s, %(away_underdog)s, 
            %(away_favorite)s, %(home_underdog)s, %(home_win)s, %(away_win)s, %(favorite_win)s, 
            %(underdog_win)s, %(home_favorite_win)s, %(away_underdog_win)s, %(away_favorite_win)s, 
            %(home_underdog_win)s, %(home_cover)s, %(away_cover)s, %(favorite_cover)s, 
            %(underdog_cover)s, %(home_favorite_cover)s, %(away_underdog_cover)s, %(away_favorite_cover)s, 
            %(home_underdog_cover)s, %(over_hit)s, %(under_hit)s
        )
    '''

    cur.executemany(sql_trends_insert, trends_arr)
    cur.executemany(sql_games_insert, games)

    conn.commit()

#################
### EXECUTION ###
#################

start_time = time.time()
data = pd.read_excel('datafiles/nfl.xlsx')
data = format_dataframe(data)

# Connect to sql database
connection = psycopg2.connect(
    host = 'localhost',
    dbname = 'postgres',
    user = 'postgres',
    password = 'pass',
    port = 5432
)
cursor = connection.cursor()

make_games_table(cursor, connection)
make_trends_table(cursor, connection)
process_game_rows(cursor, connection, data)

connection.commit()
cursor.close()
connection.close()

end_time = time.time()
print(f'TOTAL TIME: {end_time - start_time}\n')
