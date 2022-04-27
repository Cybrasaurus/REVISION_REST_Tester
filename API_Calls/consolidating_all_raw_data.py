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
    print(records_from_df)
    print(type(records_from_df))

    print(type(records_from_df[0]))
    currency_code_list = []
    for items in records_from_df:
        outitem = list(items)
        currency_code_list.append(outitem)
    #print(excel_df)
    print(currency_code_list)

    for countries in currency_code_list:
        for country_data in countries
if __name__ == "__main__":
    pass
    #country_translate_dict()
    #clean_translate_country()
    combine_country_and_excel()