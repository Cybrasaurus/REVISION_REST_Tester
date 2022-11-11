import requests
import json
def request_func(url_route, parameter):

    base_url = "http://127.0.0.1:5000/"
    thisurl = f"{base_url}{url_route}"

    print(f"Request func parameter: {parameter}")

    return_statement = requests.request("GET", thisurl, params=parameter)

    if url_route == "json":
        print("Return Data: " + str(return_statement.json()))
        print(f"Type of Return: {type(return_statement.json())}")
    elif url_route == "xml":
        print("Return Data: " + str(return_statement.content))
        print(f"Type of Return: {type(return_statement.content)}")




if __name__ == "__main__":

    load_commands = {
        "File_Name": "Fruit Data",
        "File_Location": "raw_data",
        "Headers": "Excel_Headers"
    }
    request_func(url_route="xml", parameter={"excel_dict": json.dumps(load_commands)})