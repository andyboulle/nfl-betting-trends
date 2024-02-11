#################################################################################
# SeasonCondition.py                                                            #
#                                                                               #
# This object will define the specifics of a condition related to seasons. It   #
# gives the range of seasons that this condition is associated with, as well as #
# a list of all the seasons within that range.                                  #
#################################################################################
class SeasonCondition:

    season_since = None
    seasons = None

    def __init__(self, season_since, season_to):
        self.season_since = season_since
        self.season_to = season_to
        self.seasons = self.get_seasons()

    # This function gets all the seasons from season_since to season_to and puts them in a list
    def get_seasons(self):
        seasons = []
        current_season = self.season_since
        while current_season <= self.season_to:
            start_year, end_year = current_season.split('-')
            seasons.append(current_season)
            start_year = int(start_year)
            end_year = int(end_year)
            start_year += 1
            end_year += 1
            current_season = f"{start_year}-{end_year}"
        
        return seasons

    def __str__(self):
        return f'{{ seasons: from {self.season_since} to {self.season_to} }}'