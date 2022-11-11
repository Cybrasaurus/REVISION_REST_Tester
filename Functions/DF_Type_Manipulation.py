import copy
import logging
from contextlib import suppress
import Functions.cy_exceptions as cy_ex
from Functions.cy_exceptions import Dict_Pair_Type_Check as dptc
import pandas as pd
import numpy as np
import math
from copy import deepcopy


def _convert_column_to_int(x, error_case_replacer):
    if type(x) == int:
        return x
    else:
        try:
            x = int(float(x))
            return (x)
        except TypeError:
            logging.WARNING(
                f"   WARNING: convert_column_to_int - Could not convert {x}, type {type(x)} to an Integer, overwriting with {error_case_replacer}")
            return error_case_replacer
        except ValueError:
            logging.warning(
                f"   WARNING: convert_column_to_int - Could not convert {x}, type {type(x)} to an Integer, overwriting with {error_case_replacer}")
            return error_case_replacer


def convert_columns_to_int(input_df, config_command):
    target_col_list = None
    error_case_replacer = 0
    # todo handle both string and list
    target_col_list = config_command["Column_Names"]
    with suppress(KeyError):
        error_case_replacer = config_command["Error_Replacer"]

    for target_col in target_col_list:
        logging.info(f"     Converting Column {target_col} to int")
        input_df[target_col] = input_df[target_col].apply(_convert_column_to_int,
                                                          error_case_replacer=error_case_replacer)
    return input_df


def _convert_column_to_float(x, error_case_replacer):
    if type(x) == float:
        if math.isnan(x):
            logging.warning(
                f"      WARNING: convert_column_to_int - Data {x}, type {type(x)} is already a float, but a NAN, overwriting with {error_case_replacer}")
            x = error_case_replacer
        elif math.isinf(x):
            logging.warning(
                f"      WARNING: convert_column_to_int - Data {x}, type {type(x)} is already a float, but a infinite value, overwriting with {error_case_replacer}")
            x = error_case_replacer
        return x
    else:
        try:
            x = float(x)
            logging.debug(f"      {x}")
            return x
        except TypeError:
            logging.warning(
                f"      WARNING: convert_column_to_int - Could not convert {x}, type {type(x)} to a Float, overwriting with {error_case_replacer}")
            return error_case_replacer
        except ValueError:
            logging.warning(
                f"      WARNING: convert_column_to_int - Could not convert {x}, type {type(x)} to a Float, overwriting with {error_case_replacer}")
            return error_case_replacer


def convert_column_to_float(input_df, config_command):
    # todo singe and multo colums

    # Declare default Values before potential overwrites in supress()
    error_case_replacer = 0

    # todo handle both string and list
    target_col_list = config_command["Column_Names"]
    with suppress(KeyError):
        error_case_replacer = config_command["Error_Replacer"]

    for target_col in target_col_list:
        logging.info(f"     Converting Column {target_col} to float")
        input_df[target_col] = input_df[target_col].apply(_convert_column_to_float,
                                                          error_case_replacer=error_case_replacer)
    return input_df


def _convert_to_string(x):
    return str(x)


def convert_to_string(input_df, config_command):
    """
    This function converts the variable type of a single or multiple columns of the input dataframe to a str.
    Currently, NAN Values will be converted to "NAN" as a string
    #TODO nan check
    :param input_df: The dataframe, on which columns are to be converted
    :param config_command: the dict containing the commands
    :return: The modified Dataframe
    """
    # Declare default Values before potential overwrites in supress()
    column_name = None
    column_names = None

    logging.critical(f"---Config of iteration: {config_command}, type: {type(config_command)}")

    # Load Json Dict Data
    with suppress(KeyError):
        column_name = config_command["Column_Name"]
        dptc(json_name="Column_Name", var=column_name, intended_type=str)
    with suppress(KeyError):
        column_names = config_command["Column_Names"]
        dptc(json_name="Column_Names", var=column_names, intended_type=list)

    # neither key is given, raise error
    if not column_name and not column_names:
        raise cy_ex.Dict_Missing_Keys(possible_keys=["Column_Name", "Column_Names"])

    #handle either singe-col operation or multiple columns
    #todo somehow broke


    if column_name:
        try:
            column_name = int(column_name)
        except:
            pass
        logging.info(f"        Converting Column: {column_name}")
        input_df[column_name] = input_df[column_name].apply(_convert_to_string)

    else:
        for col_names in column_names:
            logging.info(f"        Converting Column: {col_names}")
            input_df[col_names] = input_df[col_names].apply(_convert_to_string)
    return input_df

def testing_convert_to_string(input_df, config_command):

    column_name = config_command["Column_Name"]

    logging.info(f"        Converting Column: {column_name}")

    x = input_df[column_name].apply(_convert_to_string)
    deepcopy_of_apply = copy.deepcopy(x)

    input_df[column_name] = deepcopy_of_apply
    return input_df