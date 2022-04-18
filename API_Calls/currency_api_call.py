import requests
import openpyxl 
import os
import json

def get_currency_info(country):
    """
    This function calls the CurrencyScoop API.
    tbd The returned object is converted to a json, in the metric System
    :param country: the name of the country 
    tbd :return: a touple consisting of the weather, weather description and the temperature
    """
    
    url1 = "https://currencyscoop.p.rapidapi.com/currencies"
    url2 = "https://currencyscoop.p.rapidapi.com/latest?base=EUR"      #u can specify base currency here
    headers = {
        "X-RapidAPI-Host": "currencyscoop.p.rapidapi.com",
	    "X-RapidAPI-Key": "14b2a42e1cmsh8b4668038092d99p17c629jsnbdd3c14469b1"}
    response1 = requests.request("GET", url1, headers= headers) 
    response2 = requests.request("GET", url2, headers= headers)

    cc = get_curcode (country)

    res1 = response1.json()
    res2 = response2.json()

    cod1 = res1["meta"]["code"]
    cod2 = res2["meta"]["code"]
    result1 = res1["response"]["fiats"][cc]
    result2 = res2["response"]["rates"][cc]

    if type(cc) != str:
        return "Couldn't get currency code of " + country  

    elif cod1 != 200 or cod2 != 200:
        return f"Error with the Currency API Call: HTTP response codes {cod1} and {cod2}, take a look on https://currencyscoop.com/api-documentation"
    
    elif type (result1) != dict:
        return f"Couldn't find any information on currency code {cc}"
    
    else:
        print(res1)
        with open("res1.json", "w") as outfile:
            json.dump(res1, outfile, indent=3)
        with open("res2.json", "w") as outfile:
            json.dump(res2, outfile, indent=3)
        return result1, result2

def get_curcode (country):
    #xlsx created with data from https://de.iban.com/currency-codes, changed it a bit myself
    currency_code_file = openpyxl.load_workbook(os.getcwd() + '/API_Calls/currency-codes.xlsx').get_sheet_by_name("Sheet1")
    try:
        for i in range(1,currency_code_file.max_row):
            if currency_code_file.cell(row=i, column=1).value == country.upper():
                return currency_code_file.cell(row=i, column=3).value        
    except:
        return none


    #TODO durchschnittlicher kurs des zeitraums, gerade billiger oder teuerer, prozentangabe + absolute werte