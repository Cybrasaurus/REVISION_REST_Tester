from contextlib import suppress
from copy import deepcopy
import pandas as pd
import logging
from typing import Literal, get_args


def _combine_excels_on_match(input_df, aux_excel_loading, target_column, compared_column,
                             transferred_column_list):
    from Functions.File_Manipulation import load_excel

    aux_excel = load_excel(aux_excel_loading)

    splitting_dict = input_df.to_dict(orient="list")
    modifying_dict = deepcopy(splitting_dict)
    aux_dict = aux_excel.to_dict(orient="list")

    # for existing_column in modifying_dict:
    #    logging.debug(f"      Main_DF_Column: {existing_column}")
    #    if existing_column in transferred_column_list:
    #        logging.debug(f"        Transfer Column ({existing_column} already exists in main DF")
    for new_columns in transferred_column_list:
        if new_columns in modifying_dict.keys():
            logging.debug(f"        Transfer Column ({new_columns} already exists in main DF")
            modifying_dict[new_columns] = splitting_dict[new_columns]
        else:
            modifying_dict[new_columns] = []
            for times in range(len(splitting_dict[target_column])):
                modifying_dict[new_columns].append("")

    # items = entry1, entry2...
    for primary_count, items in enumerate(splitting_dict[target_column]):
        # potential_matches = potent1, potent2...
        for count, potential_matches in enumerate(aux_dict[compared_column]):
            if str(items) in str(potential_matches):
                for transfers in transferred_column_list:
                    modifying_dict[transfers][primary_count] = (aux_dict[transfers][count])
        try:
            logging.debug(f"        Current Col: {transfers}, combined content: {modifying_dict[new_columns]}")
        except UnboundLocalError:
            continue

    return_df = pd.DataFrame.from_dict(modifying_dict)
    return return_df


def combine_excels_on_match(input_df, config_command):

    #todo add option here to discard data once it has been combined


    Aux_Excel_sheet_name = 0

    Auxiliary_Excel_Name = config_command["Auxiliary_Excel_Name"]
    Aux_Excel_Loader_Variant = config_command["Aux_Excel_Loader_Variant"]
    Aux_Excel_File_Location = config_command["Aux_Excel_File_Location"]
    with suppress(KeyError):
        Aux_Excel_sheet_name = config_command["Aux_Excel_sheet_name"]
    Main_Excel_Column = config_command["Main_Excel_Column"]
    Compared_Column = config_command["Compared_Column"]
    Transferred_Column_Names = config_command["Transferred_Column_Names"]

    aux_excel_load_dict = {
        "File_Name": Auxiliary_Excel_Name,
        "File_Location": Aux_Excel_File_Location,
        "Sheet_Name": Aux_Excel_sheet_name,
        "Headers": Aux_Excel_Loader_Variant
    }

    return _combine_excels_on_match(input_df=input_df, aux_excel_loading=aux_excel_load_dict,
                                    target_column=Main_Excel_Column, compared_column=Compared_Column,
                                    transferred_column_list=Transferred_Column_Names)


def _concat_dataframes(input_df_list):
    from Functions.File_Manipulation import load_excel

    combine_list = []

    for dicts in input_df_list:
        combine_list.append(load_excel(dicts))

    return_df = pd.concat(combine_list, axis=0)
    return return_df


def concat_dataframes(config_command):
    dataframe_list = None
    dataframe_list = config_command["Dataframe_List"]

    return _concat_dataframes(input_df_list=dataframe_list)


_TYPES_add_value_to_columns_position = Literal["First", "Last"]


def _add_value_to_columns(input_df, column_name_list, added_value, combination_chars, insert_position):
    assert insert_position in get_args(_TYPES_add_value_to_columns_position), \
        f"'{insert_position}' is invalid - valid options are {get_args(_TYPES_add_value_to_columns_position)}"

    logging.debug("attempting conversion to dict")
    splitting_dict = input_df.to_dict(orient="list")

    logging.debug("start of first for loop")
    for column_name in column_name_list:
        logging.debug(f"colname: {column_name}")
        for count, row in enumerate(splitting_dict[column_name]):
            logging.debug(f"Count: {count}, row:{row}")
            current_data = row
            if str(current_data) =="nan":
                current_data = ""

            if insert_position == "First":
                combined_data = f"{added_value}{combination_chars}{current_data}"
            elif insert_position == "Last":
                combined_data = f"{current_data}{combination_chars}{added_value}"
            splitting_dict[column_name][count] = combined_data

    return_df = pd.DataFrame.from_dict(splitting_dict)
    return return_df


def add_value_to_columns(input_df, config_commands):
    insert_position = "Last"
    combination_chars = ""

    column_name_list = config_commands["Column_Name_List"]
    added_value = config_commands["Added_String"]
    with suppress(KeyError):
        insert_position = config_commands["Insert_Position"]
    with suppress(KeyError):
        combination_chars = config_commands["Combination_Chars"]

    logging.debug("got all config commmands, going to main")
    logging.debug(f"{input_df}")
    return _add_value_to_columns(input_df=input_df, column_name_list=column_name_list, added_value=added_value,
                                 combination_chars=combination_chars, insert_position=insert_position)


def _combine_cols(input_df, combined_name, source_col_list, combine_chars):

    input_df[combined_name] = input_df[source_col_list].agg(str(combine_chars).join, axis=1)

    return input_df


def combine_cols(input_df, config_commands):

    combined_name = config_commands["Combined_Column_Name"]
    source_col_list = config_commands["Column_Names"]
    combine_chars = config_commands["Combination_Characters"]

    return _combine_cols(input_df=input_df, combined_name=combined_name, source_col_list=source_col_list, combine_chars=combine_chars)