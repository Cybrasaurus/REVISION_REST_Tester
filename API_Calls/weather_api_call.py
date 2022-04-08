import requests

def get_data_from_name(city):
    """
    This function calls the Openweathermap API with the city name retrieved from the Form on the Homepage.
    The returned object is converted to a json, in the metric System
    :param city: the name of the city
    :return: a touple consisting of the weather, weather description and the temperature
    """
    r = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=14428be4e14c02529bffa4cfb8af156a&units=metric')
    json_object = r.json()

    try:
        if json_object["cod"] != "200":
            return f"Error with the API Call: {json_object['message']}, Error {json_object['cod']}"
    except:
        weather_main = json_object["weather"][0]["main"]
        weather_desc = json_object["weather"][0]["description"]
        weather_temp = json_object["main"]["temp"]
        return weather_main,weather_desc,weather_temp


if __name__ == "__main__":
    print(get_data_from_name("Ilsfeld"))