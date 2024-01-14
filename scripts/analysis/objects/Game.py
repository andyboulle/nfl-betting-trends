#################################################################################
# Game.py                                                                       #
#                                                                               #
# This object will provide information about a specific game. It will give any  #
# information about the game that is available before the game actually happens #
# such as basic info about date/time, moneyline, spread, and total info. The    # 
# toString method prints a dictionary style string of keys and attributes.      #
#################################################################################
from datetime import datetime

class Game:
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
    home_moneyline = None
    away_moneyline = None
    favorite_moneyline = None
    underdog_moneyline = None
    equal_moneyline = None
    home_favorite = None
    home_underdog = None
    away_favorite = None
    away_underdog = None
    line = None
    home_line = None
    away_line = None
    pk = None
    home_favored = None
    home_not_favored = None
    away_favored = None
    away_not_favored = None
    total = None

    def __init__(self, season, date, home_team, away_team, home_moneyline, away_moneyline, home_line, away_line, total):
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
        self.home_moneyline = home_moneyline
        self.away_moneyline = away_moneyline
        self.favorite_moneyline = home_moneyline if home_moneyline < away_moneyline else away_moneyline
        self.underdog_moneyline = away_moneyline if self.favorite_moneyline == home_moneyline else home_moneyline
        self.equal_moneyline = home_moneyline == away_moneyline
        self.home_favorite = True if (home_moneyline == self.favorite_moneyline and self.equal_moneyline == False) else False
        self.home_underdog = True if (self.home_favorite == False and self.equal_moneyline == False) else False
        self.away_favorite = True if (away_moneyline == self.favorite_moneyline and self.equal_moneyline == False) else False
        self.away_underdog = True if (self.away_favorite == False and self.equal_moneyline == False) else False
        self.home_line = home_line
        self.away_line = away_line
        self.line = home_line if home_line > 0 else away_line
        self.pk = self.line == 0
        self.home_favored = True if (home_line < away_line and self.pk == False) else False
        self.home_not_favored = True if (self.home_favored == False and self.pk == False) else False
        self.away_favored = True if (away_line < home_line and self.pk == False) else False
        self.away_not_favored = True if (self.away_favored == False and self.pk == False) else False
        self.total = total


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

    def __str__(self):
        result = ""
        for attr, value in vars(self).items():
            result += f'{attr}: {value}\n'
        return result
    