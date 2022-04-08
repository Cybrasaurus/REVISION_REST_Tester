
from flask import Blueprint, render_template, request, redirect, url_for, flash
from API_Calls import get_data_from_name

views = Blueprint("views", __name__)

destination_city=""



@views.route("/", methods=["GET", "POST"])
def home():
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
    global destination_city

    if destination_city == "":
        flash("Please enter a city came first", "error")
        return redirect(url_for("views.home"))
    else:
        returnlist = get_data_from_name(destination_city)
        w_main=returnlist[0]
        w_desc = returnlist[1]
        w_temp = returnlist[2]
        return render_template("weather.html", destination_name=destination_city, weather_main=w_main, weather_desc=w_desc, weather_temp=w_temp)

@views.route("/cur_rate")
def cur_rate():
    return render_template("currency_rate.html")

@views.route("/flights")
def flights():
    return render_template("flights.html")

@views.route("/got_city")
def got_city():
    global destination_city
    if destination_city == "":
        flash("Please enter a city came first", "error")
        return redirect(url_for("views.home"))
    else:
        return render_template("got_city.html", destination_name= destination_city)

