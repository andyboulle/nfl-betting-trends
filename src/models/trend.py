import hashlib

class Trend:

    id = None

    category = None
    month = None
    day_of_week = None
    divisional = None
    spread = None
    total = None
    seasons = None
    conditions = None

    wins = None
    losses = None
    pushes = None
    total_games = None
    win_pct = None

    def __init__(self, category, month, day_of_week, divisional, spread, total, seasons, wins=0, losses=0, pushes=0, total_games=0, win_pct=0):
        self.category = category
        self.month = month
        self.day_of_week = day_of_week
        self.divisional = divisional
        self.spread = spread
        self.total = total
        self.seasons = seasons
        
        self.id_string = ','.join(map(str, [category, month, day_of_week, divisional, spread, total, seasons]))
        self.id = hashlib.sha256(self.id_string.encode()).hexdigest()

        self.wins = wins
        self.losses = losses
        self.pushes = pushes
        self.total_games = total_games
        self.win_pct = win_pct

    def update_record(self, game):
        if self.category in ['home outright', 'away outright']:
            if game.tie:
                self.pushes += 1
            elif (self.category == 'home outright' and game.home_win) or (self.category == 'away outright' and game.away_win):
                self.wins += 1
            else:
                self.losses += 1
        elif self.category in ['favorite outright', 'underdog outright']:
            if game.pk == False:
                if game.tie:
                    self.pushes += 1
                elif (self.category == 'favorite outright' and game.favorite_win) or (self.category == 'underdog outright' and game.underdog_win):
                    self.wins += 1
                else:
                    self.losses += 1 
        elif self.category in ['home favorite outright', 'away underdog outright']:
            if game.pk == False:
                if game.home_favorite:
                    if game.tie:
                        self.pushes += 1
                    elif (self.category == 'home favorite outright' and game.home_favorite_win) or (self.category == 'away underdog outright' and game.away_underdog_win):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['away favorite outright', 'home underdog outright']:
            if game.pk == False:
                if game.away_favorite:
                    if game.tie:
                        self.pushes += 1
                    elif (self.category == 'away favorite outright' and game.away_favorite_win) or (self.category == 'home underdog outright' and game.home_underdog_win):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['home ats', 'away ats']:
            if game.spread_push:
                self.pushes += 1
            elif (self.category == 'home ats' and game.home_cover) or (self.category == 'away ats' and game.away_cover):
                self.wins += 1
            else:
                self.losses += 1
        elif self.category in ['favorite ats', 'underdog ats']:
            if game.pk == False:
                if game.spread_push:
                    self.pushes += 1
                elif (self.category == 'favorite ats' and game.favorite_cover) or (self.category == 'underdog ats' and game.underdog_cover):
                    self.wins += 1
                else:
                    self.losses += 1 
        elif self.category in ['home favorite ats', 'away underdog ats']:
            if game.pk == False:
                if game.home_favorite:
                    if game.spread_push:
                        self.pushes += 1
                    elif (self.category == 'home favorite ats' and game.home_favorite_cover) or (self.category == 'away underdog ats' and game.away_underdog_cover):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['away favorite ats', 'home underdog ats']:
            if game.pk == False:
                if game.away_favorite:
                    if game.spread_push:
                        self.pushes += 1
                    elif (self.category == 'away favorite ats' and game.away_favorite_cover) or (self.category == 'home underdog ats' and game.home_underdog_cover):
                        self.wins += 1
                    else:
                        self.losses += 1
        elif self.category in ['over', 'under']:
            if game.total_push:
                self.pushes += 1
            elif (self.category == 'over' and game.over_hit) or (self.category == 'under' and game.under_hit):
                self.wins += 1
            else:
                self.losses += 1

        self.total_games = self.wins+self.losses+self.pushes
        win_pct_games = self.wins + self.losses + (self.pushes / 2)
        self.win_pct = 0 if win_pct_games == 0 else round(self.wins / (self.wins + self.losses + (self.pushes / 2)) * 100, 2)

    def get_description(self):
        returner = ''
        returner += self.get_category_description(self.category)
        if self.day_of_week != None:
            returner += f' on {self.day_of_week}s'
        if self.month != None:
            returner += f' in {self.month}'
        if self.divisional != None:
            returner += ' in divisional games' if self.divisional else ' in non-divisional games'
        if self.spread != None:
            returner += f' when the spread is {self.spread}'
        if self.total != None:
            returner += f' and the total is {self.total}' if self.spread != None else f' when the total is {self.total}'
        if self.seasons != None:
            returner += f' {self.seasons}'

        return returner

    def get_category_description(self, category):
        returner = ''
        if category == 'home outright':
            returner += 'Home teams outright'
        elif category == 'away outright':
            returner += 'Away teams outright'
        elif category == 'favorite outright':
            returner += 'Favorites outright'
        elif category == 'underdog outright':
            returner += 'Underdogs outright'
        elif category == 'home favorite outright':
            returner += 'Home Favorites outright'
        elif category == 'away underdog outright':
            returner += 'Away Underdogs outright'
        elif category == 'away favorite outright':
            returner += 'Away Favorites outright'
        elif category == 'home underog outright':
            returner += 'Home Underdogs outright'
        elif category == 'home ats':
            returner += 'Home teams against the spread'
        elif category == 'away ats':
            returner += 'Away teams against the spread'
        elif category == 'favorite ats':
            returner += 'Favorites against the spread'
        elif category == 'underdog ats':
            returner += 'Underdogs against the spread'
        elif category == 'home favorite ats':
            returner += 'Home Favorites against the spread'
        elif category == 'away underdog ats':
            returner += 'Away Underdogs against the spread'
        elif category == 'away favorite ats':
            returner += 'Away Favorites against the spread'
        elif category == 'home underog ats':
            returner += 'Home Underdogs against the spread'
        elif category == 'over':
            returner += 'Overs'
        elif category == 'under':
            returner += 'Unders'
        return returner


    def get_month_description(self, month):
        return f' in {month}'

    def to_dict(self):
        return vars(self)

    def to_tuple(self):
        values = (
            self.id,
            self.id_string,
            self.category,
            self.month,
            self.day_of_week,
            self.divisional,
            self.spread,
            self.total,
            self.seasons,
            int(self.wins),
            int(self.losses),
            int(self.pushes),
            int(self.total_games),
            float(self.win_pct)
        )
        return values

    def __str__(self):
        return f'{self.id_string}: {self.wins}-{self.losses}-{self.pushes} ({self.win_pct}%)'
