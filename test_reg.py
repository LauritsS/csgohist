from pydoc import cli
import csv, time, os, re
from datetime import datetime
import requests, json, schedule, time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Maurits",
  password="test",
  database="csgohistory",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()


messer = requests.get('https://buff.163.com/api/market/goods/buying?game=csgo&page_num=1&category_group=knife').json()
#https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=835861&page_num=1&_=1657808768032
eurtoyuan = requests.get('https://api.frankfurter.app/latest?amount=1&from=CNY&to=EUR').json()

ids = ['835861','781677','38568']

fvs = {
    "id" : "38568",
    "wish" : "600"
}

m4 = {
    "id" : "835861",
    "wish" : "2150"
}


de = {
    "id" : "781677",
    "wish" : "645"
}

temfn = {
    "id" : "921562",
    "wish" : "3500"
}

temstat = {
    "id" : "921604",
    "wish" : "2300"
}

vals = [fvs, m4, de, temfn, temstat]
header = ["timestamp", "weapon", "preis", "preis_eur"]
yuan = float(eurtoyuan['rates']['EUR'])


def preisabfrage(val):
        s = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=" + str(val["id"])
        res= requests.get(s).json()
        name = res['data']['goods_infos'][val["id"]]['market_hash_name']
        lowest = res['data']['items'][0]['price']
        lowesteur = round(float(lowest) * yuan)
        return name, lowest, lowesteur
 

    
for val in vals:
    line = preisabfrage(val)
    skin = re.findall("\| (.*) \(", line[0])[0]
    print(skin)
    condition = re.findall("\((.*)\)",line[0])[0]
    print(condition)
    waffe = re.findall("(.*) \|", line[0])[0]
    stat = False
    if "StatTrak" in waffe:
          waffe = waffe.split(' ', 1)[1]
          stat = True
    print("statTrak: ", stat)
    print(waffe)
    

