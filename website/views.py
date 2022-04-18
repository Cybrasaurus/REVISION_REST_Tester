
from flask import Blueprint, render_template, request, redirect, url_for, flash
from API_Calls import get_data_from_name, get_currency_info

views = Blueprint("views", __name__)

destination_city=""
destination_country=""

#TODO second form for getting the country in home

"""
-Vorschlag Luxusreise
-auswahl in eu oder ausland
-most popular destination based on currency rate/location?
-know more about city
-similar cities
-big mac index or other currency index


"""

def city_and_country_checker():
    """
    This function checks whether the global variables destination_city and destination_country are assigned values rather than "".
    This prevents access to the other routes of the website until a valid input has been given
    :return: True, if both are given, otherwise False, which redirects to the main page
    """
    global destination_city
    global destination_country

    if destination_city != "" and destination_country != "":
        flash("City & Country Accepted", "alert")
        return True
    else:
        if destination_city == "" and destination_country == "":
            flash("Please enter a city and country first", "error")
            return False
        if destination_city == "":
            flash("Please enter a city first", "error")
            return False
        if destination_country == "":
            flash("Please enter country first", "error")
            return False

@views.route("/", methods=["GET", "POST"])
def home():
    """
    Main Starting Page, enter name of destination city here.
    Checks whether a City name is input before redirecting
    :return html Template:
    """
    if request.method == 'POST':
        global destination_city
        global destination_country

        destination_city = request.form.get('destination')
        destination_country = request.form.get('country')

        my_bool = city_and_country_checker()
        if my_bool:
            return redirect(url_for("views.got_city"))
        else:
            return redirect(url_for("views.home"))
    return render_template("home.html")

#TODO update check for both country and city

@views.route("/weather")
def weather():
    """
    Display the weather information page. Check for valid city name.
    Calls the Openweathermap API for information, which returns a list with the relevant data
    :return html Template:
    """
    global destination_city
    global destination_country

    my_bool = city_and_country_checker()
    if my_bool:
        returnlist = get_data_from_name(destination_city)
        if isinstance(returnlist, str):
            return render_template("404.html",
                                   errorcode="Something went wrong with the API Call of the Openweathermap, the error message is below:",
                                   errormessage=returnlist)

        else:
            w_main = returnlist[0]
            w_desc = returnlist[1]
            w_temp = returnlist[2]
            return render_template("weather.html", destination_name=destination_city, weather_main=w_main,
                                   weather_desc=w_desc, weather_temp=w_temp)
    else:
        return redirect(url_for("views.home"))


@views.route("/cur_rate")
def cur_rate():

    my_bool = city_and_country_checker()
    if my_bool:

        #TODO @Elisabeth code goes here now

        returncur = get_currency_info(destination_city)
        # if isinstance(returncur, str):
        #    return render_template("404.html",
        #                           errorcode="Something went wrong with the API Call of the Openweathermap, the error message is below:",
        #                           errormessage=returnlist)
        c_main = returncur[0]
        c_latest = returncur[1]
        return render_template("currency_rate.html", cur_main=c_main, cur_latest=c_latest)
    else:
        return redirect(url_for("views.home"))



@views.route("/flights")
def flights():
    my_bool = city_and_country_checker()
    if my_bool:
        pass
        return render_template("404.html",
                                   errorcode="Page is still under construction:",
                                   errormessage="Working on It")
        #TODO code for the website here
    else:
        return redirect(url_for("views.home"))

@views.route("/got_city")
def got_city():
    """
    Display redirect page with the 3 main links for weather, currency and flights. Same check for City Name.
    Get redirected here if a City Name is input
    :return html Template:
    """

    my_bool = city_and_country_checker()
    if my_bool:
        return render_template("got_city.html", destination_name= destination_city)
    else:
        return redirect(url_for("views.home"))

