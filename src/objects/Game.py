import itertools
from datetime import datetime
import src.constants as constants
from src.objects.conditions.GameCondition import GameCondition
from src.objects.conditions.SpreadCondition import SpreadCondition
from src.objects.conditions.TotalCondition import TotalCondition
from src.objects.conditions.SeasonCondition import SeasonCondition

class Game:

    # How the game will be selected from database
    id = None

    # Game info
    date = None
    month = None
    day = None
    year = None
    season = None
    day_of_week = None
    phase = None

    # Team info
    home_team = None
    home_abbreviation = None
    home_division = None
    away_team = None
    away_abbreviation = None
    away_divison = None
    divisional = None

    # Score info
    home_score = None
    away_score = None
    combined_score = None
    tie = None
    winner = None
    loser = None

    # Betting info
    home_spread = None
    home_spread_result = None
    away_spread = None
    away_spread_result = None
    spread_push = None
    spread = None
    pk = None
    total = None
    total_push = None

    # Home/Away Favorite/Underdog info
    home_favorite = None
    away_underdog = None
    away_favorite = None
    home_underdog = None

    # Win Results info
    home_win = None
    away_win = None
    favorite_win = None
    underdog_win = None
    home_favorite_win = None
    away_underdog_win = None
    away_favorite_win = None
    home_underdog_win = None

    # Cover Results info
    home_cover = None
    away_cover = None
    favorite_cover = None
    underdog_cover = None
    home_favorite_cover = None
    away_underdog_cover = None
    away_favorite_cover = None
    home_underdog_cover = None

    # Total Results info
    over_hit = None
    under_hit = None

    # Conditions info
    conditions = None

    def __init__(self, date, season_phase, home_team, away_team, home_score, away_score, home_spread, total):
        # Game info
        self.date = date
        self.month = datetime.strptime(date.split('-')[1], '%m').strftime('%B')
        self.day = date.split('-')[2]
        self.year = date.split('-')[0]
        self.season = f'{self.year}-{int(self.year) + 1}' if int(date.split('-')[1]) > 8 else f'{int(self.year) - 1}-{self.year}'
        self.day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        self.phase = season_phase if season_phase == "Playoffs" else "Regular Season"

        # Team info
        self.home_team = home_team if home_team in constants.TEAMS else ValueError(f'{home_team} not a valid team')
        self.home_abbreviation = constants.ABBREVIATIONS[home_team]
        self.home_division = self.get_division(home_team)
        self.away_team = away_team if away_team in constants.TEAMS else ValueError(f'{away_team} not a valid team')
        self.away_abbreviation = constants.ABBREVIATIONS[away_team]
        self.away_division = self.get_division(away_team)
        self.divisional = self.home_division == self.away_division

        # Score info
        self.home_score = home_score
        self.away_score = away_score
        self.combined_score = home_score + away_score
        self.tie = home_score == away_score
        if self.tie == True:
            self.winner = None
            self.loser = None
        else:
            self.winner = home_team if home_score > away_score else away_team
            self.loser = home_team if home_score < away_score else away_team

        # Betting info
        self.home_spread = home_spread
        self.home_spread_result = away_score - home_score
        self.away_spread = home_spread * -1.0
        self.away_spread_result = home_score - away_score
        self.spread_push = self.home_spread_result == self.home_spread
        self.spread = max(self.home_spread, self.away_spread)
        self.pk = self.spread == 0.0
        self.total = total
        self.total_push = self.total == self.combined_score

        # Home/Away Favorite/Underdog info
        self.home_favorite = home_spread < 0
        self.away_underdog = home_spread < 0

        self.away_favorite = home_spread > 0
        self.home_underdog = home_spread > 0

        # Win Results info
        self.home_win, \
        self.away_win, \
        self.favorite_win, \
        self.underdog_win, \
        self.home_favorite_win, \
        self.away_underdog_win, \
        self.away_favorite_win, \
        self.home_underdog_win = self.get_win_results(self.home_score, self.away_score, self.home_spread)

        # Cover Results info
        self.home_cover, \
        self.away_cover, \
        self.favorite_cover, \
        self.underdog_cover, \
        self.home_favorite_cover, \
        self.away_underdog_cover, \
        self.away_favorite_cover, \
        self.home_underdog_cover = self.get_cover_results(self.home_spread_result, self.home_spread)

        # Total Results info
        self.over_hit = self.combined_score > self.total
        self.under_hit = self.combined_score < self.total

        self.id = f"{self.home_abbreviation}{self.away_abbreviation}{self.year}{str(date.split('-')[1]).zfill(2)}{self.day}"

        # Conditions info
        game_conditions = self.get_game_conditions(self.phase, self.month, self.day_of_week, self.divisional)
        spread_conditions = self.get_spread_conditions(self.spread)
        total_conditions = self.get_total_conditions(self.total)
        season_conditions = self.get_season_conditions(self.season)
        self.conditions = self.get_conditions(game_conditions, spread_conditions, total_conditions, season_conditions)

    def get_division(self, team):
        for division, teams in constants.DIVISIONS.items():
            if team in teams:
                return division
        return "NOT IN DIVISION"

    def get_win_results(self, home_score, away_score, home_spread):
        home, away, favorite, underdog, home_favorite, away_underdog, away_favorite, home_underdog = False, False, False, False, False, False, False, False

        if not self.tie:
            home = home_score > away_score
            away = home_score < away_score
            if home_spread != 0:
                favorite = home_score > away_score if home_spread < 0 else home_score < away_score
                underdog = home_score < away_score if home_spread < 0 else home_score > away_score
                if self.home_favorite:
                    home_favorite = home_score > away_score
                    away_underdog = home_score < away_score
                    away_favorite = False
                    home_underdog = False
                else:
                    away_favorite = home_score < away_score
                    home_underdog = home_score > away_score
                    home_favorite = False
                    away_underdog = False
            else:
                favorite = False
                underdog = False
                home_favorite = False
                away_underdog = False
                away_favorite = False
                home_underdog = False

        return home, away, favorite, underdog, home_favorite, away_underdog, away_favorite, home_underdog
    
    def get_cover_results(self, home_spread_result, home_spread):
        home, away, favorite, underdog, home_favorite, away_underdog, away_favorite, home_underdog = False, False, False, False, False, False, False, False

        if not self.spread_push:
            home = home_spread_result < home_spread
            away = home_spread_result > home_spread
            if home_spread != 0:
                favorite = home_spread_result < home_spread if home_spread < 0 else home_spread_result > home_spread
                underdog = home_spread_result < home_spread if home_spread > 0 else home_spread_result > home_spread
                if home_spread < 0:
                    home_favorite = home_spread_result < home_spread
                    away_underdog = home_spread_result > home_spread
                    away_favorite = False
                    home_underdog = False
                else:
                    away_favorite = home_spread_result > home_spread
                    home_underdog = home_spread_result < home_spread
                    home_favorite = False
                    away_underdog = False
            else:
                favorite = False
                underdog = False
                home_favorite = False
                away_underdog = False
                away_favorite = False
                home_underdog = False

        return home, away, favorite, underdog, home_favorite, away_underdog, away_favorite, home_underdog

    def get_game_conditions(self, season_phase, month, day_of_week, divisional_game):
        game_conditions = [
            GameCondition('season_phase', season_phase),
            GameCondition('month', month),
            GameCondition('day', day_of_week),
            GameCondition('divisional_game', divisional_game)
        ]

        return game_conditions

    def get_spread_conditions(self, spread):
        spread_conditions = []
        spread_conditions.append(SpreadCondition(spread, 'equal'))
        
        current_spread = 1.0
        max_spread = constants.MAX_SPREAD
        while current_spread <= max_spread:
            if current_spread <= spread:
                spread_conditions.append(SpreadCondition(current_spread, 'more'))
            if current_spread >= spread:
                spread_conditions.append(SpreadCondition(current_spread, 'less'))
            current_spread += 1.0

        return spread_conditions

    def get_total_conditions(self, total):
        total_conditions = []
        total_conditions.append(TotalCondition(self.total, 'equal'))
        
        current_total = constants.MIN_TOTAL
        max_total = constants.MAX_TOTAL
        while current_total <= max_total:
            if current_total <= total:
                total_conditions.append(TotalCondition(current_total, 'more'))
            if current_total >= total:
                total_conditions.append(TotalCondition(current_total, 'less'))
            current_total += 1.0

        return total_conditions

    def get_season_conditions(self, season):
        season_conditions = []
        current_season = constants.OLDEST_SEASON
        
        while current_season <= season:
            start_year, end_year = current_season.split('-')
            season_conditions.append(SeasonCondition(f'{start_year}-{end_year}', self.season))
            start_year = int(start_year)
            end_year = int(end_year)
            start_year += 1
            end_year += 1
            current_season = f"{start_year}-{end_year}"

        return season_conditions

    def get_conditions(self, game_conditions, spread_conditions, total_conditions, season_conditions):
        all_combinations = []

        # Iterate over game_combinations
        for r in range(len(game_conditions) + 1):
            game_combination_tuples = itertools.combinations(game_conditions, r)
            game_combinations = [list(combination) for combination in game_combination_tuples]
            for game_combination in game_combinations:
                for spread_condition in [None] + spread_conditions:
                    for total_condition in [None] + total_conditions:
                        for season_condition in [None] + season_conditions:
                            condition_description = self.create_description(game_combination, spread_condition, total_condition, season_condition)
                            all_combinations.append(condition_description)

        return all_combinations
    
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
        description += f'the spread is {spread_condition.number}'
        if spread_condition.relation == 'less':
            description += ' or less'
        elif spread_condition.relation == 'more':
            description += ' or more'
        description += ' / '

        return description

    def get_total_description(self, total_condition):
        description = ""
        description += f'the total is {total_condition.number}'
        if total_condition.relation == 'less':
            description += ' or less'
        elif total_condition.relation == 'more':
            description += ' or more'
        description += ' / '

        return description
    
    def get_game_description(self, game_conditions):
        description = ""
        if len(game_conditions) > 0:
            for game_condition in game_conditions:
                condition = game_condition.condition
                value = game_condition.value
                if condition == 'season_phase':
                    description += f"it is the {'regular season' if value == 'Regular Season' else 'playoffs'} / "
                elif condition == 'month':
                    description += f'it is {value} / '
                elif condition == 'day':
                    description += f'it is a {value} / '
                elif condition == 'divisional_game':
                    description += f"it is {'not' if value == False else ''} a divisional game / "

        return description
    
    def get_season_description(self, season_condition):
        description = f'since the {season_condition.season_since} season / '
        return description

    def to_dict(self):
        attributes = {key: value for key, value in vars(self).items() if key != 'conditions'}
        return attributes

    def to_tuple(self):
        values = (
            self.id, 
            self.date, 
            self.month, 
            int(self.day), 
            int(self.year), 
            self.season,
            self.day_of_week, 
            self.phase, 
            self.home_team, 
            self.home_abbreviation,
            self.home_division, 
            self.away_team, 
            self.away_abbreviation,
            self.away_division, 
            self.divisional, 
            int(self.home_score),
            int(self.away_score), 
            int(self.combined_score), 
            self.tie,
            self.winner, 
            self.loser, 
            int(self.spread), 
            int(self.home_spread),
            int(self.home_spread_result), 
            int(self.away_spread), 
            int(self.away_spread_result),
            self.spread_push, 
            self.pk, 
            int(self.total),
            self.total_push, 
            self.home_favorite, 
            self.away_underdog,
            self.away_favorite, 
            self.home_underdog, 
            self.home_win,
            self.away_win, 
            self.favorite_win, 
            self.underdog_win,
            self.home_favorite_win, 
            self.away_underdog_win,
            self.away_favorite_win, 
            self.home_underdog_win,
            self.home_cover, 
            self.away_cover,
            self.favorite_cover, 
            self.underdog_cover, 
            self.home_favorite_cover,
            self.away_underdog_cover, 
            self.away_favorite_cover,
            self.home_underdog_cover, 
            self.over_hit, 
            self.under_hit
        )
        return values

    def __str__(self):
        returner = ''
        for key, value in vars(self).items():
            returner += f'{key}: '
            if isinstance(value, dict):
                returner += ' {\n'
                for k, v in value.items():
                    returner += f'    {k}: {v}\n'
                returner += '}\n'
            elif isinstance(value, list):
                returner += ' [\n'
                for item in value:
                    returner += f'    {item}\n'
                returner += ']\n'
            else:
                returner += f'{value}\n'
        return returner

    
    