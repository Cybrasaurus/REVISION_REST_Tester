
from flask import Blueprint, render_template, request

views = Blueprint("views", __name__)



@views.route("/") # this is the path where we gonna end up, so for now just host and then /
def home():
    return render_template("home.html")
    #this is the html template that gets used, is an extension of the base.html
    #the thing written between the brackets in blocktitle is what the page is called in the browser tab

@views.route("/weather")
def weather():
    return render_template("weather.html")

@views.route("/cur_rate")
def cur_rate():
    return render_template("currency_rate.html")

@views.route("/flights")
def flights():
    return render_template("flights.html")