import numpy as np
import pandas as pd
import logging
from contextlib import suppress

# TODO for all here extend to list, multiple columns in 1 batch
def _mult_negative_one(x):
    if isinstance(x, int):
        x = x * -1
    elif isinstance(x, float):
        x = x * -1
    else:
        logging.warning(f"     Could not multiply by -1, not an Int or Float. Type: {type(x)}, {x}")
        x = x
    return x


def mult_negative_one(input_df, config_command):
    target_col = None
    target_col = config_command["Column_Name"]
    input_df[target_col] = input_df[target_col].apply(_mult_negative_one)
    return input_df


def _round_to_decimals(x, decimals):
    if isinstance(x, float):
        x = round(x, decimals)
    else:
        x = x
    return x


def round_to_decimals(input_df, config_command):
    target_col = None
    decimals = None
    target_col = config_command["Column_Name"]
    decimals = config_command["Decimal_Points"]
    input_df[target_col] = input_df[target_col].apply(_round_to_decimals, decimals=decimals)
    return input_df


def _round_to_power(x, power):
    if isinstance(x, int):
        x -= x % -power
    elif isinstance(x, float):
        x -= x % -power
    else:
        logging.warning(f"     Could not round to power, not an Int or Float. Type: {type(x)}, {x}")
        x = x
    return x


def round_to_power(input_df, config_command):
    target_col = None
    power = None
    target_col = config_command["Column_Name"]
    power = config_command["Power"]
    input_df[target_col] = input_df[target_col].apply(_round_to_power, power=power)
    return input_df


def _calc_date_difference(input_df, result_column_name, first_date_column, only_business):
    # todo rework very much, runs on today
    from datetime import datetime, date
    work_df = input_df
    #try:
    #work_df[first_date_column] = pd.to_datetime(input_df[first_date_column], format="%Y-%m-%d")
    #except Exception:
    #    logging.error("     Could not convert to datetime")

    my_dict = work_df.to_dict(orient="list")
    my_dict[result_column_name] = []
    logging.debug(f"     {my_dict[first_date_column]}")

    for count, row in enumerate(my_dict[first_date_column]):
        # todo this dynamic
        # d1 = datetime.strptime(row, "%Y-%m-%d %h:%i%s")
        d1 = row
        #d1 = d1.to_pydatetime()
        d2 = datetime.today()
        d2 = str(d2)
        d2 = d2.split(" ")[0]

        if only_business is None:
            delta = d1 - d2
            my_dict[result_column_name].append(delta.days)
        else:
            delta = np.busday_count(d1, d2)
            my_dict[result_column_name].append(delta)

    return_df = pd.DataFrame.from_dict(my_dict)
    return return_df


def calc_date_difference(input_df, config_command):
    result_column_name = None
    first_date_column = None
    only_business = None

    result_column_name = config_command["Result_Column_Name"]
    first_date_column = config_command["First_Date_Column"]
    with suppress(KeyError):
        only_business = config_command["Count_Only_Business_Days"]
    return _calc_date_difference(input_df=input_df, result_column_name=result_column_name,
                                 first_date_column=first_date_column, only_business=only_business)


def _positive_zero_or_negative(x):
    if type(x) != int and type(x) != float:
        return x
    else:
        if x == 0:
            return "zero"
        elif x > 0:
            return "positive"
        elif x < 0:
            return "negative"


def positive_zero_or_negative(input_df, config_command):
    target_col = None
    target_col = config_command["Column_Name"]
    input_df[target_col] = input_df[target_col].apply(_positive_zero_or_negative)
    return input_df


def _if_smaller_add_result(x, compare_number, result):
    if type(x) == int or type(x) == float:
        if x < compare_number:
            return result
        else:
            return x
    else:
        return x


def if_smaller_add_result(input_df, config_command):
    target_col = None
    compare_number = None
    result = None
    target_col = config_command["Column_Name"]
    compare_number = config_command["Compare_To_Number"]
    result = config_command["Result_Value"]

    input_df[target_col] = input_df[target_col].apply(_if_smaller_add_result, compare_number=compare_number,
                                                      result=result)
    return input_df

def _if_larger_add_result(x, compare_number, result):
    if type(x) == int or type(x) == float:
        if x > compare_number:
            return result
        else:
            return x
    else:
        return x


def if_larger_add_result(input_df, config_command):
    target_col = None
    compare_number = None
    result = None
    target_col = config_command["Column_Name"]
    compare_number = config_command["Compare_To_Number"]
    result = config_command["Result_Value"]

    input_df[target_col] = input_df[target_col].apply(_if_larger_add_result, compare_number=compare_number,
                                                      result=result)
    return input_df

