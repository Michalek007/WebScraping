import pandas as pd
import requests
import time
import json
from bs4 import BeautifulSoup
from datetime import date

file = 'C:\\Users\\Public\\currency.json'
dateFile = 'C:\\Users\\Public\\date.json'
url = "https://e-kursy-walut.pl/"
listOfValues = []
listOfCurrency = []
currencyRate = {}
today = date.today()

def get_value(str):
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
    listOfValues.append(get_value(str(item)))
for item in soup.find_all("td", {"class": "img"}):
    # print(GetValue(str(item)))
    listOfCurrency.append(get_value(str(item)))
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

try:
    with open(dateFile, 'r', encoding='utf-8') as read_file:
        dateList = json.load(read_file)
except (FileExistsError, FileNotFoundError, PermissionError):
    dateList = None
finally:
    pass
if dateList is not None:
    dateList.append(str(today))
else:
    dateList = [str(today)]
with open(dateFile, 'w', encoding='utf-8') as write_file:
    json.dump(dateList, write_file)

save = pd.DataFrame.from_dict(currencyRate, orient="index", columns=dateList)
save.to_csv("currency.csv")

growthRate = {}
if len(currencyRate[listOfCurrency[0]]) > 1:
    for i in range(len(currencyRate)):
        growthRate[listOfCurrency[i]] = []
        for j in range(len(currencyRate[listOfCurrency[0]])-1):
            growthRateValue = float(currencyRate[listOfCurrency[i]][j+1])/float(currencyRate[listOfCurrency[i]][j])
            growthRate[listOfCurrency[i]].append(growthRateValue*100-100)

dateList.pop(0)
saveG = pd.DataFrame.from_dict(growthRate, orient="index", columns=dateList)
saveG.to_csv("growthRate.csv")