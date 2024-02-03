#################################################################################
# MoneylineTrends.py                                                            #
#                                                                               #
# This file calculates the record for trends that have to do with moneylines.   # 
# It takes a game and named dataframe then calculates the record for home/away  # 
# teams, favorite/underdogs, home favorites/away underdogs, and                 #
# away favorites/away underdogs straight up, based on the specifics of the      # 
# game. It then stores these records in an array called trends. The toString    # 
# method prints all of these records on their own line.                         #                              
#################################################################################
from src.analysis.helpers.filter_functions import *
from src.analysis.objects.Record import Record
import pandas as pd

class MoneylineTrends:

    home_record = None
    away_record = None

    favorite_record = None
    underdog_record = None

    home_favorite_record = None
    away_underdog_record = None

    away_favorite_record = None
    home_underdog_record = None

    trends = None

    def __init__(self, named_df, game):
        self.home_record = self.get_home_record(named_df)
        self.away_record = self.get_away_record(named_df)
        self.favorite_record = self.get_favorite_record(named_df)
        self.underdog_record = self.get_underdog_record(named_df)
        if game.home_favorite == True:
            self.home_favorite_record = self.get_home_favorite_record(named_df)
            self.away_underdog_record = self.get_away_underdog_record(named_df)
            self.trends = [
                self.home_record, self.away_record, 
                self.favorite_record, self.underdog_record,
                self.home_favorite_record, self.away_underdog_record
            ]
        elif game.away_favorite == True:
            self.away_favorite_record = self.get_away_favorite_record(named_df)
            self.home_underdog_record = self.get_home_underdog_record(named_df)
            self.trends = [
                self.home_record, self.away_record, 
                self.favorite_record, self.underdog_record,
                self.away_favorite_record, self.home_underdog_record
            ]


    ###########################################
    #           Home/Away Calculators         # 
    ###########################################     
    def get_home_record(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Tie?': 'N', 'Neutral Venue?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        home_wins = (df_clean['Home Team Win?'] == 'Y').sum()
        home_losses = (df_clean['Home Team Win?'] == 'N').sum()
        home_ties = (df['Tie?'] == 'Y').sum()
        home_record = Record(f'Home Team Record Straight Up in {identifiers}', home_wins, home_losses, home_ties)

        return home_record

    def get_away_record(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Tie?': 'N', 'Neutral Venue?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        away_wins = (df_clean['Away Team Win?'] == 'Y').sum()
        away_losses = (df_clean['Away Team Win?'] == 'N').sum()
        away_ties = (df['Tie?'] == 'Y').sum()
        away_record = Record(f'Away Team Record Straight Up in {identifiers}', away_wins, away_losses, away_ties)

        return away_record
    

    ###########################################
    #       Favorite/Underdog Calculators     # 
    ###########################################
    def get_favorite_record(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Equal Moneyline?': 'N'}
        df_no_equal_moneylines = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Tie?': 'N', 'Equal Moneyline?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        favorite_wins = (df_clean['Favorite Win?'] == 'Y').sum()
        favorite_losses = (df_clean['Favorite Win?'] == 'N').sum()
        favorite_ties = (df_no_equal_moneylines['Tie?'] == 'Y').sum()
        favorite_record = Record(f'Favorite Record Straight Up in {identifiers}', favorite_wins, favorite_losses, favorite_ties)

        return favorite_record
    
    def get_underdog_record(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Equal Moneyline?': 'N'}
        df_no_equal_moneylines = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Tie?': 'N', 'Equal Moneyline?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        underdog_wins = (df_clean['Underdog Win?'] == 'Y').sum()
        underdog_losses = (df_clean['Underdog Win?'] == 'N').sum()
        underdog_ties = (df_no_equal_moneylines['Tie?'] == 'Y').sum()
        underdog_record = Record(f'Underdog Record Straight Up in {identifiers}', underdog_wins, underdog_losses, underdog_ties)

        return underdog_record
    

    ###########################################
    # Home/Away Favorite/Underdog Calculators # 
    ###########################################
    def get_home_favorite_record(self, named_df): 
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Home Favorite?': 'Y'}
        home_favorites_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Home Favorite?': 'Y', 'Tie?': 'N'}
        home_favorites_df_clean = filter_dataframe_by_values(df, filter_dict)

        home_favorite_wins = (home_favorites_df_clean['Home Favorite Win?'] == 'Y').sum()
        home_favorite_losses = (home_favorites_df_clean['Home Favorite Win?'] == 'N').sum()
        home_favorite_ties = (home_favorites_df['Tie?'] == 'Y').sum()
        home_favorite_record = Record(f'Home Favorite Record Straight Up in {identifiers}', home_favorite_wins, home_favorite_losses, home_favorite_ties)

        return home_favorite_record

    def get_away_underdog_record(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Away Underdog?': 'Y'}
        away_underdogs_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Away Underdog?': 'Y', 'Tie?': 'N'}
        away_underdogs_df_clean = filter_dataframe_by_values(df, filter_dict)

        away_underdog_wins = (away_underdogs_df_clean['Away Underdog Win?'] == 'Y').sum()
        away_underdog_losses = (away_underdogs_df_clean['Away Underdog Win?'] == 'N').sum()
        away_underdog_ties = (away_underdogs_df['Tie?'] == 'Y').sum()
        away_underdog_record = Record(f'Away Underdog Record Straight Up in {identifiers}', away_underdog_wins, away_underdog_losses, away_underdog_ties)

        return away_underdog_record
    
    def get_away_favorite_record(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Away Favorite?': 'Y'}
        away_favorites_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Away Favorite?': 'Y', 'Tie?': 'N'}
        away_favorites_df_clean = filter_dataframe_by_values(df, filter_dict)

        away_favorite_wins = (away_favorites_df_clean['Away Favorite Win?'] == 'Y').sum()
        away_favorite_losses = (away_favorites_df_clean['Away Favorite Win?'] == 'N').sum()
        away_favorite_ties = (away_favorites_df['Tie?'] == 'Y').sum()
        away_favorite_record = Record(f'Away Favorite Record Straight Up in {identifiers}', away_favorite_wins, away_favorite_losses, away_favorite_ties)

        return away_favorite_record

    def get_home_underdog_record(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Home Underdog?': 'Y'}
        home_underdogs_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'Equal Moneyline?': 'N', 'Home Underdog?': 'Y', 'Tie?': 'N'}
        home_underdogs_df_clean = filter_dataframe_by_values(df, filter_dict)

        home_underdog_wins = (home_underdogs_df_clean['Home Underdog Win?'] == 'Y').sum()
        home_underdog_losses = (home_underdogs_df_clean['Home Underdog Win?'] == 'N').sum()
        home_underdog_ties = (home_underdogs_df['Tie?'] == 'Y').sum()
        home_underdog_record = Record(f'Home Underdog Record Straight Up in {identifiers}', home_underdog_wins, home_underdog_losses, home_underdog_ties)

        return home_underdog_record
    

    ###########################################
    #                ToString                 # 
    ###########################################

    def __str__(self):
        returner = ''
        for record in self.trends:
            returner += str(record) + '\n'
        return returner