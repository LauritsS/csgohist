from pydoc import cli
import csv, time, os, re
from datetime import datetime
import requests, pymongo


messer = requests.get('https://buff.163.com/api/market/goods/buying?game=csgo&page_num=1&category_group=knife').json()

#https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=835861&page_num=1&_=1657808768032
eurtoyuan = requests.get('https://api.frankfurter.app/latest?amount=1&from=CNY&to=EUR').json()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["csgo"]
mycol = mydb["IDs"]

collist = mydb.list_collection_names()
if "customers" in collist:
  print("The collection exists.")

yuan = float(eurtoyuan['rates']['EUR'])
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def preisabfrage(val):
        s = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=" + str(val["id"])
        res= requests.get(s).json()
        name = res['data']['goods_infos'][val["id"]]['market_hash_name']
        lowest = res['data']['items'][0]['price']
        lowesteur = round(float(lowest) * yuan)
        return name, lowest, lowesteur
 
with open('C:/Users/Maurits/Desktop/GIT Project/csgohist/skinverlauf.csv', 'a', newline='') as f:       
    writer = csv.writer(f)
    #writer.writerow(header)
    for val in vals:
        line = preisabfrage(val)
        processed_string = re.sub(r'\u2122', '', line[0])
        writer.writerow([datetime.now(), processed_string, str(line[1]), str(line[2])])
        mydict = {"timestamp" : now, "weapon" : processed_string, "preis": str(line[1]), "preis_eur":str(line[2]) }
        x = mycol.insert_one(mydict)