import json
from src.objects.Trend import Trend
from src.objects.Record import Record
from src.objects.CompletedGame import CompletedGame
from src.objects.conditions.SeasonCondition import SeasonCondition
from src.objects.conditions.TotalCondition import TotalCondition
from src.objects.conditions.SpreadCondition import SpreadCondition
from src.objects.conditions.GameCondition import GameCondition

class CustomEncoder(json.JSONEncoder):

    objects = (
        Trend,
        Record,
        CompletedGame, 
        SeasonCondition, 
        TotalCondition, 
        SpreadCondition, 
        GameCondition
    )

    def default(self, object):
        if isinstance(object, self.objects):
            return object.__dict__
        return json.JSONEncoder.default(self, object)