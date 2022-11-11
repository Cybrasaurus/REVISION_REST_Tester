from typing import Literal, get_args
from contextlib import suppress
import logging
import pandas as pd
_TYPEScut_to_column_on_keywordmatch_direction = Literal["from_left", "from_right"]


def _cut_to_column_on_keywordmatch(input_df, keyword_list: list,
                                  directionality: _TYPEScut_to_column_on_keywordmatch_direction):
    assert directionality in get_args(_TYPEScut_to_column_on_keywordmatch_direction), \
        f"'{directionality}' is invalid - valid options are {get_args(_TYPEScut_to_column_on_keywordmatch_direction)}"
    assert type(keyword_list) == list, \
        f"ERROR: cut_to_column_on_keyword_match - did not recieve a list of keywords, recieved a {type(keyword_list)} instead "
    my_dict = input_df.to_dict(orient="list")
    break_out_flag = False
    cut_dict = {}

    col_name_list = []
    for col_names in my_dict:
        col_name_list.append(col_names)
    if directionality == "from_right":
        col_name_list = col_name_list[::-1]

    for col_names in col_name_list:
        logging.debug(      col_names)
        for row_count, row_item in enumerate(my_dict[col_names]):
            if row_item == keyword_list[0]:
                compare_list = my_dict[col_names][row_count:row_count + len(keyword_list)]
                logging.debug(      compare_list)
                if compare_list == keyword_list:
                    logging.debug("     FULL Match")
                    temp_list = list(my_dict.keys())
                    logging.debug(f"\n      {temp_list}\n       Current Column: {col_names}\n")
                    index = temp_list.index(col_names)

                    if directionality == "from_left":
                        keep_list = temp_list[index:]
                    else:
                        keep_list = temp_list[:index + 1]

                    for dict_keys in keep_list:
                        cut_dict[dict_keys] = my_dict[dict_keys]
                    break_out_flag = True
                    break
                else:
                    logging.debug("     partial match")
        if break_out_flag:
            break
    return_df = pd.DataFrame.from_dict(cut_dict)
    return return_df

def cut_to_column_on_keywordmatch(input_df, config_command):
    keyword_list = None
    directionality = None

    keyword_list = config_command["Keyword_List"]
    directionality = config_command["Direction"]

    return _cut_to_column_on_keywordmatch(input_df=input_df, keyword_list=keyword_list, directionality=directionality)

_TYPES_cut_to_row_on_keywordmatch = Literal["from_top", "from_bottom"]


def _cut_to_row_on_keywordmatch(input_df, keyword_list: list, directionality: _TYPES_cut_to_row_on_keywordmatch):
    assert directionality in get_args(_TYPES_cut_to_row_on_keywordmatch), \
        f"'{directionality}' is invalid - valid options are {get_args(_TYPES_cut_to_row_on_keywordmatch)}"
    my_dict = input_df.to_dict(orient="list")
    key_list = []
    break_out_flag = False
    cut_dict = {}
    for keys in my_dict:
        logging.debug(f"     {keys},\n      {my_dict[keys]}")
        key_list.append(keys)

    # dictate searching order, top to bottom or bottom to top
    order_list = []
    for row_index in range(len(my_dict[key_list[0]])):
        order_list.append(row_index)
    if directionality == "from_bottom":
        order_list = order_list[::-1]

    # iterate through all rows
    for row_count in order_list:
        for col_count, col_name in enumerate(key_list):
            curr_item = my_dict[col_name][row_count]
            # logging.debug(f"      Current Item: Row: {row_count}, Col: {col_name} - Item: {my_dict[col_name][row_count]}/{curr_item} vs Comp: {keyword_list[0]}")

            if keyword_list[0] == curr_item:
                sub_key_list = key_list[col_count:col_count + len(keyword_list)]
                logging.debug(f"        Sub key list: {sub_key_list}")

                # on match get the values of that row from all columns
                row_data = []
                for col_names in sub_key_list:
                    row_data.append(my_dict[col_names][row_count])
                logging.debug(f"        Row Data: {row_data}")

                if len(row_data) < len(keyword_list):
                    logging.debug("     Did break case as row_data was too short")
                    break
                else:
                    # check for a full match between row data and the keyword_list
                    match_list = []
                    for i, j in zip(row_data, keyword_list):
                        if i != j:
                            logging.debug(f"     row data does not match keyword list, {i} != {j}")
                            break
                        else:
                            logging.debug("     row data matches keyword list")
                            match_list.append(j)
                            logging.debug(f"     matchlist: {match_list}")
                    # on full match cut the df (currently in dict form) down to the selected starting row
                    if match_list == keyword_list:
                        logging.debug("     FULL MATCH for Row and Keyword List")
                        for dict_keys in key_list:
                            if directionality == "from_top":
                                cut_dict[dict_keys] = my_dict[dict_keys][row_count:]
                            else:
                                cut_dict[dict_keys] = my_dict[dict_keys][:row_count + 1]
                        logging.debug(f"     cut dict: {cut_dict}")
                        break_out_flag = True
                        break

        if break_out_flag:
            break
        else:
            logging.debug("     No Match in this Column")
            pass
    return_df = pd.DataFrame.from_dict(cut_dict)
    return return_df


def cut_to_row_on_keywordmatch(input_df, config_command):
    keyword_list = None
    directionality = None

    keyword_list = config_command["Keyword_List"]
    directionality = config_command["Direction"]

    return _cut_to_row_on_keywordmatch(input_df=input_df, keyword_list=keyword_list, directionality=directionality)

def _isolate_segment(input_df, target_row, split_char, target_segment):
    splitting_dict = input_df.to_dict(orient="list")
    # TODO docu
    for count, items in enumerate(splitting_dict[target_row]):
        try:
            current_list = items.split(split_char)
        except AttributeError:
            items = str(items)
            current_list = items.split(split_char)

        try:
            splitting_dict[target_row][count] = current_list[target_segment].strip()
        except IndexError:
            splitting_dict[target_row][count] = current_list[len(current_list) - 1].strip()

    return_df = pd.DataFrame.from_dict(splitting_dict)
    return return_df


def isolate_segment(input_df, config_command):

    Column_Name = None
    Splitting_Character = None
    Wanted_Segment = None

    Column_Name = config_command["Column_Name"]
    Splitting_Character = config_command["Splitting_Character"]
    Wanted_Segment = config_command["Wanted_Segment"]

    return _isolate_segment(input_df=input_df, target_row=Column_Name, split_char=Splitting_Character, target_segment=Wanted_Segment)


def _slice_string_segment(x, chars_kept, direction):

    x_str = str(x)

    if direction == "From_Left":
        x_str = x_str[:chars_kept]
    elif direction == "From_Right":
        slicer = len(x_str)-chars_kept
        x_str = x_str[slicer:]
    else:
        raise Exception("Invalid Command for direction")

    return x_str

def slice_string_segment(input_df, config_command):

    # todo assert + typing and multiple columns
    target_col = config_command["Column_Name"]
    chars_kept = config_command["Chars_Kept"]
    direction = config_command["Direction"]


    input_df[target_col] = input_df[target_col].apply(_slice_string_segment, chars_kept=chars_kept, direction=direction)

    return input_df

def _drop_duplicate_rows_by_col(input_df, col_name):
    out_df = input_df.drop_duplicates(subset=[col_name])
    return out_df

def drop_duplicate_rows_by_col(input_df, config_command):

    return _drop_duplicate_rows_by_col(input_df, col_name=config_command["Column_Name"])

def _drop_duplicate_rows(input_df):
    out_df = input_df.drop_duplicates()
    return out_df

def drop_duplicate_rows(input_df):

    return _drop_duplicate_rows(input_df)