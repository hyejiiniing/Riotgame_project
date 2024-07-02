from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .utils import get_champion_rotation, get_champion_data, map_champion_id_to_name
from .models import Match
from itertools import groupby
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MatchSerializer
from rest_framework import viewsets
from model_champion.models import Champion 
import logging

logger = logging.getLogger(__name__)

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

def match_list(request):
    # 기본 7월 데이터 필터링
    matches = Match.objects.filter(match_date__startswith='07').order_by('match_date', 'match_time')
    
    grouped_matches = []
    for date, group in groupby(matches, key=lambda x: x.match_date):
        grouped_matches.append({
            'date': date,
            'matches': list(group)
        })
    
    context = {
        'grouped_matches': grouped_matches,
        'selected_month': '07'
    }
    return render(request, 'riot_app/match_list.html', context)

@api_view(['GET'])
def match_list_api(request, month):
    matches = Match.objects.filter(match_date__startswith=month).order_by('match_date', 'match_time')
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def champion_list(request):
    champions = Champion.objects.all()
    champions_data = []
    for champion in champions:
        champion_name_url = champion.name.replace(" ", "").replace("'", "").replace(".", "").replace("&", "")
        image_url = f"http://ddragon.leagueoflegends.com/cdn/11.24.1/img/champion/{champion_name_url}.png"
        logger.info(f"Image URL for {champion.name}: {image_url}")
        champion_data = {
            'id': champion.id,
            'name': champion.name,
            'image': image_url
        }
        champions_data.append(champion_data)
    return render(request, 'riot_app/champion_list.html', {'champions': champions_data})

def champion_detail(request, champion_id):
    champion = get_object_or_404(Champion, id=champion_id)
    return render(request, 'riot_app/champion_detail.html', {'champion': champion})
