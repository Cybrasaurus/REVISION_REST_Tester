from Currency_api_data_to_df import saver
import copy

def openener_wierd(filename):
    outfile = open(filename, "r")
    outfile = list(outfile)
    return outfile



def converter():
    mydata = openener_wierd("raw_iata.txt")

    print(type(mydata))
    # print(mydata[0])
    mydata = str(mydata)
    my_list = mydata.split("}, {")

    print(my_list)

    print("----")

    filtered_list = []
    for items in my_list:
        items = items.replace("[", "").replace("'", "").replace("{", "").replace("]", "").replace("}", "")
        filtered_list.append(items)

    print(my_list[0])
    print(filtered_list[-1])

    Dict_of_Dicts = {}
    for items in filtered_list:
        temp_dict = {
            "Airport Name": "",
            "City": "",
            "Country": "",
            "IATA": "",
        }

        one_dict = items.split(", ")
        # print(one_dict)
        # print(len(one_dict))

        temp_dict["Airport Name"] = one_dict[0].split(": ")[1].replace('"', "")
        temp_dict["City"] = one_dict[1].split(": ")[1].replace('"', "")
        temp_dict["Country"] = one_dict[2].split(": ")[1].replace('"', "")
        temp_dict["IATA"] = one_dict[3].split(": ")[1].replace('"', "").replace("\\\\\\\\N", "None in Database")

        # print(temp_dict)

        Dict_of_Dicts[temp_dict["City"]] = temp_dict

    return Dict_of_Dicts

def converter_v2():
    mydata = openener_wierd("raw_iata.txt")
    mydata = str(mydata)
    my_list = mydata.split("}, {")

    #print(my_list)

    #print("----")

    filtered_list = []
    for items in my_list:
        items = items.replace("[", "").replace("'", "").replace("{", "").replace("]", "").replace("}", "")
        filtered_list.append(items)

    countrylist = []
    country_dict = {}
    country_dict_2 = {}
    country_dict_3 = {}

    #make list of all countries
    for items in filtered_list:
        item_split = items.split(", ")
        countrylist.append(item_split[2].replace('"country": ', "").replace('"', ""))
    #remove duplicates from list
    countrylist = list(set(countrylist))
    #sort alphabetically
    countrylist = sorted(countrylist)

    #start building datastructute, make Dictionary with Keys being the Countries
    for items in countrylist:
        country_dict[items] = ""
    country_dict_2 = copy.deepcopy(country_dict)
    country_dict_3 = copy.deepcopy(country_dict)
    #print(countrylist)

    #add all cities/airports of the raw data to the according country, no formatting
    for keys in country_dict:
        cities_list = []
        for items in filtered_list:
            item_split = items.split(", ")
            if item_split[2].replace('"country": ', "").replace('"', "") == keys:
                cities_list.append(items)
        country_dict[keys] = cities_list


    #generate Dict (Key: Country) of Lists (all cities) of dicts (city info)
    for keys in country_dict:
        cities_list_2 = []
        for items in country_dict[keys]:
            #print(items)
            item_split = items.split(", ")
            element_dict = {}
            for elements in item_split:
                elements = elements.replace('"', "")

                temp_list = elements.split(": ")
                #clean up empty space that sometimes at the end of a city
                #temp_element = temp_list[1]

                #print(temp_element)
                #if temp_element[-1] == " ":
                #    temp_element = temp_element[:-1]
                #temp_list[1] = temp_element
                #if temp_list[1][-1] == " ":
                #    temp_list[1][-1] = temp_list[1][-1].replace(" ", "")
                element_dict[temp_list[0]] = temp_list[1]
                #print(temp_list[1][-1])
                #print(elements)
            cities_list_2.append(element_dict)

        country_dict[keys] = cities_list_2

    #sorted Dict (key: country) of Lists, lists contain each City name
    for keys in country_dict:
        #print(keys)
        list_of_country_cities = []
        for dicts in country_dict[keys]:
            #print(dicts["name"])
            substring = "\\\\"
            if substring in dicts["city"]:
                pass
            else:
                list_of_country_cities.append(dicts["city"])
        list_of_country_cities = list(set(list_of_country_cities))
        list_of_country_cities = sorted(list_of_country_cities)
        country_dict_2[keys] = list_of_country_cities
        #print(list_of_country_cities)

            #pass

    #build dict (key: Country) of Dicts (keys: Cities)
    for keys in country_dict_3:
        temp_dict = {}
        country_dict_3[keys] = temp_dict
        for items in country_dict_2[keys]:

            country_dict_3[keys][items] = ""
            #print(items)

    for countries in country_dict_3:
        for cities in country_dict_3[countries]:
            #print(cities)
            IATA_Code_List_for_city = []
            for items in country_dict[countries]:
                #print(items)
                if items["city"] == cities:
                    substring = "\\\\"
                    if substring in items["IATA"]:
                        pass
                    else:
                        IATA_Code_List_for_city.append(items["IATA"])
            print(IATA_Code_List_for_city)
            country_dict_3[countries][cities] = IATA_Code_List_for_city

    saver(filename="Cleaned_IATA_V2", file_content=country_dict)
    saver(filename="List_of_country_city", file_content=country_dict_2)
    saver(filename="Cleaned_IATA_V3", file_content=country_dict_3)

if __name__ == "__main__":
    #data = converter()
    #saver("iata2", data)
    converter_v2()