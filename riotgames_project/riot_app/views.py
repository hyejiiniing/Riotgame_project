from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_champion_rotation, get_champion_data, map_champion_id_to_name

# 홈 화면 뷰
def home_view(request):
    rotation_data = get_champion_rotation()
    champion_data = get_champion_data()
    if rotation_data and champion_data:
        id_to_name = map_champion_id_to_name(champion_data)
        champions = []
        for champion_id in rotation_data['freeChampionIds']:
            champion_name = id_to_name.get(champion_id)
            if champion_name:
                champions.append({
                    'name': champion_name,
                    'image': f"http://ddragon.leagueoflegends.com/cdn/11.24.1/img/champion/{champion_name}.png"
                })
        return render(request, 'riot_app/home.html', {'champions': champions})
    return render(request, 'riot_app/home.html', {'champions': []})
