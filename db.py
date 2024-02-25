import psycopg2
import pandas as pd
from src.objects.Game import Game

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
        'Overtime?', 'Neutral Venue?', 'Notes'
    ], inplace = True)

    # Replace 
    df.rename(columns={
        'Home Line Close': 'Home Spread', 
        'Total Score Close': 'Total',
        'Playoff Game?': 'Season Phase',
        'Neutral Venue?': 'Neutral Venue'
    }, inplace=True)

    # Replace Y and N (or NaN) with True and False
    df.fillna(False, inplace=True)
    df.replace('Y', True, inplace=True)

    # Replace True and False with Regular Season and Playoffs for season type
    df['Season Phase'] = df['Season Phase'].replace(True, 'Playoffs')
    df['Season Phase'] = df['Season Phase'].replace(False, 'Regular Season')

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
            phase VARCHAR(14),
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

    # Add Games to `games` table in database
    games = []
    for _, row in df.iterrows():
        game = Game(
            row['Date'], 
            row['Season Phase'], 
            row['Home Team'], row['Away Team'],
            row['Home Score'], row['Away Score'],
            row['Home Spread'],
            row['Total']
        )
        games.append(game.to_dict())

    sql_insert = '''
        INSERT INTO games VALUES (
            %(id)s, %(id_string)s, %(date)s, %(month)s, %(day)s, %(year)s, %(season)s, 
            %(day_of_week)s, %(phase)s, %(home_team)s, %(home_abbreviation)s, %(home_division)s, 
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
    cur.executemany(sql_insert, games)

def make_trends_table(cur):
    cur.execute('''
       DROP TABLE IF EXISTS trends         
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            id VARCHAR(64),
            id_string VARCHAR(250),
            category VARCHAR(25),
            phase VARCHAR(15),
            month VARCHAR(10),
            day_of_week VARCHAR(8),
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

    trends = {}
    for _, row in df.iterrows():
        game = Game(
            row['Date'], 
            row['Season Phase'], 
            row['Home Team'], row['Away Team'],
            row['Home Score'], row['Away Score'],
            row['Home Spread'],
            row['Total'], True
        )

        for trend in game.trends:
            trend_to_update = trends.get(trend.id)
            if trend_to_update is None:
                trends[trend.id] = trend
                trend_to_update = trends[trend.id]
            trend_to_update.update_record(game)

    trends_arr = [trend.to_tuple() for trend in trends.values()]
    sql_insert = '''
        INSERT INTO trends (id, id_string, category, phase, month, day_of_week, divisional, spread, total, seasons, wins, losses, pushes, total_games, win_percentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cur.executemany(sql_insert, trends_arr)

#################
### EXECUTION ###
#################

df = pd.read_excel('datafiles/excel/nfl.xlsx')

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

# Commit database changes
conn.commit()

# Close cursor and connection
cur.close()
conn.close()
