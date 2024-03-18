import hashlib
import itertools
from datetime import datetime
from models.trend import Trend
import config as config

class UpcomingGame:
    id = None
    id_string = None
    
    # Game info
    date = None
    month = None
    day = None
    year = None
    season = None
    day_of_week = None

    # Team info
    home_team = None
    home_abbreviation = None
    home_division = None
    away_team = None
    away_abbreviation = None
    away_divison = None
    divisional = None

    # Spread info
    spread = None
    home_spread = None
    home_spread_odds = None
    away_spread = None
    away_spread_odds = None

    # Moneyline info
    home_moneyline_odds = None
    away_moneyline_odds = None

    # Total info
    total = None
    over = None
    over_odds = None
    under = None
    under_odds = None

    trends = None

    def __init__(self, date, home_team, away_team, home_spread, home_spread_odds, away_spread_odds, home_moneyline_odds, away_moneyline_odds, over, over_odds, under_odds, trends_indicator=False):
        # Game info
        self.date = date
        self.month = datetime.strptime(date.split('-')[1], '%m').strftime('%B')
        self.day = date.split('-')[2]
        self.year = date.split('-')[0]
        self.season = f'{self.year}-{int(self.year) + 1}' if int(date.split('-')[1]) > 8 else f'{int(self.year) - 1}-{self.year}'
        self.day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

        # Team info
        self.home_team = home_team if home_team in config.TEAMS else ValueError(f'{home_team} not a valid team')
        self.home_abbreviation = config.ABBREVIATIONS[home_team]
        self.home_division = self.get_division(home_team)
        self.away_team = away_team if away_team in config.TEAMS else ValueError(f'{away_team} not a valid team')
        self.away_abbreviation = config.ABBREVIATIONS[away_team]
        self.away_division = self.get_division(away_team)
        self.divisional = self.home_division == self.away_division

        # Spread info
        self.home_spread = home_spread
        self.home_spread_odds = home_spread_odds
        self.away_spread = home_spread * -1
        self.away_spread_odds = away_spread_odds
        self.spread = max(self.home_spread, self.away_spread)

        # Moneyline info
        self.home_moneyline_odds = home_moneyline_odds
        self.away_moneyline_odds = away_moneyline_odds

        # Total info
        self.total = over
        self.over = over
        self.over_odds = over_odds
        self.under = over
        self.under_odds = under_odds

        # Id info
        self.id_string = f"{self.home_abbreviation}{self.away_abbreviation}{self.year}{str(date.split('-')[1]).zfill(2)}{self.day}"
        self.id = hashlib.sha256(self.id_string.encode()).hexdigest()

        if trends_indicator:
            self.trends = self.get_trends(self.month, self.day_of_week, self.divisional, self.spread, self.total, self.season)

    def get_trends(self, month, day_of_week, divisional, spread, total, season):
        spread_conditions = [None, f'{spread}']
        for i in range(1, config.MAX_SPREAD + 1):
            if i < spread:
                spread_conditions.append(f'{i} or more')
            elif i == spread:
                spread_conditions.extend([f'{i} or more', f'{i} or less'])
            else:
                spread_conditions.append(f'{i} or less')
        total_conditions = [None]
        for i in range(config.MIN_TOTAL, config.MAX_TOTAL + 1, 5):
            if i < total:
                total_conditions.append(f'{i} or more')
            elif i == total:
                total_conditions.extend([f'{i} or more', f'{i} or less'])
            else:
                total_conditions.append(f'{i} or less')      
        start_year, end_year = map(int, config.OLDEST_SEASON.split('-'))
        season_conditions = [f'since {start_year}-{end_year}']
        while end_year < int(season.split('-')[1]):
            start_year += 1
            end_year += 1
            season_conditions.append(f'since {start_year}-{end_year}')

        categories = [
            'home outright', 'away outright', 
            'home ats', 'away ats',
            'over', 'under'
        ]

        if self.spread != 0:
            categories.extend(['favorite outright', 'underdog outright', 'favorite ats', 'underdog ats'])
            categories.extend(
                ['home favorite outright', 'away underdog outright', 'home favorite ats', 'away underdog ats'] if self.home_spread < 0 
                else ['away favorite outright', 'home underdog outright', 'away favorite ats', 'home underdog ats']
            )

        conditions = [categories, [month, None], [day_of_week, None], [divisional, None], spread_conditions, total_conditions, season_conditions]
        trends = [Trend(*args) for args in itertools.product(*conditions)]

        return trends

    def get_division(self, team):
        for division, teams in config.DIVISIONS.items():
            if team in teams:
                return division
        return "NOT IN DIVISION"       
    
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
            self.home_team, 
            self.home_abbreviation,
            self.home_division, 
            self.away_team, 
            self.away_abbreviation,
            self.away_division, 
            self.divisional, 
            float(self.spread), 
            float(self.home_spread),
            int(self.home_spread_odds), 
            float(self.away_spread), 
            int(self.away_spread_odds),
            int(self.home_moneyline_odds),
            int(self.away_moneyline_odds),
            float(self.total),
            float(self.over),
            int(self.over_odds),
            float(self.under),
            int(self.under_odds)
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