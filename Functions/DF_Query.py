import pandas as pd


def _get_col_index_by_name(input_df, col_name):
    return input_df.columns.get_loc(col_name)


def get_col_index_by_name(input_df, config_command):
    header_name = None

    header_name = str(config_command["Header_Name"])
    return _get_col_index_by_name(input_df=input_df, col_name=header_name)


d = {'Names': [3, 27]}
df = pd.DataFrame(d)


def _get_longest_string_in_column(input_df, column_name):
    print(f"Column '{column_name} max Chars: {input_df[column_name].str.len().max()}")


def get_longest_string_in_column(input_df, config_commands):
    working_df = input_df
    for columns in config_commands["Column_Names"]:
        working_df[columns] = working_df[columns].astype(str)

    for columns in config_commands["Column_Names"]:
        _get_longest_string_in_column(working_df, columns)


