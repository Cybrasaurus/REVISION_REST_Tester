import json
import pandas as pd


def saver(filename, file_content):
    """
    This function saves any object (json file, string, integer...) into a jsonfile.

    :param filename: The name of the saved file
    :param file_content: the content that gets to be saved
    """
    with open(f"{filename}.json", "w") as outfile:
        json.dump(file_content, outfile, indent=2)


def opener(filename):
    """
    This function opens any local json file and returns the object inside
    :param filename: the name of the json file
    :return: the contents of the json file
    """
    with open(f"{filename}.json") as infile:
        loaded_data = json.load(infile)
    return loaded_data


def editer(iterations_to_edit, json_to_edit):
    """
    This function generates fake data to generate the pandas dataframe with

    First: load the initial data with the opener()

    iterate through all the country rates and increase the number there by one, then save a copy of that before iterating through it again
    -the copy is names "test_res_i", i being the current iteration
    the amount of iterations is given as a paramenter

    :param iterations_to_edit: how many iterations to do, i.e. how many sets of fake data to generate
    :return: nothing, it saves the data locally
    """
    opener("res2")
    for i in range(iterations_to_edit):
        for key in json_to_edit["response"]["rates"]:
            json_to_edit["response"]["rates"][f"{key}"] = json_to_edit["response"]["rates"][f"{key}"]+1
            # print(key)
        saver(f"test_res_{i}", json_to_edit)


def to_df(amount_datasets: int):
    """
    This functions loads the saved json datasets for a certain amount of times, strips the info down to the relevant bits,
    and then adds it to a list of dictionaries, which later gets converted to a pandas dataframe
    :param amount_datasets: how many datasets there are and need to be opened
    :return: the finished dataframe
    """

    list_of_dicts = []
    for i in range(amount_datasets):
        processing_dict = opener(f"data{i+1}")
        processing_dict = processing_dict["response"]["rates"]
        list_of_dicts.append(processing_dict)

    my_df = pd.DataFrame.from_records(list_of_dicts)

    #print(my_df)
    return my_df


def get_df_data(input_df, df_column):
    """
    Generates the mean/average of a certain column of a df, returning it
    :param input_df: the pandas dataframe, from which the mean is generated
    :param df_column: the name of the column of the dataframe
    :return: the mean of said column, as a float
    """
    cur_mean = input_df[f"{df_column}"].mean()
    #print(cur_mean)
    return cur_mean


def get_column_heads(input_df):
    """
    This function prints the Headers of all columns. Mostly for debugging and seeing what inputs can be used in the
    get_df_data() function, 'df_column' parameter
    :param input_df: the dataframe where the headers are to be read
    :return: a list of the headers
    """
    header_list = list(input_df.columns)
    print(header_list)
    return header_list


if __name__ == "__main__":

    #TODO @Elisabet hier die anzahl and durchgängen, 7 um eine woche zu simulieren
 #   number_of_iterations = 7


    #load sample data
 #   json_sample_data = opener("res2")
    #generate fake data from sample data
 #   editer(number_of_iterations, json_sample_data)
    #generate pandas dataframe
#    numberdf = to_df(number_of_iterations)

    #TODO: 'ADA" durch beliebigen anderen code ersetzten, liste an codes wird mit get_column_heads() printed
    #get average of certain df column
#    get_df_data(numberdf, "ADA")
    #get head of all df columns
#    get_column_heads(numberdf)

    my_dict = {'success': True, 'data': {'AMS': {'1': {'price': 56251, 'airline': 'EY', 'flight_number': 431, 'departure_at': '2022-05-20T20:00:00+07:00', 'return_at': '2022-06-01T11:40:00+02:00', 'expires_at': '2022-04-24T15:38:51Z'}, '2': {'price': 70062, 'airline': 'PG', 'flight_number': 272, 'departure_at': '2022-04-24T10:20:00+07:00', 'return_at': '2022-04-27T11:40:00+02:00', 'expires_at': '2022-04-24T15:38:51Z'}}}, 'currency': 'RUB'}
    saver("flightdata", my_dict)