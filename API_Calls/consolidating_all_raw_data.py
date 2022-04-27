from Currency_api_data_to_df import opener, saver
import pandas as pd

def country_translate_dict():
    countries_en = opener("countries_en")
    countries_de = opener("countries_de")


    Translate_Dict = {}
    for items in countries_en:
        print(items)
        sub_dict = {
            "EN_Name": "",
            "DE_Name": "",
            "alpha3": "",
        }
        sub_dict["EN_Name"] = items["name"]
        sub_dict["alpha3"] = items["alpha3"]

        Translate_Dict[items["name"]] = sub_dict

    print(Translate_Dict)

    for items in countries_de:
        for countries in Translate_Dict:
            if Translate_Dict[countries]["alpha3"] == items["alpha3"]:
                Translate_Dict[countries]["DE_Name"] = items["name"]

    print(Translate_Dict)

    saver(filename="country_translation", file_content=Translate_Dict)

def clean_translate_country():
    dict_to_clean = opener("country_translation")

    for items in dict_to_clean:
        print(items)
        print(dict_to_clean[items]["DE_Name"])
        dict_to_clean[items]["DE_Name"] = dict_to_clean[items]["DE_Name"]

    saver(filename="country_translation_clean", file_content=dict_to_clean)

def combine_country_and_excel():
    excel_df = pd.read_excel("currency-codes.xlsx", header=None)

    records_from_df = excel_df.to_records(index=False)
    records_from_df = list(records_from_df)
    #print(records_from_df)
    #print(type(records_from_df))

    #get excel data, convert into df
    print(type(records_from_df[0]))
    currency_code_list = []
    for items in records_from_df:
        outitem = list(items)
        currency_code_list.append(outitem)
    #print(excel_df)
    #print(currency_code_list)

    #convert df into usable form
    countries_list = []
    for countries in currency_code_list:

        country_data_list = []
        for country_data in countries:
            #print(country_data)
            if isinstance(country_data, str):
                country_data_list.append(country_data.lower())
            else:
                country_data_list.append(country_data)
        countries_list.append(country_data_list)
        #print(country_data_list)

    #print(countries_list)
    country_translater = opener("country_translation_cleaned")

    #actually combine and transfer data
    for keys in country_translater:
        #print(keys.lower())
        for countries in countries_list:
            #print(countries)
            if country_translater[keys]["DE_Name"].lower() == countries[0]:
                #print(f"match: {countries[0]}")
                country_translater[keys]["Currency Name"] = countries[1]
                country_translater[keys]["Currency Short"] = countries[2]
                country_translater[keys]["Currency Code"] = str(int(countries[3]))
    #print(country_translater)

    saver(filename="Countries_translate_and_curr_code", file_content=country_translater)

def combine_curr_codes_and_IATA_data():
    iata_json = opener("Cleaned_IATA_V3")
    curr_json = opener("Countries_translate_and_curr_code")

    for keys in iata_json:
        pass
        #print(keys)
        for countries in curr_json:
            #print(f"countries in cur_json: {countries}")
            if keys.lower() == countries.lower():
                print(keys.lower())
                currency_data_dict = {}
                try:
                    currency_data_dict["Currency Name"] = curr_json[countries]["Currency Name"]
                    currency_data_dict["Currency Short"] = curr_json[countries]["Currency Short"]
                    currency_data_dict["Currency Code"] = curr_json[countries]["Currency Code"]
                except KeyError:
                    currency_data_dict["Currency Name"] = "No Data"
                    currency_data_dict["Currency Short"] = "No Data"
                    currency_data_dict["Currency Code"] = "No Data"
            #print(currency_data_dict)
            iata_json[keys]["Currency_data"] = currency_data_dict
    saver(filename="Cleaned_IATA_V3_and_Curr", file_content=iata_json)


def combine_big_mac_with_total_list():
    big_mac_data = opener("Big_mac_data_modified")
    big_list = opener("Cleaned_IATA_V3_and_Curr")

    for items in big_mac_data:
        print(items["Country Name"])

        dict_to_insert = {
            "Local Big Mac Price": items["Local Big Mac Price"],
            "Local Big Mac Price in Euro": items["Local Big Mac Price in Euro"],
            "Relative Cost for BigMac to Germany": items["Relative Cost for BigMac to Germany"],
        }
        try:
            big_list[items["Country Name"]]["Big Mac Data"] =  dict_to_insert
        except KeyError:
            pass
    saver("final_database", big_list)


if __name__ == "__main__":
    pass
    #country_translate_dict()
    #clean_translate_country()
    #combine_country_and_excel()
    #combine_curr_codes_and_IATA_data()
    combine_big_mac_with_total_list()