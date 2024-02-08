#################################################################################
# Record.py                                                                     #
#                                                                               #
# This object will provide information about the record of a trend. It will     #
# take description of the trend, as well as the number of wins, losses, and     #
# pushes for the trend. It also calculates the total number of games and win    #
# percentage of the trend. The toString method prints the description and then  #
# the wins, losses, pushes, and win percentage of a trend.                      # 
#################################################################################
class Record:

    wins = 0
    losses = 0
    pushes = 0
    win_pct = 0.0
    total_games = None

    def __init__(self, description, wins, losses, pushes):
        self.description = description
        self.wins = wins
        self.losses = losses
        self.pushes = pushes
        self.win_pct = 0 if wins == 0 else round((100 * wins / (wins + losses + (pushes / 2))), 2)
        self.total_games = wins + losses + pushes

    def __str__(self):
        return f'{self.description}: {self.wins}-{self.losses}-{self.pushes} ({self.win_pct}%)'