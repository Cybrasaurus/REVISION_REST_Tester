import logging
from typing import Literal, get_args
from contextlib import suppress
import pandas as pd

_TYPES_load_excel_loader_variant = Literal["Numeric_Headers", "Excel_Headers"]
_TYPES_load_excel_purge_umlaute = Literal[True, False]


def _load_excel(excel_file_name, excel_file_location, excel_sheet_name, loader_variant, purge_umlaute=True):
    ## TODO DOCU
    logging.info(f"      Loading Excel: {excel_file_location}/{excel_file_name}, page: {excel_sheet_name}")
    assert loader_variant in get_args(_TYPES_load_excel_loader_variant), \
        f"'{loader_variant}' is invalid - valid options are {get_args(_TYPES_load_excel_loader_variant)}"
    assert purge_umlaute in get_args(_TYPES_load_excel_purge_umlaute), \
        f"'{purge_umlaute}' is invalid - valid options are {get_args(_TYPES_load_excel_purge_umlaute)}"

    if loader_variant == "Excel_Headers":
        loader_variant = 0
    else:
        loader_variant = None

    return_df = pd.read_excel(f'{excel_file_location}/{excel_file_name}.xlsx', header=loader_variant,
                              sheet_name=excel_sheet_name)

    if purge_umlaute:
        umlaute_dict = {
            "ä": "ae",
            "ü": "ue",
            "ö": "oe"
        }
        return_df = return_df.replace(umlaute_dict, regex=True)

    return return_df


def load_excel(config_command):
    ## TODO DOCU
    excel_file_location = ""
    excel_sheet_name = 0
    loader_variant = None
    purge_umlaute = True

    print(config_command)

    excel_file_name = config_command["File_Name"]
    with suppress(KeyError):
        excel_file_location = config_command["File_Location"]
    with suppress(KeyError):
        excel_sheet_name = config_command["Sheet_Name"]
    with suppress(KeyError):
        loader_variant = config_command["Headers"]
    with suppress(KeyError):
        loader_variant = config_command["purge_umlaute"]

    return _load_excel(excel_file_name=excel_file_name, excel_file_location=excel_file_location,
                       excel_sheet_name=excel_sheet_name, loader_variant=loader_variant)


def _create_excel(input_df, excel_name, excel_location, keep_index):
    assert type(excel_name) == str
    assert type(excel_location) == str
    try:
        input_df.to_excel(f"{excel_location}/{excel_name}.xlsx", index=keep_index)
    except PermissionError:
        logging.critical(
            f"     Could not write to {excel_location}/{excel_name}, make sure to close them, then try again")
        input("If closed, press 'r' and enter to rerun")
        logging.info("      Attempting Rerun")
        _create_excel(input_df, excel_name, excel_location, keep_index)


def create_excel(input_df, config_command):
    excel_name = None
    excel_location = None
    keep_index = False
    excel_name = config_command["Excel_Name"]
    excel_location = config_command["Excel_Location"]
    with suppress(KeyError):
        keep_index = config_command["Keep_Index"]
        if keep_index == "True":
            logging.debug("      kept index when creating")
            keep_index = True
    _create_excel(input_df=input_df, excel_name=excel_name, excel_location=excel_location, keep_index=keep_index)


_TYPES_remove_files_variant = Literal["Single_File", "File_Type"]


def _remove_files(file_name, file_extension, path, remove_type="Single_File"):
    assert remove_type in get_args(_TYPES_remove_files_variant), \
        f"'{remove_type}' is invalid - valid options are {get_args(remove_type)}"
    import os

    if remove_type == "Single_File":

        full_file = f"{file_name}.{file_extension}"
        logging.info(f"      Attempting to remove '{full_file}' in '{path}'")
        file_name_and_path = os.path.join(path, full_file)
        if os.path.exists(file_name_and_path):
            os.remove(file_name_and_path)
            logging.info(f"      Deleted '{file_name_and_path}'")
        else:
            logging.warning(f"      Could not find file '{file_name_and_path}', skipping delete")
    elif remove_type == "File_Type":
        logging.info(f"     Attempting to remove all files in '{path}' with the extension '{file_extension}'")

        file_list = os.listdir(path)
        for files in file_list:
            if files.endswith(f".{file_extension}"):
                os.remove(os.path.join(path, files))
        logging.info(f"     Found and removed {len(file_list)} files")


def remove_files(config_commands):
    file_name = None
    path = ""

    with suppress(KeyError):
        file_name = config_commands["File_Name"]
    with suppress(KeyError):
        path = config_commands["File_Path"]
    file_extension = config_commands["File_Extension"]
    remove_type = config_commands["Remove_Type"]

    _remove_files(file_name=file_name, file_extension=file_extension, path=path, remove_type=remove_type)