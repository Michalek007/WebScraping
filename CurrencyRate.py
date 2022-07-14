import pandas as pd
import requests
import time
import json
from bs4 import BeautifulSoup

file = 'C:\\Users\\Public\\currency.json'
url = "https://e-kursy-walut.pl/"
listOfValues = []
listOfCurrency = []
currencyRate = {}


def GetValue(str):
    value = ""
    x = False
    z = 0
    for i in range(len(str)):
        if str[i] == '\"':
            x = not x
            z += 1
        elif x and z > 2:
            value += str[i]
        else:
            pass
        if z == 4:
            break
    return value


request_response = requests.get(url)
request_data = request_response.text
soup = BeautifulSoup(request_data, "html.parser")
for item in soup.find_all("td", {"class": "price"}):
    static = item.find("strong")
    # print(GetValue(str(item)))
    listOfValues.append(GetValue(str(item)))
for item in soup.find_all("td", {"class": "img"}):
    # print(GetValue(str(item)))
    listOfCurrency.append(GetValue(str(item)))
for i in range(len(listOfValues)):
    currencyRate[listOfCurrency[i]] = [listOfValues[i]]

try:
    with open(file, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
except (FileExistsError, FileNotFoundError, PermissionError):
    data = None
finally:
    pass

if data is not None:
    for i in range(len(listOfValues)):
        for j in range(len(data[listOfCurrency[0]])):
            currencyRate[listOfCurrency[i]].append(data[listOfCurrency[i]][j])
with open(file, 'w', encoding='utf-8') as write_file:
    json.dump(currencyRate, write_file)

columns = []
for i in range(len(currencyRate[listOfCurrency[0]])):
    columns.append("value" + " " + str(i))

save = pd.DataFrame.from_dict(currencyRate, orient="index", columns=columns)
save.to_csv("currency.csv")
