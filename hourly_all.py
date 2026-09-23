from pydoc import cli
import csv, time, os, re
from datetime import datetime
import requests, pymongo, pandas as pd


messer = requests.get('https://buff.163.com/api/market/goods/buying?game=csgo&page_num=1&category_group=knife').json()

#https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=835861&page_num=1&_=1657808768032
eurtoyuan = requests.get('https://api.frankfurter.app/latest?amount=1&from=CNY&to=EUR').json()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["csgo"]
mycol = mydb["ALL_IDs"]

all_ids = pd.read_csv('C:/Users/Maurits/Desktop/GIT Project/csgohist/ids.csv', encoding= 'unicode_escape')
all_ids = all_ids.reset_index()

yuan = float(eurtoyuan['rates']['EUR'])
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for index, row in all_ids.iterrows():
        rowid = row['ID']
        rowname = row.values[2]
        mydict = {"ID" : rowid, "weapon" : rowname}
        x = mycol.insert_one(mydict)

        collist = mydb.list_collection_names()
        if str(row['ID']) not in collist:
            mydb.create_collection(str(rowid))
            myrow = mydb[str(rowid)]

            href = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=" + str(rowid)

            print(id, ": Wird überprüft")
            res= requests.get(href)
            while res.status_code == 429:
                print("429... Warte")
                time.sleep(10)
                res = requests.get(href)

            res = res.json()
            if not (res['data']['items'] == []):
                lowest = res['data']['items'][0]['price']
                lowesteur = round(float(lowest) * yuan, 2)

                content = {"Timestamp" : now, "preis" : lowest, "preis_eur": lowesteur}

                y = myrow.insert_one(content)



