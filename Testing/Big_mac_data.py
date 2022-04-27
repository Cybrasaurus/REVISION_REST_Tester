import pandas as pd

from API_Calls import Currency_api_data_to_df as apic


def generate_raw_data():
    #TODO clean up and split up into reading and processing
    mac_df = pd.read_csv("big-mac-source-data.csv")

    #print(mac_df)
    mac_df_22 = mac_df.loc[mac_df["date"] == "2022-01-01"]
    #print(mac_df_22)

    records = list(mac_df_22.to_records())

    #print(records)
    #print(type(records))
    data_list_dict = []
    for items in records:
        data_dict = {
            "Country Name" : "",
            "Local Big Mac Price": "",
            "Dollar Exchange Rate": "",
        }
        workingitem = str(items)
        workingitem = workingitem.split(",")

        for elements in workingitem:
            elements = elements.replace(",", "").replace("(", "").replace("'", "")
        data_dict["Country Name"] = workingitem[1].replace("'","")[1:]
        data_dict["Local Big Mac Price"] = float(workingitem[4])
        data_dict["Dollar Exchange Rate"] = float(workingitem[5])

        #print(type(data_dict["Dollar Exchange Rate"]))

        print(data_dict)
        data_list_dict.append(data_dict)
    print("done for loop")
    #print(records[0])

    apic.saver("Big_Mac_Data", data_list_dict)

def conversions(datalist):
    #print(datalist[0])
    #print(datalist[0]["Dollar Exchange Rate"])


    #todo dynamic update from currency api call
    #eur_to_dollar = 1.0859
    eur_to_dollar = 1.121

    for items in datalist:
        items["Value in EUR"] = round(items["Dollar Exchange Rate"] * eur_to_dollar, 5)


        bic_mac_price_in_eur = round(items["Local Big Mac Price"] / items["Value in EUR"], 5)
        items["Local Big Mac Price in Euro"] = bic_mac_price_in_eur

        print(items)

    pass
    print(datalist)

    return datalist

def percentage_ger_big_mac(datalist):
    #TODO grab german big mac price

    ger_big_mac = 4.46

    for items in datalist:
        items["Relative Cost for BigMac to Germany"] = round(items["Local Big Mac Price in Euro"] / ger_big_mac, 2)

    return datalist


def stats_and_numbers(datalist):
    my_df = pd.DataFrame.from_records(datalist)
    print(my_df)

    mean_cost = my_df["Relative Cost for BigMac to Germany"].mean()
    print(mean_cost)

    min_cost = my_df["Relative Cost for BigMac to Germany"].min()
    max_cost = my_df["Relative Cost for BigMac to Germany"].max()
    print(min_cost)
    print(max_cost)

if __name__ == "__main__":
    datalist = apic.opener("Big_mac_data_modified")
    #datalist = conversions(datalist=datalist)
    #datalist = percentage_ger_big_mac(datalist=datalist)

    #apic.saver("Big_mac_data_modified", datalist)
    stats_and_numbers(datalist=datalist)
    #generate_raw_data()

#TODO Dollar Exchange Rate: 1 Dollar is worth this much local currency
#TODO Value in EUR: 1 Eur is worth this much local currency