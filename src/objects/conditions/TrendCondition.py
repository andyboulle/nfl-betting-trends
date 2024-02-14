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
from src.objects.conditions.GameCondition import GameCondition
from src.objects.conditions.SpreadCondition import SpreadCondition
from src.objects.conditions.TotalCondition import TotalCondition
from src.objects.conditions.SeasonCondition import SeasonCondition

class TrendCondition:
    
    description = None
    # game_conditions = None
    # spread_condition = None
    # total_condition = None
    # season_condition = None

    def __init__(self, game_conditions, spread_condition, total_condition, season_condition):
        # self.game_conditions = game_conditions
        # self.spread_condition = spread_condition
        # self.total_condition = total_condition
        # self.season_condition = season_condition
        self.description = self.create_description(game_conditions, spread_condition, total_condition, season_condition)

    def create_description(self, game_conditions, spread_condition, total_condition, season_condition):
        description = ''
        if game_conditions == None and spread_condition == None and total_condition == None and season_condition == None:
            description += 'No conditions'
        else:
            description += self.get_spread_description(spread_condition) if spread_condition != None else ''
            description += self.get_total_description(total_condition) if total_condition != None else ''
            description += self.get_game_description(game_conditions) if game_conditions != None else ''
            description += self.get_season_description(season_condition) if season_condition != None else ''
        return description
    
    def get_spread_description(self, spread_condition):
        description = ""
        description += f'\n the spread is {spread_condition.number}'
        if spread_condition.relation == 'less':
            description += ' or less'
        elif spread_condition.relation == 'more':
            description += ' or more'

        return description

    def get_total_description(self, total_condition):
        description = ""
        description += f'\n the total is {total_condition.number}'
        if total_condition.relation == 'less':
            description += ' or less'
        elif total_condition.relation == 'more':
            description += ' or more'

        return description
    
    def get_game_description(self, game_conditions):
        description = ""
        if len(game_conditions) > 0:
            for game_condition in game_conditions:
                condition = game_condition.condition
                value = game_condition.value
                if condition == 'Season Type':
                    description += f"\n it is the {'regular season' if value == 'Regular' else 'playoffs'}"
                elif condition == 'Month':
                    description += f'\n it is month {value}'
                elif condition == 'Day':
                    description += f'\n it is a {value}'
                elif condition == 'Divisional?':
                    description += f'\n it is a divisional game'

        return description
    
    def get_season_description(self, season_condition):
        description = f'\n since the {season_condition.season_since} season'
        return description
    
    def __str__(self):
        returner = '{\n'

        returner += f'\tdescription: {self.description}\n'
        returner += '\tgame_conditions: [\n'
        for condition in self.game_conditions:
            returner += f'\t\t{condition},\n'
        returner += '\t]\n'

        returner += f"\tspread_condition: {self.spread_condition}\n"
        returner += f"\ttotal_condition: {self.total_condition}\n"
        returner += f"\tseason_condition: {self.season_condition}\n"

        returner += '}\n'

        return returner
        
