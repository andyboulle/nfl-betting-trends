#################################################################################
# column_editor.py                                                              #
#                                                                               #
# This file will add columns necessary to do analysis on the data. It will add  #
# columns with information about the games themselves and the results of the    #
# games. It will also change decimal odds to american odds for all the columns. # 
#################################################################################
import pandas as pd
import numpy as np
from datetime import datetime

afc_east = ['New York Jets', 'Miami Dolphins', 'New England Patriots', 'Buffalo Bills']
afc_north = ['Baltimore Ravens', 'Pittsburgh Steelers', 'Cincinnati Bengals', 'Cleveland Browns']
afc_west = ['Kansas City Chiefs', 'Denver Broncos', 'Los Angeles Chargers', 'Las Vegas Raiders']
afc_south = ['Jacksonville Jaguars', 'Indianapolis Colts', 'Tennessee Titans', 'Houston Texans']
nfc_east = ['Washington Commanders', 'Philadelphia Eagles', 'Dallas Cowboys', 'New York Giants']
nfc_north = ['Detroit Lions', 'Green Bay Packers', 'Minnesota Vikings', 'Chicago Bears']
nfc_west = ['San Francisco 49ers', 'Seattle Seahawks', 'Arizona Cardinals', 'Los Angeles Rams']
nfc_south = ['New Orleans Saints', 'Atlanta Falcons', 'Carolina Panthers', 'Tampa Bay Buccaneers']

# Helper Functions
def round_to_nearest_multiple_of_5(num):
    return 5 * round(num / 5)

def decimal_to_american(decimal_odds):
    if decimal_odds < 2.0:
        american_odds = str(round_to_nearest_multiple_of_5(int(-100 / (decimal_odds - 1))))
    else:
        american_odds = '+' + str(round_to_nearest_multiple_of_5(int((decimal_odds - 1) * 100)))
    return american_odds

# Creates the following columns:
# Year
# Month
# Day
def create_time_columns(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Day of Week'] = df['Date'].dt.strftime('%A')
    return df


# Creates the following columns:
# Season
def create_season_column(df):
    df['Season'] = None

    for index, row in df.iterrows():
        year = int(row['Year'])
        if int(row['Month']) > 8:
            next_year = year + 1
            df.loc[index, 'Season'] = str(year) + '-' + str(next_year)
        else:
            prev_year = year - 1
            df.loc[index, 'Season'] = str(prev_year) + '-' + str(year)

    return df


# Creates the following columns:
# Home Division
# Away Division
# Divisional Game?
def create_division_columns(df):
    df['Home Division'] = None
    df['Away Division'] = None
    df['Divisional Game?'] = None
    
    for index, row in df.iterrows():
        home_team = row['Home Team']
        if home_team in afc_east:
            df.loc[index, 'Home Division'] = 'AFC East'
        elif home_team in afc_north:
            df.loc[index, 'Home Division'] = 'AFC North'
        elif home_team in afc_west:
            df.loc[index, 'Home Division'] = 'AFC West'
        elif home_team in afc_south:
            df.loc[index, 'Home Division'] = 'AFC South'
        elif home_team in nfc_east:
            df.loc[index, 'Home Division'] = 'NFC East'
        elif home_team in nfc_north:
            df.loc[index, 'Home Division'] = 'NFC North'
        elif home_team in nfc_west:
            df.loc[index, 'Home Division'] = 'NFC West'
        elif home_team in nfc_south:
            df.loc[index, 'Home Division'] = 'NFC South'

    for index, row in df.iterrows():
        away_team = row['Away Team']
        if away_team in afc_east:
            df.loc[index, 'Away Division'] = 'AFC East'
        elif away_team in afc_north:
            df.loc[index, 'Away Division'] = 'AFC North'
        elif away_team in afc_west:
            df.loc[index, 'Away Division'] = 'AFC West'
        elif away_team in afc_south:
            df.loc[index, 'Away Division'] = 'AFC South'
        elif away_team in nfc_east:
            df.loc[index, 'Away Division'] = 'NFC East'
        elif away_team in nfc_north:
            df.loc[index, 'Away Division'] = 'NFC North'
        elif away_team in nfc_west:
            df.loc[index, 'Away Division'] = 'NFC West'
        elif away_team in nfc_south:
            df.loc[index, 'Away Division'] = 'NFC South'

    for index, row in df.iterrows():
        if row['Home Division'] == row['Away Division']:
            df.loc[index, 'Divisional Game?'] = 'Y'
        else:
            df.loc[index, 'Divisional Game?'] = 'N'

    return df


# Creates the following columns:
# Total Score
# Home Spread Result
# Away Spread Result
def create_score_result_columns(df):
    df['Total Score'] = df['Home Score'] + df['Away Score']
    df['Home Spread Result'] = df['Away Score'] - df['Home Score']
    df['Away Spread Result'] = df['Home Score'] - df['Away Score']
    return df


# Creates the following columns:
# Tie?
# Winner
# Loser
# Home Team Win?
# Away Team Win?
def create_game_result_columns(df):
    df['Tie?'] = None
    df['Winner'] = None
    df['Loser'] = None
    df['Home Team Win?'] = None
    df['Away Team Win?'] = None

    for index, row in df.iterrows():
        home_score = df.loc[index, 'Home Score']
        away_score = df.loc[index, 'Away Score']
        home_team = df.loc[index, 'Home Team']
        away_team = df.loc[index, 'Away Team']
        if home_score == away_score:
            df.loc[index, 'Tie?'] = 'Y'
            df.loc[index, 'Winner'] = 'NEITHER'
            df.loc[index, 'Loser'] = 'NEITHER'
            df.loc[index, 'Home Team Win?'] = 'N'
            df.loc[index, 'Away Team Win?'] = 'N'
        else:
            df.loc[index, 'Tie?'] = 'N'
            if home_score > away_score:
                df.loc[index, 'Winner'] = home_team
                df.loc[index, 'Loser'] = away_team
                df.loc[index, 'Home Team Win?'] = 'Y'
                df.loc[index, 'Away Team Win?'] = 'N'
            else:
                df.loc[index, 'Winner'] = away_team
                df.loc[index, 'Loser'] = home_team
                df.loc[index, 'Home Team Win?'] = 'N'
                df.loc[index, 'Away Team Win?'] = 'Y'

    return df


# Create the following columns:
# Home Moneyline Odds
# Away Moneyline Odds
def create_moneyline_odds_columns(df):
    df['Home Moneyline Open'] = df['Home Odds Open'].apply(lambda odds: decimal_to_american(odds) if not pd.isna(odds) else odds)
    df['Away Moneyline Open'] = df['Away Odds Open'].apply(lambda odds: decimal_to_american(odds) if not pd.isna(odds) else odds)
    return df


# Create the following columns:
# Equal Moneyline
# Home Favorite?
# Home Underdog?
# Away Favorite?
# Away Underdog?
# Favorite Moneyline
# Underdog Moneyline
def create_favorite_underdog_columns(df):
    for index, row in df.iterrows():
        home_ml = int(row['Home Moneyline Open'][1:]) if '+' in row['Home Moneyline Open'] else int(row['Home Moneyline Open'])
        away_ml = int(row['Away Moneyline Open'][1:]) if '+' in row['Away Moneyline Open'] else int(row['Away Moneyline Open'])
        if home_ml == away_ml:
            df.loc[index, 'Equal Moneyline?'] = 'Y'
            df.loc[index, 'Home Favorite?'] = 'N'
            df.loc[index, 'Home Underdog?'] = 'N'
            df.loc[index, 'Away Favorite?'] = 'N'
            df.loc[index, 'Away Underdog?'] = 'N'
            df.loc[index, 'Favorite Moneyline'] = row['Home Moneyline Open']
            df.loc[index, 'Underdog Moneyline'] = row['Home Moneyline Open']
        else:
            df.loc[index, 'Equal Moneyline?'] = 'N'
            if home_ml < away_ml:
                df.loc[index, 'Home Favorite?'] = 'Y'
                df.loc[index, 'Home Underdog?'] = 'N'
                df.loc[index, 'Away Favorite?'] = 'N'
                df.loc[index, 'Away Underdog?'] = 'Y'
                df.loc[index, 'Favorite Moneyline'] = row['Home Moneyline Open']
                df.loc[index, 'Underdog Moneyline'] = row['Away Moneyline Open']
            else:
                df.loc[index, 'Home Favorite?'] = 'N'
                df.loc[index, 'Home Underdog?'] = 'Y'
                df.loc[index, 'Away Favorite?'] = 'Y'
                df.loc[index, 'Away Underdog?'] = 'N'
                df.loc[index, 'Favorite Moneyline'] = row['Away Moneyline Open']
                df.loc[index, 'Underdog Moneyline'] = row['Home Moneyline Open']
    return df


# Create the following columns:
# Favorite Win?
# Underdog Win?
# Home Favorite Win?
# Home Underdog Win?
# Away Favorite Win?
# Away Underdog Win?
def create_moneyline_result_columns(df):
    for index, row in df.iterrows():
        home_team = row['Home Team']
        away_team = row['Away Team']
        winner = row['Winner']
        tie = row['Tie?']
        # If there is a tie or no favorite/underdog, then everything is No
        if tie == True or row['Equal Moneyline?'] == 'NEITHER':
            df.loc[index, 'Favorite Win?'] = 'N'
            df.loc[index, 'Underdog Win?'] = 'N'
            df.loc[index, 'Home Favorite Win?'] = 'N'
            df.loc[index, 'Home Underdog Win?'] = 'N'
            df.loc[index, 'Away Favorite Win?'] = 'N'
            df.loc[index, 'Away Underdog Win?'] = 'N'
        # There is no tie and a favorite/underdog
        else:
            # Home team is the winner, so away team is loser
            if home_team == winner:
                # Home team is the favorite, so away team is underdog
                if row['Home Favorite?'] == 'Y':
                    df.loc[index, 'Favorite Win?'] = 'Y'
                    df.loc[index, 'Underdog Win?'] = 'N'
                    df.loc[index, 'Home Favorite Win?'] = 'Y'
                    df.loc[index, 'Home Underdog Win?'] = 'N'
                    df.loc[index, 'Away Favorite Win?'] = 'N'
                    df.loc[index, 'Away Underdog Win?'] = 'N'
                # Home team is the underdog, so away team is the favorite
                else:
                    df.loc[index, 'Favorite Win?'] = 'N'
                    df.loc[index, 'Underdog Win?'] = 'Y'
                    df.loc[index, 'Home Favorite Win?'] = 'N'
                    df.loc[index, 'Home Underdog Win?'] = 'Y'
                    df.loc[index, 'Away Favorite Win?'] = 'N'
                    df.loc[index, 'Away Underdog Win?'] = 'N'
            # Away team is the winner
            else:
                # Away team is the favorite, so home team is underdog
                if row['Away Favorite?'] == 'Y':
                    df.loc[index, 'Favorite Win?'] = 'Y'
                    df.loc[index, 'Underdog Win?'] = 'N'
                    df.loc[index, 'Home Favorite Win?'] = 'N'
                    df.loc[index, 'Home Underdog Win?'] = 'N'
                    df.loc[index, 'Away Favorite Win?'] = 'Y'
                    df.loc[index, 'Away Underdog Win?'] = 'N'
                # Away team is the underdog, so home team is favorite
                else:
                    df.loc[index, 'Favorite Win?'] = 'N'
                    df.loc[index, 'Underdog Win?'] = 'Y'
                    df.loc[index, 'Home Favorite Win?'] = 'N'
                    df.loc[index, 'Home Underdog Win?'] = 'N'
                    df.loc[index, 'Away Favorite Win?'] = 'N'
                    df.loc[index, 'Away Underdog Win?'] = 'Y'
    return df


# Create the following columns:
# Line Open
# PK?
def create_line_columns(df):
    df['Line Open'] = df[['Home Line Open', 'Away Line Open']].max(axis=1)
    df['PK?'] = None

    for index, row in df.iterrows():
        line = row['Home Line Open']
        if line == 0:
            df.loc[index, 'PK?'] = 'Y'
        else:
            df.loc[index, 'PK?'] = 'N'
    return df


# Create the following columns:
# Home Favored?
# Home Not Facored?
# Away Favored?
# Away Not Favored?
def create_favored_not_favored_columns(df):
    df['Home Favored?'] = None
    df['Home Not Favored?'] = None
    df['Away Favored?'] = None
    df['Away Not Favored?'] = None

    for index, row in df.iterrows():
        home_line = row['Home Line Open']
        if row['PK?'] == True:
            df.loc[index, 'Home Favored?'] = 'N'
            df.loc[index, 'Home Not Favored?'] = 'N'
            df.loc[index, 'Away Favored?'] = 'N'
            df.loc[index, 'Away Not Favored?'] = 'N'
        else:
            if home_line < 0:
                df.loc[index, 'Home Favored?'] = 'Y'
                df.loc[index, 'Home Not Favored?'] = 'N'
                df.loc[index, 'Away Favored?'] = 'N'
                df.loc[index, 'Away Not Favored?'] = 'Y'
            else:
                df.loc[index, 'Home Favored?'] = 'N'
                df.loc[index, 'Home Not Favored?'] = 'Y'
                df.loc[index, 'Away Favored?'] = 'Y'
                df.loc[index, 'Away Not Favored?'] = 'N'
    return df

# Create the following columns:
# Spread Push?
# Home Cover?
# Away Cover?
# Favored Cover?
# Not Favored Cover?
# Home Favored Cover?
# Home Not Favored Cover?
# Away Favored Cover?
# Away Not Favored Cover?
def create_spread_result_columns(df):
    df['Spread Push?'] = None
    df['Home Cover?'] = None
    df['Away Cover?'] = None
    df['Favored Cover?'] = None
    df['Not Favored Cover?'] = None
    df['Home Favored Cover?'] = None
    df['Home Not Favored Cover?'] = None
    df['Away Favored Cover?'] = None
    df['Away Not Favored Cover?'] = None

    for index, row in df.iterrows():
        home_line = row['Home Line Open']
        away_line = row['Away Line Open']
        home_result = row['Home Spread Result']
        away_result = row['Away Spread Result']

        # Line pushed
        if home_line == home_result:
            df.loc[index, 'Spread Push?'] = 'Y'
            df.loc[index, 'Home Cover?'] = 'N'
            df.loc[index, 'Away Cover?'] = 'N'
            df.loc[index, 'Favored Cover?'] = 'N'
            df.loc[index, 'Not Favored Cover?'] = 'N'
            df.loc[index, 'Home Favored Cover?'] = 'N'
            df.loc[index, 'Home Not Favored Cover?'] = 'N'
            df.loc[index, 'Away Favored Cover?'] = 'N'
            df.loc[index, 'Away Not Favored Cover?'] = 'N'
        # Spread did not push
        else:
            df.loc[index, 'Spread Push?'] = 'N'
            # Home team covers spread
            if home_result <= home_line:
                df.loc[index, 'Home Cover?'] = 'Y'
                df.loc[index, 'Away Cover?'] = 'N'
                # Home team was favored
                if row['Home Favored?'] == 'Y':
                    df.loc[index, 'Favored Cover?'] = 'Y'
                    df.loc[index, 'Not Favored Cover?'] = 'N'
                    df.loc[index, 'Home Favored Cover?'] = 'Y'
                    df.loc[index, 'Home Not Favored Cover?'] = 'N'
                    df.loc[index, 'Away Favored Cover?'] = 'N'
                    df.loc[index, 'Away Not Favored Cover?'] = 'N'
                # Home team was not favored
                else:
                    df.loc[index, 'Favored Cover?'] = 'N'
                    df.loc[index, 'Not Favored Cover?'] = 'Y'
                    df.loc[index, 'Home Favored Cover?'] = 'N'
                    df.loc[index, 'Home Not Favored Cover?'] = 'Y'
                    df.loc[index, 'Away Favored Cover?'] = 'N'
                    df.loc[index, 'Away Not Favored Cover?'] = 'N'
            # Away team covers spread
            else:
                df.loc[index, 'Home Cover?'] = 'N'
                df.loc[index, 'Away Cover?'] = 'Y'
                # Away team was favored
                if row['Away Favored?'] == 'Y':
                    df.loc[index, 'Favored Cover?'] = 'Y'
                    df.loc[index, 'Not Favored Cover?'] = 'N'
                    df.loc[index, 'Home Favored Cover?'] = 'N'
                    df.loc[index, 'Home Not Favored Cover?'] = 'N'
                    df.loc[index, 'Away Favored Cover?'] = 'Y'
                    df.loc[index, 'Away Not Favored Cover?'] = 'N'
                # Away team was not favored
                else:
                    df.loc[index, 'Favored Cover?'] = 'N'
                    df.loc[index, 'Not Favored Cover?'] = 'Y'
                    df.loc[index, 'Home Favored Cover?'] = 'N'
                    df.loc[index, 'Home Not Favored Cover?'] = 'N'
                    df.loc[index, 'Away Favored Cover?'] = 'N'
                    df.loc[index, 'Away Not Favored Cover?'] = 'Y'
    return df


# Create the following columns:
# Total Push?
# Over Hit?
# Under Hit?
def create_total_result_columns(df):
    df['Total Push?'] = None
    df['Over Hit?'] = None
    df['Under Hit?'] = None

    for index, row in df.iterrows():
        total_score = row['Total Score']
        total = row['Total Score Open']

        # Total pushed
        if total_score == total:
            df.loc[index, 'Total Push?'] = 'Y'
            df.loc[index, 'Over Hit?'] = 'N'
            df.loc[index, 'Under Hit?'] = 'N'
        # Total did not push
        else:
            df.loc[index, 'Total Push?'] = 'N'
            if total_score > total:
                df.loc[index, 'Over Hit?'] = 'Y'
                df.loc[index, 'Under Hit?'] = 'N'
            else:
                df.loc[index, 'Over Hit?'] = 'N'
                df.loc[index, 'Under Hit?'] = 'Y'
    return df


# Rearranges columns in desired order
def reorder_columns(df):
    new_order = [
        'Season','Date','Day of Week','Month','Day','Year',
        'Home Team','Home Division','Away Team','Away Division',
        'Home Score','Away Score','Total Score','Home Spread Result','Away Spread Result','Winner','Loser',
        'Divisional Game?','Tie?','Overtime?','Playoff Game?','Neutral Venue?',
        'Home Moneyline Open','Away Moneyline Open','Favorite Moneyline', 'Underdog Moneyline', 'Equal Moneyline?',
        'Home Favorite?','Home Underdog?','Away Favorite?','Away Underdog?',
        'Home Team Win?','Away Team Win?','Favorite Win?','Underdog Win?','Home Favorite Win?','Home Underdog Win?','Away Favorite Win?','Away Underdog Win?',
        'Line Open', 'Home Line Open','Away Line Open','PK?','Home Favored?','Home Not Favored?','Away Favored?','Away Not Favored?', 'Spread Push?',
        'Home Cover?','Away Cover?','Favored Cover?','Not Favored Cover?','Home Favored Cover?','Home Not Favored Cover?','Away Favored Cover?','Away Not Favored Cover?',
        'Total Score Open','Total Push?','Over Hit?','Under Hit?'
    ]
    df = df[new_order]
    return df


def edit_columns(df):
    df = create_time_columns(df)
    df = create_season_column(df)
    df = create_division_columns(df)
    df = create_score_result_columns(df)
    df = create_game_result_columns(df)
    df = create_moneyline_odds_columns(df)
    df = create_favorite_underdog_columns(df)
    df = create_moneyline_result_columns(df)
    df = create_line_columns(df)
    df = create_favored_not_favored_columns(df)
    df = create_spread_result_columns(df)
    df = create_total_result_columns(df)
    df = reorder_columns(df)
    return df
