from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_champion_rotation, get_champion_data, map_champion_id_to_name

def champion_rotation_view(request):
    data = get_champion_rotation()
    champion_data = get_champion_data()
    if not champion_data:
        return HttpResponse("Error fetching champion data.", status=500)
    
    id_to_name = map_champion_id_to_name(champion_data)
    
    if 'status' in data and data['status']['status_code'] != 200:
        return HttpResponse(f"Error fetching data: {data['status']['message']}", status=data['status']['status_code'])
    
    champions = []
    for champ_id in data['freeChampionIds']:
        name = id_to_name.get(champ_id, "Unknown")
        champions.append({
            'id': champ_id,
            'name': name,
            'image': f"http://ddragon.leagueoflegends.com/cdn/11.24.1/img/champion/{name}.png"
        })
    
    return render(request, 'riot_app/champion_rotation.html', {'champions': champions})

def home_view(request):
    return render(request, 'riot_app/home.html')
