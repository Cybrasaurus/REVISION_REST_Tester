#todo read in configs to do the commands, have optional keyword handling here
import json
import logging
import sys

def config_loader(file_name:str):
    assert type(file_name) == str
    return_config = None
    try:
        with open(f"{file_name}.json", encoding="utf-8") as json_file:
            return_config = json.load(json_file)
        assert return_config is not None
    except json.decoder.JSONDecodeError as json_error:
        logging.error(f"ERROR: Config Read-In: {json_error}\n This error usually means the json file does not contain a valid data structure")
    except FileNotFoundError as file_error:
        logging.error(f"ERROR: Config Read-In: {file_error}\n This error means the given name for the json file is wrong, please check")
    except AssertionError:
        logging.error("ERROR: Config Read-in, error during reading of config, is still null")

    if return_config == None:
        sys.exit()
    else:
        logging.info("      Successfully Loaded Config")
        return return_config