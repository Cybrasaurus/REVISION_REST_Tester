import logging

import pandas as pd
from typing import Literal, get_args
from contextlib import suppress


def _fill_rows_with_fixed_number(x, fixed_number):
    return fixed_number


def _fill_rows_with_incremental(input_df, col_name, start_number, increment):
    splitting_dict = input_df.to_dict(orient="list")

    for row_nr in range(len(splitting_dict[col_name])):
        splitting_dict[col_name][row_nr] = start_number
        start_number += increment
    return pd.DataFrame.from_dict(splitting_dict)


def _fill_rows_with_random_number(x, random_range):
    import random
    return random.randrange(random_range[0], random_range[1] + 1, random_range[2])


_TYPES_fill_mode_variants = Literal["Fixed", "Incremental", "Random"]


def fill_rows_with_numbers(input_df, config_commands):
    fill_mode = config_commands["Fill_Mode"]
    assert fill_mode in get_args(_TYPES_fill_mode_variants), \
        f"'{fill_mode}' is invalid - valid options are {get_args(_TYPES_fill_mode_variants)}"

    column_names = config_commands["Column_Names"]

    fixed_number = None
    random_range = None
    with suppress(KeyError):
        fixed_number = config_commands["Fixed_Number"]
    with suppress(KeyError):
        random_range = config_commands["Random_Number_Range"]
        assert type(random_range) == list or random_range is None, logging.error(
            "      Random_Number_Range needs to be a list")
        if type(random_range) == list:
            if len(random_range) == 2:
                logging.info("       No Random Step specified, defaulting to 1")
                random_range.append(1)




    for column_name in column_names:
        if fill_mode == "Fixed":
            if fixed_number is None:
                logging.info("       Did not specify a fixed number, defaulting to 0")
                fixed_number = 0
            input_df[column_name] = input_df[column_name].apply(_fill_rows_with_fixed_number, fixed_number=fixed_number)
        elif fill_mode == "Incremental":
            start_number = None
            increment_step = None
            with suppress(KeyError):
                start_number = config_commands["Starting_Number"]
            with suppress(KeyError):
                increment_step = config_commands["Increment_Step"]
            if start_number is None:
                start_number = 0
                logging.info("       Incremental Start Number not specified, defaulting to 0")
            if increment_step is None:
                increment_step = 1
                logging.info("       Incremental Step not specified, defaulting to 1")
            return _fill_rows_with_incremental(input_df=input_df, col_name=column_name, start_number=start_number,
                                               increment=increment_step)
        elif fill_mode == "Random":
            if random_range is None:
                logging.warning("       Did not specify a random range, defaulting to 0-1000")
                random_range = [0, 1000, 1]
            input_df[column_name] = input_df[column_name].apply(_fill_rows_with_random_number,
                                                                random_range=random_range)
    return input_df