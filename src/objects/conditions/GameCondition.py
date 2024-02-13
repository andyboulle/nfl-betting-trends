#################################################################################
# GameCondition.py                                                              #
#                                                                               #
# This object will define the specifics of a condition related to games. It     #
# gives the name of a condition and its value.                                  #
#################################################################################
class GameCondition:

    condition = None
    value = None

    def __init__(self, condition, value):
        self.condition = condition
        self.value = value

    def __str__(self):
        return f'{{ {self.condition}: {self.value} }}'