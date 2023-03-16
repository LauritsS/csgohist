import requests

def get_buff_ids():
    url = 'https://buff.163.com/api/market/goods?game=csgo&game_type=k1010&sort_by=price.asc&page_num=1&sort_order=asc'
    response = requests.get(url)
    response_json = response.json()
    if response_json is not None and 'data' in response_json:
        buff_ids = {item['itemid']: item['name'] for item in response_json['data']['items']}
        return buff_ids
    else:
        print("Fehler: Ungültige Antwort vom Server.")
        return None

# Ausgabe der IDs und Namen
buff_ids = get_buff_ids()
if buff_ids is not None:
    for id, name in buff_ids.items():
        print(f"ID: {id}, Name: {name}")
else:
    print("Fehler: Keine IDs gefunden.")