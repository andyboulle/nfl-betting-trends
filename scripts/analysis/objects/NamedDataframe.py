#################################################################################
# NamedDataframe.py                                                             #
#                                                                               #
# This object will provide names for dataframes. It pairs a dataframe with a    #
# passed string called description. The toString method prints the description  #
# followed by the dataframe itself                                              #
#################################################################################
class NamedDataframe:
    description = None
    df = None

    def __init__(self, df, description):
        self.df = df
        self.description = description

    def __str__(self):
        returner = self.description + '\n'
        returner += self.df
        return returner