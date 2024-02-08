#################################################################################
# SpreadTrends.py                                                               #
#                                                                               #
# This file calculates the record for trends that have to do with spreads. It   # 
# takes a game and named dataframe then calculates the record for home/away     # 
# teams, favorite/not favorite, home favorite/away not favorite, and                #
# away favorite/home not favorite against the spread, based on the specifics of   # 
# the game. It then stores these records in an array called trends. The         # 
# toString method prints all of these records on their own line.                #                              
#################################################################################
from src.analysis.helpers.filter_functions import *
from src.analysis.objects.Record import Record
import pandas as pd

class SpreadTrends:

    home_covers = None
    away_covers = None

    favorite_covers = None
    underdog_covers = None

    home_favorite_covers = None
    away_underdog_covers = None

    away_favorite_covers = None
    home_underdog_covers = None

    trends = None

    def __init__(self, named_df, game):
        self.home_covers = self.get_home_covers(named_df)
        self.away_covers = self.get_away_covers(named_df)
        self.favorite_covers = self.get_favorite_covers(named_df)
        self.underdog_covers = self.get_underdog_covers(named_df)
        if game.home_favorite == True:
            self.home_favorite_covers = self.get_home_favorite_covers(named_df)
            self.away_underdog_covers = self.get_away_underdog_covers(named_df)
            self.trends = [
                self.home_covers, self.away_covers, 
                self.favorite_covers, self.underdog_covers, 
                self.home_favorite_covers, self.away_underdog_covers
            ]
        elif game.away_favorite == True:
            self.away_favorite_covers = self.get_away_favorite_covers(named_df)
            self.home_underdog_covers = self.get_home_underdog_covers(named_df)
            self.trends = [
                self.home_covers, self.away_covers, 
                self.favorite_covers, self.underdog_covers, 
                self.away_favorite_covers, self.home_underdog_covers
            ]


    ###########################################
    #           Home/Away Calculators         # 
    ###########################################     
    def get_home_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Spread Push?': 'N', 'Neutral Venue?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        home_covers = (df_clean['Home Cover?'] == 'Y').sum()
        home_not_covers = (df_clean['Home Cover?'] == 'N').sum()
        home_pushes = (df['Spread Push?'] == 'Y').sum()
        home_covers = Record(f'Home Team Record ATS in {identifiers}', home_covers, home_not_covers, home_pushes)

        return home_covers

    def get_away_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Spread Push?': 'N', 'Neutral Venue?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        away_covers = (df_clean['Away Cover?'] == 'Y').sum()
        away_not_covers = (df_clean['Away Cover?'] == 'N').sum()
        away_pushes = (df['Spread Push?'] == 'Y').sum()
        away_covers = Record(f'Away Team Record ATS in {identifiers}', away_covers, away_not_covers, away_pushes)

        return away_covers


    ###########################################
    #       favorite/Not favorite Calculators   # 
    ###########################################
    def get_favorite_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'PK?': 'N'}
        df_no_pk = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Spread Push?': 'N', 'PK?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        favorite_covers = (df_clean['Favored Cover?'] == 'Y').sum()
        favorite_not_covers = (df_clean['Favored Cover?'] == 'N').sum()
        favorite_pushes = (df_no_pk['Spread Push?'] == 'Y').sum()
        favorite_covers = Record(f'Favorite Record ATS in {identifiers}', favorite_covers, favorite_not_covers, favorite_pushes)

        return favorite_covers
    
    def get_underdog_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'PK?': 'N'}
        df_no_pk = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Spread Push?': 'N', 'PK?': 'N'}
        df_clean = filter_dataframe_by_values(df, filter_dict)

        underdog_covers = (df_clean['Not Favored Cover?'] == 'Y').sum()
        underdog_not_covers = (df_clean['Not Favored Cover?'] == 'N').sum()
        underdog_pushes = (df_no_pk['Spread Push?'] == 'Y').sum()
        underdog_covers = Record(f'Underdog Record ATS in {identifiers}', underdog_covers, underdog_not_covers, underdog_pushes)

        return underdog_covers


    ###########################################
    # Home/Away favorite/Not favorite Calculators # 
    ###########################################
    def get_home_favorite_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Favored?': 'Y'}
        home_favorite_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Favored?': 'Y', 'Spread Push?': 'N'}
        home_favorite_df_clean = filter_dataframe_by_values(df, filter_dict)

        home_favorite_covers = (home_favorite_df_clean['Home Favored Cover?'] == 'Y').sum()
        home_favorite_not_covers = (home_favorite_df_clean['Home Favored Cover?'] == 'N').sum()
        home_favorite_pushes = (home_favorite_df['Spread Push?'] == 'Y').sum()
        home_favorite_covers = Record(f'Home Favorite Record ATS in {identifiers}', home_favorite_covers, home_favorite_not_covers, home_favorite_pushes)

        return home_favorite_covers

    def get_away_underdog_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Not Favored?': 'Y'}
        away_underdog_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Not Favored?': 'Y', 'Spread Push?': 'N'}
        away_underdog_df_clean = filter_dataframe_by_values(df, filter_dict)

        away_underdog_covers = (away_underdog_df_clean['Away Not Favored Cover?'] == 'Y').sum()
        away_underdog_not_covers = (away_underdog_df_clean['Away Not Favored Cover?'] == 'N').sum()
        away_underdog_pushes = (away_underdog_df['Spread Push?'] == 'Y').sum()
        away_underdog_covers = Record(f'Away Underdog Record ATS in {identifiers}', away_underdog_covers, away_underdog_not_covers, away_underdog_pushes)

        return away_underdog_covers
    
    def get_away_favorite_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Favored?': 'Y'}
        away_favorite_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Away Favored?': 'Y', 'Spread Push?': 'N'}
        away_favorite_df_clean = filter_dataframe_by_values(df, filter_dict)

        away_favorite_covers = (away_favorite_df_clean['Away Favored Cover?'] == 'Y').sum()
        away_favorite_not_covers = (away_favorite_df_clean['Away Favored Cover?'] == 'N').sum()
        away_favorite_pushes = (away_favorite_df['Spread Push?'] == 'Y').sum()
        away_favorite_covers = Record(f'Away Favorite Record ATS in {identifiers}', away_favorite_covers, away_favorite_not_covers, away_favorite_pushes)

        return away_favorite_covers

    def get_home_underdog_covers(self, named_df):
        df = named_df.df
        identifiers = named_df.description

        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Not Favored?': 'Y'}
        home_underdog_df = filter_dataframe_by_values(df, filter_dict)
        filter_dict = {'Neutral Venue?': 'N', 'PK?': 'N', 'Home Not Favored?': 'Y', 'Spread Push?': 'N'}
        home_underdog_df_clean = filter_dataframe_by_values(df, filter_dict)

        home_underdog_covers = (home_underdog_df_clean['Home Not Favored Cover?'] == 'Y').sum()
        home_underdog_not_covers = (home_underdog_df_clean['Home Not Favored Cover?'] == 'N').sum()
        home_underdog_pushes = (home_underdog_df['Spread Push?'] == 'Y').sum()
        home_underdog_covers = Record(f'Home Underdog Record ATS in {identifiers}', home_underdog_covers, home_underdog_not_covers, home_underdog_pushes)

        return home_underdog_covers


    ###########################################
    #                ToString                 # 
    ###########################################

    def __str__(self):
        returner = ''
        for cover in self.trends:
            returner += str(cover) + '\n'
        return returner 