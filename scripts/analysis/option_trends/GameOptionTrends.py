#################################################################################
# GameOptionTrends.py                                                           #
#                                                                               #
# This file calculates the record for trends that have to do with all possible  #
# combinations of information about the given game. It then gets all possible   #
# combinations of including and not including these game info options and       #
# creates dataframes matching the criteria of these combinations. Then it uses  #
# BasicTrends to find all basic trends for the combination dataframes. The      #  
# toString method prints all of these records on their own line.                #  
#                                                                               #
# Examples:                                                                     #
# - games where the day of the week is Sunday and the month is 10               #
# - games where the day of the week is Sunday and it is the regular season      #
# - games where the day of the week is Sunday and it is the regular season and  #
#   it is a divisional game                                                     # 
# - games where the month is 10 and it is the regular season and it is a        # 
#   divisional game                                                             #
#################################################################################
from analysis.basic_trends.BasicTrends import BasicTrends
from analysis.objects.NamedDataframe import NamedDataframe
from analysis.helpers.filter_functions import *
import pandas as pd
from itertools import combinations
from datetime import datetime

class GameOptionTrends:

    named_df = None
    df = None

    game = None
    day_of_week = None
    month = None
    playoff = None
    divisional = None

    trends = None

    def __init__(self, named_df, game):
        self.named_df = named_df
        self.df = self.named_df.df
        self.game = game
        self.day_of_week = game.day_of_week
        self.month = game.month
        self.playoff = 'Y' if game.playoff == True else 'N'
        self.divisional = 'Y' if game.divisional == True else 'N'
        self.trends = self.get_option_combination_trends()
    
    # This function gets all possible combinations of the options that
    # can only be one thing or nothing. It results in 2^n - 1 combos
    # where n is the number of options you can toggle
    def get_option_combinations(self):
        options = {
            'Day of Week': self.day_of_week,
            'Month': self.month,
            'Playoff Game?': self.playoff,
            'Divisional Game?': self.divisional
        }

        all_option_combinations = []
        for r in range(1, len(options) + 1):
            for combo in combinations(options.keys(), r):
                option_combo = {key: options[key] for key in combo}
                all_option_combinations.append(option_combo)

        return all_option_combinations

    # This function gets the dataframe for each combination, so that the 
    # trends can then be analyzed from each dataframe in the list
    def get_option_combination_dataframes(self):
        option_combinations = self.get_option_combinations()
        option_combination_dataframes = []

        for option_combo in option_combinations:
            option_combo_string = 'games where '
            option_combo_length = len(option_combo)
            options_visited = 0
            for option in option_combo:
                options_visited += 1
                if option == 'Day of Week':
                    option_combo_string += f'the day of the week is {option_combo[option]} '
                elif option == 'Month':
                    option_combo_string += f'the month is {option_combo[option]} '
                elif option == 'Divisional Game?' and option_combo[option] == 'Y':
                    option_combo_string += f'it is a divisional game '
                elif option == 'Divisional Game?' and option_combo[option] == 'N':
                    option_combo_string += f'it is not a divisional game '
                elif option == 'Playoff Game?' and option_combo[option] == 'Y':
                    option_combo_string += f'it is the playoffs '
                elif option == 'Playoff Game?' and option_combo[option] == 'N':
                    option_combo_string += f'it is the regular season '

                if options_visited < option_combo_length:
                    option_combo_string += 'and '
    
            option_combo_dataframe = filter_dataframe_by_values(self.df, option_combo)
            named_option_combo_dataframe = NamedDataframe(option_combo_dataframe, option_combo_string)
            option_combination_dataframes.append(named_option_combo_dataframe)

        return option_combination_dataframes
    
    # This function gets all trends from each of the dataframes and adds them to
    # the object's list of trends
    def get_option_combination_trends(self):
        option_combo_trends = []
        option_combination_dataframes = self.get_option_combination_dataframes()

        for df in option_combination_dataframes:
            trends = BasicTrends(df, self.game).trends
            option_combo_trends += trends

        return option_combo_trends
    
    # toString method
    def __str__(self):
        returner = ''
        for record in self.trends:
            returner += str(record) + '\n'
        return returner