import time
import psycopg2
import pandas as pd
from src.models.game import Game

#########################
### DATAFRAME METHODS ###
#########################

def format_dataframe(df):
    # Change date entered from date object to just "YYYY-MM-DD" format
    df['Date'] = df['Date'].astype(str).str[:10]

    # Reverse dataframe so oldest game is indexed first
    df = df.iloc[::-1].reset_index(drop=True)

    # If 'Home Line Close' and 'Away Line Close' are empty, replace them with 'Home Line Open' and 'Home Line Open * -1'
    df['Home Line Close'].fillna(df['Home Line Open'], inplace=True)
    df['Total Score Close'].fillna(df['Total Score Open'], inplace=True)

    # Delete unnecessary columns
    df.drop(columns=[
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
        'Total Score Over Open', 'Total Score Over Min', 'Total Score Over Max', 'Total Score Over Close',
        'Total Score Under Open', 'Total Score Under Min', 'Total Score Under Max', 'Total Score Under Close',

        # Don't need overtime, neutral venue, or notes
        'Overtime?', 'Neutral Venue?', 'Playoff Game?', 'Notes'
    ], inplace = True)

    # Replace 
    df.rename(columns={
        'Home Line Close': 'Home Spread', 
        'Total Score Close': 'Total',
        'Neutral Venue?': 'Neutral Venue'
    }, inplace=True)

    # Replace Y and N (or NaN) with True and False
    df.fillna(False, inplace=True)
    df.replace('Y', True, inplace=True)

    # Keep team names and locations consistent
    name_change_dict = {
        'Washington': 'Washington Commanders', 
        'Rams': 'Los Angeles Rams',
        'Raiders': 'Las Vegas Raiders',
        'Chargers': 'Los Angeles Chargers'
    }

    for key, value in name_change_dict.items():
        home_mask = df['Home Team'].str.contains(key)
        away_mask = df['Away Team'].str.contains(key)
        df.loc[home_mask, 'Home Team'] = value
        df.loc[away_mask, 'Away Team'] = value

    return df

########################
### DATABASE METHODS ###
########################

def make_games_table(cur, df):
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

def make_trends_table(cur):
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
    for trend in game_trends:
        trend_to_update = trends_dict.get(trend.id)
        if trend_to_update is None:
            trends_dict[trend.id] = trend
            trend_to_update = trends_dict[trend.id]
        trend_to_update.update_record(game)

def process_game_rows(cur, df):
    trends = {}
    games = []

    for _, row in df.iterrows():
        game = Game(
            row['Date'],  
            row['Home Team'], row['Away Team'],
            row['Home Score'], row['Away Score'],
            row['Home Spread'],
            row['Total'], True
        )

        process_game_trends(game.trends, trends, game)
        games.append(game)

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
df = pd.read_excel('datafiles/nfl.xlsx')
df = format_dataframe(df)

# Connect to sql database
conn = psycopg2.connect(
    host = 'localhost',
    dbname = 'postgres',
    user = 'postgres',
    password = 'pass',
    port = 5432
)
cur = conn.cursor()

make_games_table(cur, df)
make_trends_table(cur)
process_game_rows(cur, df)

conn.commit()
cur.close()
conn.close()

end_time = time.time()
print(f'TOTAL TIME: {end_time - start_time}\n')
