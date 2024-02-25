import hashlib
import itertools
from datetime import datetime
import src.constants as constants
from src.objects.Trend import Trend

class Game:

    # How the game will be selected from database
    id = None
    id_string = None

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

    trends = None

    def __init__(self, date, season_phase, home_team, away_team, home_score, away_score, home_spread, total, trends_indicator=False):
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

        # Id info
        self.id_string = f"{self.home_abbreviation}{self.away_abbreviation}{self.year}{str(date.split('-')[1]).zfill(2)}{self.day}"
        self.id = hashlib.sha256(self.id_string.encode()).hexdigest()

        if trends_indicator:
            self.trends = self.get_trends(self.phase, self.month, self.day_of_week, self.divisional, self.spread, self.total, self.season)

    def get_trends(self, phase, month, day_of_week, divisional, spread, total, season):
        spread_conditions = [None, f'{spread}'] + [f'{i} or more' for i in range(1, int(spread) + 1)] + [f'{i} or less' for i in range(int(spread), constants.MAX_SPREAD + 1)]
        total_conditions = [None, f'{total}'] + [f'{i} or more' for i in range(constants.MIN_TOTAL, int(total) + 1)] + [f'{i} or less' for i in range(int(total), constants.MAX_TOTAL + 1)]
        start_year, end_year = map(int, constants.OLDEST_SEASON.split('-'))
        season_conditions = [f'since {start_year}-{end_year}']
        while end_year < int(season.split('-')[1]):
            start_year += 1
            end_year += 1
            season_conditions.append(f'since {start_year}-{end_year}')

        categories = [
            'home outright', 'away outright', 'favorite outright', 'underdog outright', 
            'home favorite outright', 'away underdog outright', 'away favorite outright', 'home underdog outright',
            'home ats', 'away ats', 'favorite ats', 'underdog ats', 
            'home favorite ats', 'away underdog ats', 'away favorite ats', 'home underdog ats',
            'over', 'under'
        ]

        conditions = [categories, [phase, None], [month, None], [day_of_week, None], [divisional, None], spread_conditions, total_conditions, season_conditions]
        trends = [Trend(*args) for args in itertools.product(*conditions)]

        return trends
                

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

    
        description = f'since the {season_condition.season_since} season / '
        return description

    def to_dict(self):
        return vars(self)

    def to_tuple(self):
        values = (
            self.id,
            self.id_string, 
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
            float(self.spread), 
            float(self.home_spread),
            int(self.home_spread_result), 
            float(self.away_spread), 
            int(self.away_spread_result),
            self.spread_push, 
            self.pk, 
            float(self.total),
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

    
    