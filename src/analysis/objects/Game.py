#################################################################################
# Game.py                                                                       #
#                                                                               #
# This object will provide information about a specific game. It will give any  #
# information about the game that is available before the game actually happens #
# such as basic info about date/time, spread, and total info. The toString      #
# method prints a dictionary style string of keys and attributes.               #
#################################################################################
import itertools
from datetime import datetime
from src.analysis.objects.conditions.GameCondition import GameCondition
from src.analysis.objects.conditions.SpreadCondition import SpreadCondition
from src.analysis.objects.conditions.TotalCondition import TotalCondition
from src.analysis.objects.conditions.SeasonCondition import SeasonCondition
from src.analysis.objects.conditions.TrendCondition import TrendCondition
import src.analysis.helpers.constants as constants

class Game:

    # Game info
    season = None
    date = None
    day_of_week = None
    month = None
    day = None
    year = None
    home_team = None
    home_division = None
    away_team = None
    away_division = None
    divisional = None
    playoff = None

    # Betting info
    home_spread = None
    away_spread = None
    spread = None
    home_favorite = None
    home_underdog = None
    away_favorite = None
    away_underdog = None
    pk = None
    total = None

    # Conditions
    game_conditions = None
    spread_conditions = None
    total_conditions = None
    season_conditions = None

    def __init__(self, season, date, home_team, away_team, home_spread, away_spread, total):
        # Game info
        self.season = season
        self.date = date
        self.day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        self.month = int(date[5:7])
        self.day = int(date[8:10])
        self.year = int(date[:4])
        self.home_team = home_team
        self.home_division = self.get_division(home_team)
        self.away_team = away_team
        self.away_division = self.get_division(away_team)
        self.divisional = self.home_division == self.away_division
        self.playoff = False

        # Betting info
        self.home_spread = home_spread
        self.away_spread = away_spread
        self.spread = home_spread if home_spread > 0 else away_spread
        self.pk = self.spread == 0
        self.home_favorite = True if home_spread < 0 else False
        self.home_underdog = True if home_spread > 0 else False
        self.away_favorite = True if away_spread < 0 else False
        self.away_underdog = True if away_spread > 0 else False
        self.total = total

        # Conditions
        self.game_conditions = self.get_game_conditions()
        self.spread_conditions = self.get_spread_conditions()
        self.total_conditions = self.get_total_conditions()
        self.season_conditions = self.get_season_conditions()
        self.condition_combinations = self.get_condition_combinations(
                                        self.game_conditions, 
                                        self.spread_conditions, 
                                        self.total_conditions, 
                                        self.season_conditions)

    def get_division(self, team):
        divisions = {
            'AFC East': ['New York Jets', 'Miami Dolphins', 'New England Patriots', 'Buffalo Bills'],
            'AFC North': ['Baltimore Ravens', 'Pittsburgh Steelers', 'Cincinnati Bengals', 'Cleveland Browns'],
            'AFC West': ['Kansas City Chiefs', 'Denver Broncos', 'Los Angeles Chargers', 'Las Vegas Raiders'],
            'AFC South': ['Jacksonville Jaguars', 'Indianapolis Colts', 'Tennessee Titans', 'Houston Texans'],
            'NFC East': ['Washington Commanders', 'Philadelphia Eagles', 'Dallas Cowboys', 'New York Giants'],
            'NFC North': ['Detroit Lions', 'Green Bay Packers', 'Minnesota Vikings', 'Chicago Bears'],
            'NFC West': ['San Francisco 49ers', 'Seattle Seahawks', 'Arizona Cardinals', 'Los Angeles Rams'],
            'NFC South': ['New Orleans Saints', 'Atlanta Falcons', 'Carolina Panthers', 'Tampa Bay Buccaneers']
        }

        for division, teams in divisions.items():
            if team in teams:
                return division
            
        return 'TEAM NOT IN DIVISION'
    
    def get_game_conditions(self):
        game_conditions = [
            GameCondition('Season Type', self.playoff),
            GameCondition('Month', self.month),
            GameCondition('Day', self.day_of_week),
            GameCondition('Divisional?', self.divisional)
        ]

        return game_conditions
    
    # This function gets all the possible conditions for spreads based on the given game
    # This includes:
    # The spread of the given game
    # Every spread up to the given spread or higher
    # Every spread above the given spread up to the highest possible or lower
    def get_spread_conditions(self):
        spread_conditions = []
        spread_conditions.append(SpreadCondition(self.spread, 'equal'))
        
        current_spread = 1.0
        max_spread = constants.MAX_SPREAD
        while current_spread <= max_spread:
            if current_spread <= self.spread:
                spread_conditions.append(SpreadCondition(current_spread, 'more'))
            if current_spread >= self.spread:
                spread_conditions.append(SpreadCondition(current_spread, 'less'))
            current_spread += 1.0

        return spread_conditions

    # This function gets all the possible conditions for totals based on the given game
    # This includes:
    # The total of the given game
    # Every total up to the given total or higher
    # Every total above the given total up to the highest possible or lower
    def get_total_conditions(self):
        total_conditions = []
        total_conditions.append(TotalCondition(self.total, 'equal'))
        
        current_total = constants.MIN_TOTAL
        max_total = constants.MAX_TOTAL
        while current_total <= max_total:
            if current_total <= self.total:
                total_conditions.append(TotalCondition(current_total, 'more'))
            if current_total >= self.total:
                total_conditions.append(TotalCondition(current_total, 'less'))
            current_total += 1.0

        return total_conditions
    
    # This function gets all the possible conditions for all possible seasons
    # This includes:
    # The current season
    # Every season up through the current season starting in 2006-2007 season
    def get_season_conditions(self):
        season_conditions = []
        current_season = constants.OLDEST_SEASON
        
        while current_season <= self.season:
            start_year, end_year = current_season.split('-')
            season_conditions.append(SeasonCondition(f'{start_year}-{end_year}', self.season))
            start_year = int(start_year)
            end_year = int(end_year)
            start_year += 1
            end_year += 1
            current_season = f"{start_year}-{end_year}"

        return season_conditions
    
    # This function will get all possible condition combinations for this game
    # Each combination will include:
    # Any combination of any number of game conditions (including none)
    # 0 or 1 spread condition
    # 0 or 1 total condition
    # 0 or 1 season condition
    # And will be placed into a TrendCondition object and added to the list
    def get_condition_combinations(self, game_conditions, spread_conditions, total_conditions, season_conditions):
        all_combinations = []

        # Iterate over game_combinations
        for r in range(len(game_conditions) + 1):
            game_combination_tuples = itertools.combinations(game_conditions, r)
            game_combinations = [list(combination) for combination in game_combination_tuples]
            for game_combination in game_combinations:
                for spread_condition in [None] + spread_conditions:
                    for total_condition in [None] + total_conditions:
                        for season_condition in [None] + season_conditions:
                            condition = TrendCondition(
                                game_combination,
                                spread_condition,
                                total_condition,
                                season_condition
                            )
                            all_combinations.append(condition)

        return all_combinations

    def __str__(self):
        result = ""
        for attr, value in vars(self).items():
            if isinstance(value, list):
                result += f'{attr}:\n'
                for elem in value:
                    result += f'  {elem},\n'
            else:
                result += f'{attr}: {value}\n'
        return result
    