#################################################################################
# Trend.py                                                                      #
#                                                                               #
# This object will provide information about a trend. It takes a TrendCondition #
# object as a parameter and creates a description for the trend based off it,   #
# then makes a dictionary of empty records where the key is a string of the     #
# type of record (home favorite straight up, away ats, over, etc), and the      #
# value is the record itself. All records in the dictionary are empty, so they  #
# start with 0 wins, 0 losses, and 0 pushes.                                    #
#################################################################################
from src.analysis.objects.Record import Record

class Trend:

    conditions = None
    description = None
    records = None

    def __init__(self, conditions):
        self.conditions = conditions
        self.description = self.create_description(self.conditions)
        self.records = self.get_records()

    # This function will create the description for the trend
    # based off the conditions of the trend.
    # The order for description is:
    # spread condition, total condition, game conditions, season condition
    def create_description(self, conditions):
        description = ''
        description += self.get_spread_description(conditions.spread_condition) if conditions.spread_condition != None else ''
        description += self.get_total_description(conditions.total_condition) if conditions.total_condition != None else ''
        description += self.get_game_description(conditions.game_conditions) if conditions.game_conditions != None else ''
        description += self.get_season_description(conditions.season_condition) if conditions.season_condition != None else ''

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
    
    # This function creates empty records for every record type
    # (straight up, against the spread, totals)
    def get_records(self):
        records = {}
        record_categories = [
            'home straight up', 'away straight up', 'favorite straight up', 'underdog straight up',
            'home favorite straight up', 'away underdog straight up', 'away favorite straight up', 'home underdog straight up',
            'home ats', 'away ats', 'favorite ats', 'underdog ats',
            'home favorite ats', 'away underdog ats', 'away favorite ats', 'home underdog ats',
            'over', 'under'
        ]

        for category in record_categories:
            records[category] = Record(category, 0, 0, 0)

        return records
    
    def __str__(self):
        returner = ''
        returner += f'{self.description}:\n\n'
        for value in self.records.values():
            returner += f'{value}\n'

        return returner