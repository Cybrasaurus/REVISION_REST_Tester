from flask import Blueprint, render_template, request, redirect, url_for, flash
import Functions as cy
import json
views = Blueprint("views", __name__)

destination_city = ""
destination_country = ""


@views.route("/", methods=["GET"])
def home():
    # default route
    return "Server Running"


@views.route("/json", methods=["GET"])
def get_json():

    if request.method == "GET":

        #load_commands = json.loads(request.args.get("excel_dict"))
        load_commands = {
            "File_Name": "Fruit Data",
            "File_Location": "raw_data",
            "Headers": "Excel_Headers"
        }
        print(f"load commands:{load_commands}")
        excel_data_DF = cy.File_Manipulation.load_excel(config_command=load_commands)
        excel_data_json = excel_data_DF.to_json(orient="records")
        print(excel_data_DF)
        return excel_data_json


@views.route("/json_dynamic", methods=["GET"])
def get_json_dynamic():

    if request.method == "GET":

        load_commands = json.loads(request.args.get("excel_dict"))
        print(f"load commands:{load_commands}")
        excel_data_DF = cy.File_Manipulation.load_excel(config_command=load_commands)
        excel_data_json = excel_data_DF.to_json(orient="records")
        print(excel_data_DF)
        return excel_data_json


@views.route("/xml", methods=["GET"])
def get_xml():

    if request.method == "GET":

        #load_commands = json.loads(request.args.get("excel_dict"))
        load_commands = {
            "File_Name": "Fruit Data",
            "File_Location": "raw_data",
            "Headers": "Excel_Headers"
        }
        print(f"load commands:{load_commands}")
        excel_data_DF = cy.File_Manipulation.load_excel(config_command=load_commands)
        excel_data_xml = excel_data_DF.to_xml()
        print(type(excel_data_xml))
        print(excel_data_DF)
        return excel_data_xml

@views.route("/xml_dynamic", methods=["GET"])
def get_xml_dynamic():

    if request.method == "GET":

        #load_commands = json.loads(request.args.get("excel_dict"))
        load_commands = {
            "File_Name": "Fruit Data",
            "File_Location": "raw_data",
            "Headers": "Excel_Headers"
        }
        print(f"load commands:{load_commands}")
        excel_data_DF = cy.File_Manipulation.load_excel(config_command=load_commands)
        excel_data_xml = excel_data_DF.to_xml()
        print(type(excel_data_xml))
        print(excel_data_DF)
        return excel_data_xml