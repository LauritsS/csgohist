import requests
from bs4 import BeautifulSoup
import time, csv

def search_item(id):
    url = "https://buff.163.com/goods/{}?from=market#tab=selling".format(id)
    response = requests.get(url)

    while response.status_code == 429:
         print("429... Warte")
         time.sleep(5)
         response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    
    try:

        if soup.find("div", {"class" : "nodata"}):
            return

        div = soup.find("div", {"class": "detail-summ"})
        hrefs = div.findAll('a', href=True)

        name = soup.find("div", {"class": "detail-cont"}).find('h1').get_text()

        checkcs = soup.find("body", {"class": "csgo"})
        
        return hrefs[2].get('href'), name, checkcs
    
    except ValueError:
            print("Null value error")
    
def check_csgo(href, id):
    b = False
    print(id, ": Wird überprüft")
    response = requests.get(href)
    while response.status_code == 429:
         print("429... Warte")
         time.sleep(15)
         response = requests.get(href)
    soup = BeautifulSoup(response.text, "html.parser")

    game = soup.find("div", {"class": "market_listing_nav"}).find('a', href=True).get_text()

    if("Counter-Strike: Global Offensive" in game):
            b = True

    return b
# Beispielaufruf

def namenabfrage(id):
        s = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=" + str(id)
        res= requests.get(s).json()
        name = ""

        if not (res['data']['items'] == []):
            name = res['data']['goods_infos'][str(id)]['market_hash_name']
        
        return name
        

with open('C:/Users/Maurits/Desktop/GIT Project/csgohist/ids.csv', 'a', newline='', encoding='utf-8') as f:   
    for id in range(195945,1000000): #33686 macht Probleme, da keine Angebote
        writer = csv.writer(f)
        link = search_item(id)
        print(id, ": Wird überprüft")
        if(link is not None):
            if (link[2] is not None):
                name = namenabfrage(id)
                if name is "": 
                     name = link[1]
                print(str(id), ": ",str(name))
                writer.writerow([str(id), str(name)])