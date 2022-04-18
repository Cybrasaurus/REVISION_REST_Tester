import requests

def get_currency_info(city):
    """
    This function calls the CurrencyScoop API.
    tbd The returned object is converted to a json, in the metric System
    tbd :param city: the name of the city
    tbd :return: a touple consisting of the weather, weather description and the temperature
    """
    
    url1 = "https://currencyscoop.p.rapidapi.com/currencies"
    url2 = "https://currencyscoop.p.rapidapi.com/latest?base=USD"     
    headers = {
        "X-RapidAPI-Host": "currencyscoop.p.rapidapi.com",
	    "X-RapidAPI-Key": "14b2a42e1cmsh8b4668038092d99p17c629jsnbdd3c14469b1"}
    response1 = requests.request("GET", url1, headers= headers) 
    response2 = requests.request("GET", url2, headers= headers)

    try:
        if response1["cod"] != "200" or response2 ["cod"] != "200":
            return f"Error with the Currency API Call: {json_object['message']}, Error {json_object['cod']}"
    except:
        res1 = response1.json()
        res2 = response2.json()
        return res1["response"]["fiats"]["AOA"], res2 ["response"]["rates"]["AOA"]

    
    