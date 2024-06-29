import requests

API_KEY = 'RGAPI-d3f39a74-e89d-4a68-a18e-6abeedc175c9'

def get_summoner_data(summoner_name):
    url = f'https://REGION.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={RGAPI-d3f39a74-e89d-4a68-a18e-6abeedc175c9}'
    response = requests.get(url)
    return response.json()
