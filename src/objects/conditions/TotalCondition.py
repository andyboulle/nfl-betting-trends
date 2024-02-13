#################################################################################
# TotalCondition.py                                                             #
#                                                                               #
# This object will define the specifics of a condition related to totals. It    #
# gives the total associated with the condition and the relation to the total   #    
# associated with the condition. Relations can be more, less or equal.          #
#################################################################################
class TotalCondition:
    
    number = None
    relation = None #more, less, equal

    def __init__(self, number, relation):
        self.number = number
        self.relation = relation

    def __str__(self):
        return f'{{ total: {self.number}, {self.relation} }}'