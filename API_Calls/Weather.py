import requests


zipcode = "02108"

def get_temperature_by_zip(zipcode):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',us&appid=14428be4e14c02529bffa4cfb8af156a&units=metric')
    print(type(r))
    json_object = r.json()
    print(type(json_object))
    print(json_object)
    print(json_object["weather"])
    print(json_object["main"])
    return r


#get_temperature_by_zip(zipcode)
print("--------")

#https://openweathermap.org/current
#https://openweathermap.org/api/geocoding-api
#https://openweathermap.org/current#name

def get_data_from_name(city):
    r = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=14428be4e14c02529bffa4cfb8af156a&units=metric')
    print(type(r))
    json_object = r.json()
    print(type(json_object))
    print(json_object)

    print("-----------")
    weather_main = json_object["weather"][0]["main"]
    weather_desc = json_object["weather"][0]["description"]
    weather_temp = json_object["main"]["temp"]

    return weather_main,weather_desc,weather_temp

print(type(list(get_data_from_name("Gießen"))))