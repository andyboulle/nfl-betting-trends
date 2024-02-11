#################################################################################
# TrendCondition.py                                                             #
#                                                                               #
# This object will define the specifics of a condition related to a trend. It   #
# combines the other types of conditions to define all the conditions necessary #
# for a trend.                                                                  #   
#                                                                               #
# The format for trend conditions is as follows:                                #
# - Any combination of any number of Game Conditions                            #
# - Either zero or one Spread Condition                                         #
# - Either zero or one Total Condition                                          #
# - Either zero or one Season Condition                                         #
#################################################################################
from src.analysis.objects.conditions.GameCondition import GameCondition
from src.analysis.objects.conditions.SpreadCondition import SpreadCondition
from src.analysis.objects.conditions.TotalCondition import TotalCondition
from src.analysis.objects.conditions.SeasonCondition import SeasonCondition

class TrendCondition:
    
    game_conditions = None
    spread_condition = None
    total_condition = None
    season_condition = None

    def __init__(self, game_conditions, spread_condition, total_condition, season_condition):
        self.game_conditions = game_conditions
        self.spread_condition = spread_condition
        self.total_condition = total_condition
        self.season_condition = season_condition

    def __str__(self):
        returner = '{{\n'

        returner += 'game_conditions: [\n'
        for condition in self.game_conditions:
            returner += f'{condition},\n'
        returner += ']\n'

        returner += f"spread_condition: {self.spread_condition}\n"
        returner += f"total_condition: {self.total_condition}\n"
        returner += f"season_condition: {self.season_condition}\n"

        return returner
        
