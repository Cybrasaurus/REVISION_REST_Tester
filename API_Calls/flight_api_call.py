# TODO: the api calls here
import requests

from .Currency_api_data_to_df import opener


def get_flight_info(city, country):
    try:
        #todo update location + relative imports
        dict_of_dicts = opener("API_Calls/Cleaned_IATA_V3")
        #dict_of_dicts = opener("Cleaned_IATA_V3")
        iata_code = dict_of_dicts[country][city]
        print(iata_code)
        print(type(iata_code))


        if len(iata_code) == 0:
            return ["Error", f"Country({country}) and City({city}) in Database, but no Airport for that City"]

        else:
            for items in iata_code:
                url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/cheap"

                querystring = {"origin": "STR", "page": "None", "currency": "EUR", "destination": {items}}

                headers = {
                    "X-Access-Token": "488367f9770fafd22215497b309bb23c",
                    "X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
                    "X-RapidAPI-Key": "b56a5bba8dmsh785f91ec855be3ep1188aejsn8d77cf720f02"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                json_object = response.json()
                print("printing json object")
                print(json_object)
                print(json_object["success"])
                if str(json_object["success"]) == "False":
                    print("going into false case")
                    return ["Error", f"Error reason: {json_object['error']}"]

                else:
                    print("else case, before for loop")
                    key_list = []
                    for keys in json_object["data"]:
                        key_list.append(keys)
                    print(key_list)
                    new_iata_key = key_list[0]
                    print(new_iata_key)

                    for keys in json_object["data"][new_iata_key]:
                        for subitems in json_object["data"][new_iata_key][keys]:
                            #print(subitems)
                            json_object["data"][new_iata_key][keys][subitems] = str(json_object["data"][new_iata_key][keys][subitems])
                    print("else case, after for loop")
                    return ["Success", json_object["data"][new_iata_key]]

    except KeyError:
        print("Flight API - KeyError")
        return ["Error", "City not found in Database"]


if __name__ == "__main__":
    get_flight_info(city="New York", country="United States")

    # print(response.text)

    # flight_price = json_object["data"]["price"]
    # flight_airline = json_object["data"]["airline"]

    # weather_main = json_object["weather"][0]["main"]
    # weather_desc = json_object["weather"][0]["description"]
    # weather_temp = json_object["main"]["temp"]
    # return flight_price, flight_airline

# print(flight_airline)


# return
