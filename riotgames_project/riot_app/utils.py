import requests
import os

def get_champion_rotation():
    api_key = os.getenv('RIOT_API_KEY')
    url = f"https://kr.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": {"status_code": response.status_code, "message": response.text}}

def get_champion_data():
    url = "https://ddragon.leagueoflegends.com/cdn/11.24.1/data/en_US/champion.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def map_champion_id_to_name(champion_data):
    id_to_name = {}
    for champ in champion_data['data'].values():
        id_to_name[int(champ['key'])] = champ['id']
    return id_to_name
