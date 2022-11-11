import pandas as pd
import logging
import copy
import numpy as np
from contextlib import suppress


def _strip_char_in_column(input_df, char_to_strip, target_col):
    my_dict = input_df.to_dict(orient="list")

    mod_list = []

    for items in my_dict[target_col]:
        try:
            mod_list.append(items.strip(fr"{char_to_strip}"))
            logging.debug("STRIP_CHAR_IN_COLUMN:   Stripped")
        except AttributeError:
            mod_list.append(items)
            logging.debug("STRIP_CHAR_IN_COLUMN:   Failed to Strip")
    my_dict[target_col] = mod_list
    return_df = pd.DataFrame.from_dict(my_dict)
    return return_df

def strip_char_in_column(input_df, config_command):
    char_to_strip = None
    target_col = None

    char_to_strip = config_command["Remove_Character"]
    target_col = config_command["Column_Name"]

    return _strip_char_in_column(input_df=input_df, char_to_strip=char_to_strip, target_col=target_col)

def _fill_nan_with_above_in_col(input_df, col_name, tolerance):
    import math
    my_dict = input_df.to_dict(orient="list")
    mod_dict = copy.deepcopy(my_dict)
    for count, rows in enumerate(my_dict[col_name]):
        logging.debug(f"      FILL_NAN_WITH_ABOVE {count}, Type: {type(rows)}, Item:{rows}-")
        if count == 0:
            continue
        elif len(str(rows)) < tolerance or pd.isna(rows):
            logging.debug(f"      prev: {my_dict[col_name][count - 1]}")
            mod_dict[col_name][count] = mod_dict[col_name][count - 1]
        else:
            logging.debug("      went else")
    return_df = pd.DataFrame.from_dict(mod_dict)
    return return_df

def fill_nan_with_above_in_col(input_df, config_command):

    col_name = None
    tolerance = 1

    col_name = config_command["Column_Name"]
    with suppress(KeyError):
        tolerance = config_command["Char_Lenght_Tolerance"]

    return _fill_nan_with_above_in_col(input_df=input_df, col_name=col_name, tolerance=tolerance)


def _replace_Row_Data_in_Columns(input_df, target_col_name, target_row_name, column_name_list, replacer):
    my_dict = input_df.to_dict(orient="list")

    target_index = my_dict[target_col_name].index(target_row_name)

    for cols in column_name_list:
        my_dict[cols][target_index] = replacer

    return_df = pd.DataFrame.from_dict(my_dict)
    return return_df


def replace_Row_Data_in_Columns(input_df, config_command):

    target_col_name = None
    target_row_name = None
    column_name_list = []
    replacer = None

    target_col_name = config_command["Reference_Column_Name"]
    target_row_name = config_command["Reference_Row_Name"]
    column_name_list = config_command["Column_Names"]
    replacer = config_command["Replacement"]

    return _replace_Row_Data_in_Columns(input_df=input_df, target_col_name=target_col_name,
                                        target_row_name=target_row_name, column_name_list=column_name_list,
                                        replacer=replacer)

def _generic_row_splitter(input_df, column_to_split: str, split_character: str):
    """
    This function splits a row containing multiple data into multiple, separate rows. Here's an alternate solution to the same problem: https://sureshssarda.medium.com/pandas-splitting-exploding-a-column-into-multiple-rows-b1b1d59ea12e
    :param input_df: The Pandas DF that contains data with multiples
    :param column_to_split: The Pandas Column Name containing rows with multiples
    :param split_character: The Character (or String) identifying the splitting operation
    :return: The Dataframe with more rows
    """
    splitting_dict = input_df.to_dict(orient="list")

    key_list = list(splitting_dict.keys())
    keylist_2 = copy.deepcopy(key_list)

    try:
        keylist_2.remove(column_to_split)
    except ValueError as ve:
        logging.warning(f"      Got Value Error: {ve}")
        logging.warning(f"      The Column Name does not exist in the Dataframe. Here is a list of all column names: \n"
              f"      {key_list}\n      Trying to remove: {column_to_split}")

    output_records = {}
    for items in key_list:
        output_records[items] = []

    for curr_iteration, keys in enumerate(splitting_dict[column_to_split]):
        try:
            temp_var = keys.split(split_character)
        except AttributeError:
            keys = str(keys)
            temp_var = keys.split(split_character)

        for entries in temp_var:
            output_records[column_to_split].append(entries.strip())  # strip() to remove trailing & leading whitespaces
            for items in keylist_2:
                output_records[items].append(splitting_dict[items][curr_iteration])

    return_df = pd.DataFrame.from_dict(output_records)
    return return_df


def generic_row_splitter(input_df, config_command):
    column_to_split = None
    split_character = None

    column_to_split = config_command["Column_Name"]
    split_character = config_command["Splitting_Character"]

    return _generic_row_splitter(input_df=input_df, column_to_split=column_to_split, split_character=split_character)