# This file will run every night

# Update each individual game table in the database
# Update the weekly_trends database
# Update the weekly_config file with updated unique values

import psycopg2
import time
import requests
import json
import pytz
import psutil
from datetime import datetime
import config.all_time_config as all_time_config
import config.db_config as db_config
from models.upcoming_game import UpcomingGame

# Function to print memory usage
def log_memory_usage(stage):
    process = psutil.Process()
    mem_info = process.memory_info()
    print(f"[{stage}] Memory usage: {mem_info.rss / (1024 ** 2):.2f} MB")

total_start_time = time.time()
print('Starting...')
log_memory_usage("Start")  # Log memory at the start

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_config.DB_HOST,
    port=db_config.DB_PORT,
    database=db_config.DB_NAME,
    user=db_config.DB_USER,
    password=db_config.DB_PASSWORD
)
cur = conn.cursor()

def update_weekly_tables(cur):
    log_memory_usage("Before updating tables")  # Log memory before updating tables

    # Check if the table 'upcoming_games' exists
    check_table_query = '''
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'upcoming_games'
        )
    '''
    cur.execute(check_table_query)
    table_exists = cur.fetchone()[0]

    if table_exists:
        # If the table exists, truncate it
        truncate_table_query = '''
            TRUNCATE TABLE upcoming_games
        '''
        cur.execute(truncate_table_query)
        conn.commit()
    else:
        # If the table does not exist, create it
        create_table_query = '''
            CREATE TABLE upcoming_games (
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
                spread DECIMAL(4, 1),
                home_spread DECIMAL(4, 1),
                home_spread_odds INT,
                away_spread DECIMAL(4, 1),
                away_spread_odds INT,
                home_moneyline_odds INT,
                away_moneyline_odds INT,
                total DECIMAL(4, 1),
                over DECIMAL(4, 1),
                over_odds INT,
                under DECIMAL(4, 1),
                under_odds INT
            )
        '''
        cur.execute(create_table_query)
        conn.commit()

        log_memory_usage("After creating/updating upcoming_games table")  # Log memory after creating/updating table

    # Check if the table 'weekly_trends' exists
    check_table_query = '''
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'weekly_trends'
        )
    '''
    cur.execute(check_table_query)
    table_exists = cur.fetchone()[0]

    if table_exists:
        # If the table exists, truncate it
        truncate_table_query = '''
            TRUNCATE TABLE weekly_trends
        '''
        cur.execute(truncate_table_query)
        conn.commit()
    else:
        # If the table does not exist, create it
        create_table_query = '''
            CREATE TABLE weekly_trends (
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
                win_percentage DECIMAL(5, 2),
                games_applicable VARCHAR(250)
            )
        '''
        cur.execute(create_table_query)
        conn.commit()

        log_memory_usage("After creating/updating weekly_trends table")  # Log memory after creating/updating table

    # Make a call to odds API to get the upcoming games
    url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds?"
    body = {
        "apiKey": "APIKEY",
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "dateFormat": "iso",
        "oddsFormat": "american",
        "bookmakers": "fanduel",
        "commenceTimeFrom": all_time_config.WEEK_START,
        "commenceTimeTo": all_time_config.WEEK_END,
    }

    for key, value in body.items():
        url += f"{key}={value}&"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print("Error: Failed to access the API")

    games = []
    us_tz = pytz.timezone('US/Eastern')
    for game in data:
        # Odds API is 4 hours ahead, adjust dates accordingly
        utc_time = datetime.strptime(game['commence_time'], "%Y-%m-%dT%H:%M:%SZ")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(us_tz)
        date = local_time.strftime("%Y-%m-%d")

        home_team = game['home_team']
        away_team = game['away_team']
        if game['bookmakers'][0]['markets'][1]['outcomes'][0]['name'] == game['home_team']:
            home_spread = game['bookmakers'][0]['markets'][1]['outcomes'][0]['point']
            home_spread_odds = game['bookmakers'][0]['markets'][1]['outcomes'][0]['price']
            away_spread_odds = game['bookmakers'][0]['markets'][1]['outcomes'][1]['price']
        else:
            home_spread = game['bookmakers'][0]['markets'][1]['outcomes'][1]['point']
            home_spread_odds = game['bookmakers'][0]['markets'][1]['outcomes'][1]['price']
            away_spread_odds = game['bookmakers'][0]['markets'][1]['outcomes'][0]['price']
        if game['bookmakers'][0]['markets'][0]['outcomes'][0]['name'] == game['home_team']:
            home_moneyline_odds = game['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
            away_moneyline_odds = game['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
        else:
            home_moneyline_odds = game['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
            away_moneyline_odds = game['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
        total = game['bookmakers'][0]['markets'][2]['outcomes'][0]['point']
        over_odds = game['bookmakers'][0]['markets'][2]['outcomes'][0]['price']
        under_odds = game['bookmakers'][0]['markets'][2]['outcomes'][1]['price']

        print(f'DATETIME OF GAME {home_team} vs {away_team}: {date}')
        
        game = UpcomingGame(date, home_team, away_team, home_spread, home_spread_odds, away_spread_odds, home_moneyline_odds, away_moneyline_odds, total, over_odds, under_odds, True)
        games.append(game)

        log_memory_usage("After processing games from API")  # Log memory after processing games

    total_games_start_time = time.time()
    weekly_trends = {}
    for game in games:
        game_start_time = time.time()
        print(f'Processing game {game.id_string}...')
        # Insert game into upcoming_games table
        insert_query = '''
            INSERT INTO upcoming_games VALUES (
                %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, 
                %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, 
                %s, %s, %s, %s, %s
            )
        '''
        cur.execute(insert_query, game.to_tuple())
        conn.commit()

        log_memory_usage(f"After processing game {game.id_string}")  # Log memory after processing each game

        # Check if table exists
        check_table_query = f'''
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = '{game.id_string.lower()}'
            )
        '''
        cur.execute(check_table_query)
        table_exists = cur.fetchone()[0]

        if table_exists:
            # Truncate table if it exists
            truncate_table_query = f'''
                TRUNCATE TABLE {game.id_string.lower()}
            '''
            cur.execute(truncate_table_query)
            conn.commit()
        else:
            # Create table if it does not exist
            create_table_query = f'''
                CREATE TABLE {game.id_string.lower()} (
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
            '''
            cur.execute(create_table_query)
            conn.commit()

        # Insert trends into individual game trends table
        insert_query = f'''
            INSERT INTO {game.id_string.lower()}
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        trend_tuples = [trend.to_tuple() for trend in game.trends]
        cur.executemany(insert_query, trend_tuples)
        conn.commit()

        # Update individual game trends records to match records in trends table
        update_query = f'''
            UPDATE {game.id_string.lower()}
            SET 
                wins = trends.wins,
                losses = trends.losses,
                pushes = trends.pushes,
                total_games = trends.total_games,
                win_percentage = trends.win_percentage
            FROM trends
            WHERE {game.id_string.lower()}.id_string = trends.id_string;
        '''
        cur.execute(update_query)
        conn.commit()

        # Insert trends into weekly_trends dictionary with updated applicable games
        for trend in game.trends:
            weekly_game_string = f'{game.home_abbreviation}vs{game.away_abbreviation}'
            if trend.trend_id in weekly_trends:
                weekly_trends[trend.trend_id].applicable_games += f', {weekly_game_string}'
            else:
                trend.applicable_games = weekly_game_string
                weekly_trends[trend.trend_id] = trend

        game_end_time = time.time()
        print(f'Game processing took {game_end_time - game_start_time}')

    total_games_end_time = time.time()
    print(f'Total games processing took {total_games_end_time - total_games_start_time}')

    log_memory_usage("After processing all games")  # Log memory after processing all games

    weekly_trends_start_time = time.time()
    print('Inserting weekly trends...')
    insert_query = '''
        INSERT INTO weekly_trends
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    trend_tuples = [trend.to_tuple() for trend in weekly_trends.values()]
    cur.executemany(insert_query, trend_tuples)
    conn.commit()
    weekly_trends_end_time = time.time()
    print(f'Inserting weekly trends took {weekly_trends_end_time - weekly_trends_start_time}')

    log_memory_usage("After inserting weekly trends")  # Log memory after inserting weekly trends

    updating_trends_start_time = time.time()
    print('Updating weekly trends...')
    update_query = '''
        UPDATE weekly_trends
        SET 
            wins = trends.wins,
            losses = trends.losses,
            pushes = trends.pushes,
            total_games = trends.total_games,
            win_percentage = trends.win_percentage
        FROM trends
        WHERE weekly_trends.id_string = trends.id_string;
    '''
    cur.execute(update_query)
    conn.commit()
    updating_trends_end_time = time.time()
    print(f'Updating weekly trends took {updating_trends_end_time - updating_trends_start_time}')

    log_memory_usage("After updating weekly trends")  # Log memory after updating weekly trends

def update_weekly_config(cur):
    table = 'weekly_trends'
    columns = ['month', 'day_of_week', 'divisional', 'spread', 'total']
    unique_values = {}

    weekly_config_start_time = time.time()
    print(f'Updating unique weekly config values...')

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
    with open('src/config/weekly_config.py', 'w') as f:
        for key, values in unique_values.items():
            f.write(f'{key} = {values}\n')

    weekly_config_end_time = time.time()
    print(f'Updating unique weekly config values took {weekly_config_end_time - weekly_config_start_time}')

    total_end_time = time.time()
    print(f'Total time took {total_end_time - total_start_time}')

##################################################################################################
# Update weekly_trends tables, upcoming games table, and each individual game table for the week #
##################################################################################################
update_weekly_tables(cur)

############################################################################
# Update weekly_config with new unique values from the weekly_trends table #
############################################################################
update_weekly_config(cur)