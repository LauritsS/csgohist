from pydoc import cli
import csv, time, os, re
from datetime import datetime
import requests, pymongo


# Buff verlangt seit Ende Juli einen Login. Den Wert des "session"-Cookies aus dem
# eingeloggten Browser (buff.163.com -> F12 -> Application -> Cookies) in buff_session.txt
# neben diesem Skript speichern.
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'buff_session.txt')) as sf:
    buff_session = sf.read().strip()

buff = requests.Session()
buff.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"})
buff.cookies.set("session", buff_session, domain="buff.163.com")

#https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=835861&page_num=1&_=1657808768032
eurtoyuan = requests.get('https://api.frankfurter.app/latest?amount=1&from=CNY&to=EUR').json()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["csgo"]
mycol = mydb["csgohistory"]

collist = mydb.list_collection_names()
if "customers" in collist:
  print("The collection exists.")

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

temstatmw = {
    "id" : "921604",
    "wish" : "2300"
}

temstatfn = {
     "id" : "921460",
     "wish" : "4500"
}

wpcs1 = {
     "id" : "34273",
     "wish" : "430"
}

bp = {
     "id" : "835547",
     "wish" : "4300"
}

onibs = {
     "id" : "34107",
     "wish" : "1450"
}

vals = [fvs, m4, de, temfn, temstatmw,temstatfn, wpcs1, bp, onibs]
header = ["timestamp", "weapon", "preis", "preis_eur"]
yuan = float(eurtoyuan['rates']['EUR'])
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def preisabfrage(val):
        s = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=" + str(val["id"])
        # Buff drosselt stark ("System Error" / zu viele Anfragen) -> mit Wartezeit erneut versuchen
        for versuch in range(5):
            res= buff.get(s).json()
            if res.get('code') != 'System Error':
                break
            time.sleep(15 * (versuch + 1))
        if res.get('code') == 'Login Required':
            raise SystemExit("Buff: Login Required - Session-Cookie in buff_session.txt fehlt oder ist abgelaufen.")
        if res.get('code') != 'OK':
            raise SystemExit("Buff-Fehler bei goods_id " + str(val["id"]) + ": " + str(res.get('code')) + " - " + str(res.get('error')))
        if not res['data']['items']:
            print("Keine Angebote fuer goods_id " + str(val["id"]) + " - uebersprungen")
            return None
        name = res['data']['goods_infos'][val["id"]]['market_hash_name']
        lowest = res['data']['items'][0]['price']
        lowesteur = round(float(lowest) * yuan)
        return name, lowest, lowesteur
 
with open('C:/Users/Maurits/Desktop/GIT Project/csgohist/skinverlauf.csv', 'a', newline='') as f:       
    writer = csv.writer(f)
    #writer.writerow(header)
    for val in vals:
        line = preisabfrage(val)
        if line is None:
            continue
        processed_string = re.sub(r'\u2122', '', line[0])
        writer.writerow([datetime.now(), processed_string, str(line[1]), str(line[2])])
        mydict = {"timestamp" : now, "weapon" : processed_string, "preis": str(line[1]), "preis_eur":str(line[2]) }
        x = mycol.insert_one(mydict)
        time.sleep(5)