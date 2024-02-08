#################################################################################
# BettingOptionTrends.py                                                        #
#                                                                               #
# This file calculates the record for trends that have to do with all possible  #
# combinations of betting information about the given game. It then gets all    #
# possible combinations up to and including these betting info options and      #
# creates dataframes matching the criteria of these combinations. Then it uses  #
# BasicTrends to find all basic trends for the combination dataframes.          #  
# The toString method prints all of these records on their own line.            #    
#                                                                               #
# Examples:                                                                     #
# - games where the spread is 7                                                 #
# - games where the total is 56.5 or lower                                      #
# - games where the spread is 3.0 or more and the total is 52.0 or lower        #          
#################################################################################
from src.analysis.basic_trends.BasicTrends import BasicTrends
from src.analysis.objects.NamedDataframe import NamedDataframe
from src.analysis.helpers.filter_functions import *
import pandas as pd

class BettingOptionTrends:
    
    named_df = None
    df = None
    
    game = None
    spread = None
    total = None

    trends = None

    def __init__(self, named_df, game):
        self.named_df = named_df
        self.df = self.named_df.df
        self.game = game
        self.spread = game.spread
        self.total = game.total
        self.trends = self.get_all_trends()

    # This function creates dataframes with the following criteria:
    #   - The spread is exactly the spread given
    #   - The spread is at every number at least 1 or higher up to the given spread by 1.0 (1.0, 2.0, 3.0)
    def get_spread_dataframes(self, df, spread):
        spread_dataframes = []

        # Get rows where spread is exactly spread passed
        filtered_spread_df = df[df['Line Open'] == spread]
        named_spread_df = NamedDataframe(filtered_spread_df, f'games where the spread is {spread} ')
        spread_dataframes.append(named_spread_df)

        # Go through every spread from 1 up to spread passed, by 0.5
        min_spread = 1.0
        while min_spread <= spread:
            filtered_spread_df = df[df['Line Open'] >= min_spread]

            named_spread_df = NamedDataframe(filtered_spread_df, f'games where the spread is {min_spread} or more ')
            spread_dataframes.append(named_spread_df)
            
            min_spread += 1.0
        
        return spread_dataframes
    
    # This function gets the dataframes created in the get_spread_dataframes() method
    # and finds all the generic trends for each of the dataframes and returns a list of those trends
    def get_spread_trends(self):
        spread_trends = []
        spread_dataframes = self.get_spread_dataframes(self.df, self.spread)

        for df in spread_dataframes:
            trends = BasicTrends(df, self.game).trends
            spread_trends += trends

        return spread_trends

    # This function creates dataframes with the following criteria:
    #   - The total is exactly the total given
    #   - The total is at least every number from the lowest total ever to the given total by 1.0 (31.0, 32.0, 33.0, etc)
    #   - The total is at most every number from the highest total ever to the given total by -1.0 (63.0, 62.0, 61.0, etc)
    def get_total_dataframes(self, df, total):
        total_dfs = []

        # Get rows where total is exactly total passed
        filtered_total_df = df[df['Total Score Open'] == total]
        named_total_df = NamedDataframe(filtered_total_df, f'games where the total is {total} ')
        total_dfs.append(named_total_df)

        # Go through every total from the lowest possible total up to total passed, by 0.5
        min_total = df['Total Score Open'].min()
        while min_total <= total:
            filtered_total_df = df[df['Total Score Open'] >= min_total]

            named_total_df = NamedDataframe(filtered_total_df, f'games where the total is {min_total} or higher ')
            total_dfs.append(named_total_df)

            min_total += 1.0

        # Go through every total from the highest possible total down to total passed, by -0.5
        max_total = df['Total Score Open'].max()
        while max_total >= total:
            filtered_total_df = df[df['Total Score Open'] <= max_total]

            named_total_df = NamedDataframe(filtered_total_df, f'games where the total is {max_total} or lower ')
            total_dfs.append(named_total_df)

            max_total -= 1.0

        return total_dfs
    
    # This function gets the dataframes created in the get_total_dataframes() method
    # and finds all the generic trends for each of the dataframes and returns a list of those trends
    def get_total_trends(self):
        total_trends = []
        total_dataframes = self.get_total_dataframes(self.df, self.total)

        for df in total_dataframes:
            trends = BasicTrends(df, self.game).trends
            total_trends += trends

        return total_trends

    # This function combines the get_spread_dataframes() and get_total_dataframes() methods
    # so it will get all possible spreads up to the given spread for every possible total
    # up to and down to the given total. It will also get when the spread is exactly the
    # spread given and the total is exactly the total given
    def get_spread_and_total_dataframes(self, df, spread, total):
        spread_and_total_dfs = []

        spread_dataframes = self.get_spread_dataframes(df, spread)
        
        for spread_df in spread_dataframes:
            spread_description = spread_df.description
            spread_and_total_dataframes = self.get_total_dataframes(spread_df.df, total)

            for spread_and_total_df in spread_and_total_dataframes:
                total_description = spread_and_total_df.description[12:]
                spread_and_total_df.description = f'{spread_description}and {total_description}'
                spread_and_total_dfs.append(spread_and_total_df)

        return spread_and_total_dfs

    # This function gets the dataframes created in the get_spread_and_total_dataframes() method
    # and finds all the generic trends for each of the dataframes and returns a list of those trends
    def get_spread_and_total_trends(self):
        spread_and_total_trends = []
        spread_and_total_dataframes = self.get_spread_and_total_dataframes(self.df, self.spread, self.total)

        for df in spread_and_total_dataframes:
            trends = BasicTrends(df, self.game).trends
            spread_and_total_trends += trends

        return spread_and_total_trends
    
    def get_all_dataframes(self):
        spread_dataframes = self.get_spread_dataframes(self.df, self.spread)
        total_dataframes = self.get_total_dataframes(self.df, self.total)
        spread_and_total_dataframes = self.get_spread_and_total_dataframes(self.df, self.spread, self.total)

        return [spread_dataframes, total_dataframes, spread_and_total_dataframes]

    # This function gets all the trends calculated in the other methods. It places the following
    # resulting trends into one large trends list:
    #   - get_spread_trends()
    #   - get_total_trends()
    #   - get_spread_and_total_trends()
    def get_all_trends(self):
        all_trends = []

        spread_trends = self.get_spread_trends()
        total_trends = self.get_total_trends()
        spread_and_total_trends = self.get_spread_and_total_trends()

        all_trends += spread_trends
        all_trends += total_trends
        all_trends += spread_and_total_trends

        return all_trends

    def __str__(self):
        returner = ''
        for trend in self.trends:
            returner += str(trend) + '\n'
        return returner

