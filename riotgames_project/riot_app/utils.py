from django.conf import settings
import requests

API_KEY = settings.RIOT_API_KEY

def get_summoner_data(summoner_name):
    url = f'https://REGION.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}'
    response = requests.get(url)
    return response.json()
