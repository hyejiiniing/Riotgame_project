from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .utils import get_champion_rotation, get_champion_data, map_champion_id_to_name, parse_match_date, parse_match_time
from .models import Match
from itertools import groupby
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MatchSerializer
from rest_framework import viewsets
from model_champion.models import Champion, ChampionSkin
import logging
import os
from django.conf import settings
from django.utils import timezone
from .models import Player
from django.views import View
from django.core.management import call_command
from django.core.cache import cache

logger = logging.getLogger(__name__)

# 홈 화면 뷰
def home_view(request):
    # 챔피언 로테이션 데이터 가져오기
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
    else:
        champions = []

    # 경기 일정 데이터 가져오기
    current_date = timezone.now().date()
    all_matches = Match.objects.all()
    
    upcoming_matches = []
    for match in all_matches:
        match_date = parse_match_date(match.match_date)
        if match_date and match_date >= current_date:
            upcoming_matches.append(match)

    # 날짜순으로 정렬
    upcoming_matches = sorted(upcoming_matches, key=lambda x: parse_match_date(x.match_date))[:4]
    
    logger.debug(f"Current date: {current_date}")
    logger.debug(f"Upcoming matches: {upcoming_matches}")

    return render(request, 'riot_app/home.html', {
        'champions': champions,
        'upcoming_matches': upcoming_matches
    })

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
    passive_image = None
    skill_images = {'Q': None, 'W': None, 'E': None, 'R': None}
    skin_images = {}

    # 패시브 이미지 폴더 경로
    passive_image_dir = os.path.join(settings.BASE_DIR, 'static/assets/images/passive')

    # 패시브 이미지 파일 이름 찾기
    for filename in os.listdir(passive_image_dir):
        if filename.startswith(champion_id):
            passive_image = os.path.join('assets/images/passive', filename)
            break

    # 스킬 이미지 파일 이름 찾기
    spell_image_dir = os.path.join(settings.BASE_DIR, 'static/assets/images/spell')
    for spell_key in skill_images.keys():
        for filename in os.listdir(spell_image_dir):
            if filename.startswith(f"{champion_id}{spell_key}"):
                skill_images[spell_key] = os.path.join('assets/images/spell', filename)
                break

    # 스킨 이미지 파일 이름 찾기
    splash_image_dir = os.path.join(settings.BASE_DIR, 'static/assets/images/splash')
    skins = ChampionSkin.objects.filter(champion_id=champion_id)
    for skin in skins:
        for filename in os.listdir(splash_image_dir):
            if filename.startswith(f"{champion_id}_{skin.num}"):
                skin_images[skin.name] = os.path.join('assets/images/splash', filename)
                break

    context = {
        'champion': champion,
        'passive_image': passive_image,
        'skill_images': skill_images,
        'skin_images': skin_images,
    }
    return render(request, 'riot_app/champion_detail.html', context)

def player_list(request):
    players = Player.objects.all()
    return render(request, 'riot_app/player_list.html', {'players': players})

class HomeView(View):
    def get(self, request):
        # 캐시에서 크롤링 결과 가져옴
        latest_videos = cache.get('latest_videos')
        
        # 크롤링 결과가 없는 경우 처리
        if not latest_videos:
            latest_videos = []
        
        return render(request, 'riot_app/home.html', {'latest_videos': latest_videos})
    
# 로그인
# def login(request):
#     if request.method != 'POST':
#         return render(request, 'member/login.html')  # 로그인 폼 이동
#     else: 
#         member_id = request.POST['member_id']
#         member_password = request.POST['member_password']
        
#         try:
#             member = Member.objects.get(member_id=member_id)
#             if member.member_password == member_password:
#                 request.session['login_id'] = member.member_id  # 로그인 정보 session에 저장
#                 request.session['login_point'] = member.member_point
#                 request.session['login_grade'] = member.grade_name 
#                 return HttpResponseRedirect("/")  # 메인 페이지로 리디렉션 (로그인 상태)
#             else:
#                 context = {"msg": "비밀번호가 틀립니다.", "url": "../login/"}
#                 messages.error(request, '비밀번호가 틀렸습니다.')
#                 return render(request, 'member/login.html', context)
#         except Member.DoesNotExist:
#             messages.error(request, '아이디가 틀렸습니다.')
#             return render(request, 'member/login.html', {"errormsg": "아이디가 틀립니다."})


    
