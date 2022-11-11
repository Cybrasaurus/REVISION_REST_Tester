import math

import pandas as pd
import logging
from contextlib import suppress
from Functions.cy_exceptions import Dict_Pair_Type_Check as dptc
import Functions.cy_exceptions as cy_ex

def _rename_column_containing_keyword(input_df, header_name, keyword_to_match):
    my_dict = input_df.to_dict(orient="list")

    break_out_flag = False
    reworked_dict = {}

    key_list = []
    mod_key_list = []
    for keys in my_dict:
        key_list.append(keys)
        mod_key_list.append(keys)

    for keys in my_dict:
        for rows in my_dict[keys]:
            if rows == keyword_to_match:
                logging.debug(f"     match: {keyword_to_match}")

                # get index (position) of key in mod_key_list
                index_key = mod_key_list.index(keys)
                # rename said key at index
                mod_key_list[index_key] = header_name

                for items in range(len(key_list)):
                    reworked_dict[mod_key_list[items]] = my_dict[key_list[items]]

                break_out_flag = True
                break
            else:
                logging.debug(
                    f"     rename_col_keyword else case, no match found: Curr Item: {rows} vs {keyword_to_match}")
        if break_out_flag:
            break
    return_df = pd.DataFrame.from_dict(reworked_dict)
    return return_df


def rename_column_containing_keyword(input_df, config_command):
    header_name = None
    keyword_to_match = None

    header_name = config_command["New_Header"]
    keyword_to_match = config_command["Keyword"]
    return _rename_column_containing_keyword(input_df=input_df, header_name=header_name,
                                             keyword_to_match=keyword_to_match)


def batch_rename_column_containing_keyword(input_df, config_command):
    return_df = input_df
    for keys in config_command["Keyword_Header_Dict"]:
        header_name = None
        keyword_to_match = None

        header_name = config_command["Keyword_Header_Dict"][keys]
        keyword_to_match = str(keys)
        return_df = _rename_column_containing_keyword(input_df=return_df, header_name=header_name,
                                                      keyword_to_match=keyword_to_match)
    return return_df


def _rename_Col_based_on_Index(input_df, col_index, col_name):
    # todo rework function to handle both based on index and actual name
    assert type(col_index) == int
    assert type(col_name) == str

    original_col_name = input_df.columns[col_index]
    # input_df.columns.values[col_index] = col_name
    input_df = input_df.rename(columns={original_col_name: col_name})
    return input_df


def rename_Col_based_on_Index(input_df, config_command, col_variable):
    col_index = None
    index_adjuster = 0

    with suppress(KeyError):
        col_index = config_command["Column_Index"]
    col_name = config_command["Column_Name"]
    with suppress(KeyError):
        index_adjuster = config_command["Index_Adjustment"]

    if index_adjuster != 0:
        col_index = col_variable
        col_index += index_adjuster

    return _rename_Col_based_on_Index(input_df=input_df, col_index=col_index, col_name=col_name)


def _reformat_col_by_shema(reformat_string, current_schema, reformat_schema, amount_percent, nan_handling):
    """
    Does the actual formatting
    :param reformat_string: the string to be reformatted
    :param current_schema: the schema of the current string
    :param reformat_schema: the schema in which the string is to be reformatted
    :param amount_percent: amount of '%' chars in the formatting string
    :return formatted_string: reformatted string
    """



    cur_list = current_schema.split("%")
    reformat_list = reformat_schema.split("%")

    # split the string into a dict, current_format is the key, string segment the value
    if type(reformat_string) == float and math.isnan(reformat_string):
        if nan_handling:
            return reformat_string
        else:
            raise cy_ex.Format_Exception(f"Current Item: '{reformat_string}', type: '{type(reformat_string)}' does not "
                                         f"fit the current schema: '{current_schema.replace('%', '')}'")
    else:
        # check whether the schema and the string have the same format
        assert len(current_schema) - amount_percent == len(str(reformat_string)), \
            f"Current Schema: '{current_schema.replace('%', '')}' does not fit the current item: '{str(reformat_string)}'," \
            f"type: {type(reformat_string)}"

        # split formatting_string into segments in a dict
        workingstring = str(reformat_string)
        logging.debug(workingstring)
        stitch_dict = {}
        for count, items in enumerate(cur_list):
            stitch_dict[items] = workingstring[:len(items)]
            logging.debug(f"stitch at count: {stitch_dict[items]}")
            workingstring = workingstring[len(items):]
            logging.debug(f"Working String: {workingstring}")

        # stitch the string back together, based on dict key
        formatted_string = ""
        for items in reformat_list:
            formatted_string += stitch_dict[items]
            logging.debug(formatted_string)

        return formatted_string

def reformat_col_by_shema(input_df, config_commands):
    """
    This function can reformat a string built in a specific pattern into a different pattern.
    Example: A Date (16.06.2000) would have the format DD.MM.YYYY and could be reformatted into
    a sql format of 2000.06.16, so YYYY.MM.DD. Commands:
    current_schema="dd%.%mm%.%yyyy", reformat_schema="yyyy%.%mm%.%dd"

    Both Schemas need to have the same length, and the length of the string (excluding the splitting denominator %).
    Due to the mapping to a dict, each segment that is to be reordered needs to have a unique key, or the last
    occurrence of the Key will be used for all segments with the same key.
    Date Example:
    Original Date: '16.06,2000'
    current_schema="dd%.%mm%.%yyyy", reformat_schema="yyyy%.%mm%.%dd"
    Output: 2000,06,16
    Both the '.' between 16 and 06 as well as the ',' between 06 and 2000 got mapped to '.' in the schema

    :param input_df: Input Dataframe
    :param config_commands: json config commands
    :return input_df: reformatted Dataframe
    """

    # Declare default Values before potential overwrites in supress()
    column_name = False
    column_names = False
    nan_handling = False

    # Load Json Dict Data
    current_schema = config_commands["Current_Schema"]
    reformat_schema = config_commands["Reformatted_Schema"]
    with suppress(KeyError):
        column_name = config_commands["Column_Name"]
        dptc(json_name="Column_Name", var=column_name, intended_type=str)
    with suppress(KeyError):
        column_names = config_commands["Column_Names"]
        dptc(json_name="Column_Names", var=column_names, intended_type=list)
    with suppress(KeyError):
        nan_handling = config_commands["Skip_Blank_Fields"]
        assert nan_handling == "Yes" or nan_handling == 1, "if Skip_Blank_Fields is used, " \
                                                           "only 'Yes' or 1 is allowed, otherwise do not use key"
        nan_handling = True
    amount_percent = current_schema.count("%")
    assert len(current_schema) == len(reformat_schema), \
        f"'Current_Schema' and 'Reformatted_Schema' are no the same lenght"

    # handle either singe-col operation or multiple columns
    if column_name:
        logging.info(f"        Reformatting Column: {column_name}")
        input_df[column_name] = input_df[column_name].apply(_reformat_col_by_shema, current_schema=current_schema,
                                                            reformat_schema=reformat_schema,
                                                            amount_percent=amount_percent,
                                                            nan_handling=nan_handling)
    else:
        for col_names in column_names:
            logging.info(f"        Reformatting Column: {col_names}")
            input_df[col_names] = input_df[col_names].apply(_reformat_col_by_shema, current_schema=current_schema,
                                                            reformat_schema=reformat_schema,
                                                            amount_percent=amount_percent,
                                                            nan_handling=nan_handling)
    return input_df


if __name__ == "__main__":
    _reformat_col_by_shema("16.06.2016", current_schema="dd%.%mm%.%yyyy", reformat_schema="yyyy%.%mm%.%dd", amount_percent = 4)