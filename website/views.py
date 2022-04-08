
from flask import Blueprint, render_template, request, redirect, url_for, flash
from API_Calls import get_data_from_name

views = Blueprint("views", __name__)

destination_city=""



@views.route("/", methods=["GET", "POST"])
def home():
    """
    Main Starting Page, enter name of destination city here.
    Checks whether a City name is input before redirecting
    :return html Template:
    """
    if request.method == 'POST':
        destination_name = request.form.get('destination')
        print(destination_name)

        global destination_city
        destination_city=destination_name
        if destination_city != "":
            flash("City Accepted", "alert")
            return redirect(url_for("views.got_city"))
        else:
            flash("Please enter a city came first", "error")
            return redirect(url_for("views.home"))
    return render_template("home.html")


@views.route("/weather")
def weather():
    """
    Display the weather information page. Check for valid city name.
    Calls the Openweathermap API for information, which returns a list with the relevant data
    :return html Template:
    """
    global destination_city



    if destination_city == "":
        flash("Please enter a city came first", "error")
        return redirect(url_for("views.home"))
    else:
        returnlist = get_data_from_name(destination_city)
        if isinstance(returnlist, str):
            return render_template("404.html",
                                   errorcode="Something went wrong with the API Call of the Openweathermap, the error message is below:",
                                   errormessage=returnlist)

        else:
            w_main=returnlist[0]
            w_desc = returnlist[1]
            w_temp = returnlist[2]
            return render_template("weather.html", destination_name=destination_city, weather_main=w_main, weather_desc=w_desc, weather_temp=w_temp)

@views.route("/cur_rate")
def cur_rate():
    if destination_city == "":
        flash("Please enter a city came first", "error")
        return redirect(url_for("views.home"))

    #TODO: add content from currency rate API call and maths here

    else:
        return render_template("currency_rate.html")

@views.route("/flights")
def flights():
    if destination_city == "":
        flash("Please enter a city came first", "error")
        return redirect(url_for("views.home"))

    # TODO: add content from flights API call and maths here

    else:
        return render_template("flights.html")

@views.route("/got_city")
def got_city():
    """
    Display redirect page with the 3 main links for weather, currency and flights. Same check for City Name.
    Get redirected here if a City Name is input
    :return html Template:
    """
    global destination_city
    if destination_city == "":
        flash("Please enter a city came first", "error")
        return redirect(url_for("views.home"))
    else:
        return render_template("got_city.html", destination_name= destination_city)

