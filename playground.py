import time
from src.analysis.objects.Game import Game
from src.analysis.objects.NamedDataframe import NamedDataframe
from src.analysis.basic_trends.BasicTrends import BasicTrends
from src.analysis.option_trends.GameOptionTrends import GameOptionTrends
from src.analysis.option_trends.BettingOptionTrends import BettingOptionTrends
from src.analysis.option_trends.IntegratedOptionTrends import IntegratedOptionTrends
from src.analysis.option_trends.YearlyOptionTrends import YearlyOptionTrends
from src.analysis.option_trends.AllOptionTrends import AllOptionTrends
import pandas as pd

start_time = time.time()

# Use any game you want
game = Game('2023-2024', '2023-10-29', 'Washington Commanders', 'Philadelphia Eagles', 265, -330, 7, -7, 43.5)
df = pd.read_csv('datafiles/csv/analysis_data.csv')
nd = NamedDataframe(df, 'All data')

# Change to determine what kind of trends you see
got = BasicTrends(nd, game)
strng = str(got)
with open('output.txt', 'w') as file:
    file.write(strng)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

