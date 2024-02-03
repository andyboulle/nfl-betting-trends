#################################################################################
# filter_functions.py                                                           #
#                                                                               #
# This file will provide helper functions for other files to use. The functions # 
# will give functionality for creating new dataframes based on filter criteria  #
#################################################################################

# Returns whether the given column name is in the given dataframe
def column_in_dataframe(column_name, dataframe):
    if column_name in dataframe.columns:
        return True
    else:
        return False

# Filters a dataframe by column name and corresponding valie
def filter_dataframe_by_values(df, filter_dict):
    filtered_df = df.copy()
    for col, value in filter_dict.items():
        if column_in_dataframe(col, filtered_df):
            filtered_df = filtered_df[filtered_df[col] == value]
    return filtered_df

# Filters a dataframe by column name and corresponding value, 
# where ALL of the column-value pairs are met
def filter_dataframe_by_values_and(df, filter_dict):
    filtered_df = df.copy()
    for col, value in filter_dict.items():
        if column_in_dataframe(col, filtered_df):
            filtered_df = filtered_df[filtered_df[col] == value]
    return filtered_df

# Filters a dataframe by column name and corresponding value, 
# where ANY of the column-value pairs are met
def filter_dataframe_by_values_or(df, filter_dict):
    filtered_df = df.copy()
    mask = None

    for col, value in filter_dict.items():
        if column_in_dataframe(col, filtered_df):
            if mask is None:
                mask = filtered_df[col] == value
            else:
                mask |= filtered_df[col] == value

    if mask is not None:
        filtered_df = filtered_df[mask]

    return filtered_df