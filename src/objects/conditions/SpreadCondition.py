#################################################################################
# SpreadCondition.py                                                            #
#                                                                               #
# This object will define the specifics of a condition related to spreads. It   #
# gives the spread associated with the condition and the relation to the spread #    
# associated with the condition. Relations can be more, less, or equal.         #
#################################################################################
class SpreadCondition:
    
    number = None
    relation = None #more, less, equal

    def __init__(self, number, relation):
        self.number = number
        self.relation = relation

    def __str__(self):
        return f'{{ spread: {self.number}, {self.relation} }}'
            