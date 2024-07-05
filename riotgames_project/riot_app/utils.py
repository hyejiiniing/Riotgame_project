import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import datetime
import re

# 로테이션 챔피언 목록 가져오기
def get_champion_rotation():
    api_key = os.getenv('RIOT_API_KEY')
    url = f"https://kr.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": {"status_code": response.status_code, "message": response.text}}

# 모든 챔피언 데이터 가져오기
def get_champion_data():
    url = "https://ddragon.leagueoflegends.com/cdn/11.24.1/data/en_US/champion.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 챔피언 ID를 이름으로 매핑
def map_champion_id_to_name(champion_data):
    id_to_name = {}
    for champ in champion_data['data'].values():
        id_to_name[int(champ['key'])] = champ['id']
    return id_to_name

def parse_match_date(date_str):
    # '08월 18일 (일)' 형식의 날짜 문자열을 datetime.date로 변환
    month_map = {
        '01': 1, '02': 2, '03': 3, '04': 4, '05': 5,
        '06': 6, '07': 7, '08': 8, '09': 9, '10': 10,
        '11': 11, '12': 12
    }
    match = re.match(r'(\d{2})월 (\d{2})일', date_str)
    if match:
        month = month_map[match.group(1)]
        day = int(match.group(2))
        year = datetime.datetime.now().year
        return datetime.date(year, month, day)
    return None

def parse_match_time(time_str):
    # 'HH:MM' 형식의 시간 문자열을 datetime.time으로 변환
    return datetime.datetime.strptime(time_str, '%H:%M').time()

# def get_lck_schedule():
#     url = 'https://lolesports.com/ko-KR/schedule?leagues=lck'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # 실제 HTML 구조에 맞게 데이터를 추출합니다.
#     schedule = []

#     matches = soup.find_all('div', class_='EventMatch')  # 실제 HTML 구조에 맞는 클래스 이름 사용
#     for match in matches:
#         # 날짜 정보 추출
#         date_str = match.find('span', class_='EventMatch__date--1mdGh').text.strip()  # 클래스 이름 확인 및 수정
#         match_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')  # 날짜 형식 확인 및 수정
#         teams = match.find_all('span', class_='EventMatch__team--1jGd5')  # 클래스 이름 확인 및 수정
#         team1 = teams[0].text.strip()
#         team2 = teams[1].text.strip()
#         schedule.append({'date': match_date, 'team1': team1, 'team2': team2})

#     # 다음 예정된 5개의 경기를 반환
#     return schedule[:5]

# # lck 순위
# def crawl_lck_rankings():
#     url = "https://game.naver.com/esports/League_of_Legends/record/lck/team/lck_2024_summer"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     rankings = []

#     teams = soup.select('div.record_list_item__2fFsp')
#     for team in teams:
#         team_logo_style = team.select_one('.record_list_thumb_logo__1s1BT')['style']
#         team_logo = team_logo_style.split('url("')[1].split('")')[0]
#         team_name = team.select_one('.record_list_name__27huQ').text
#         stats = team.select('.record_list_data__3wyY7')
#         wins = stats[0].text.strip()
#         losses = stats[1].text.strip()
#         points = stats[2].text.strip()
#         rank = team.select_one('.record_list_rank__3mn_o').text.strip()
#         win_rate = stats[3].text.strip()
#         kda = stats[4].text.strip()
#         kills = stats[5].text.strip()
#         deaths = stats[6].text.strip()
#         assists = stats[7].text.strip()

#         rankings.append({
#             'rank': int(rank),
#             'team_logo': team_logo,
#             'team_name': team_name,
#             'wins': int(wins),
#             'losses': int(losses),
#             'points': int(points),
#             'win_rate': float(win_rate),
#             'kda': float(kda),
#             'kills': int(kills),
#             'deaths': int(deaths),
#             'assists': int(assists),
#             'season': '2024 LCK 서머'
#         })
    
#     return rankings

# def update_rankings():
#     data = crawl_lck_rankings()
#     TeamRanking.objects.all().delete()
#     for team in data:
#         TeamRanking.objects.create(
#             rank=team['rank'],
#             team_logo=team['team_logo'],
#             team_name=team['team_name'],
#             wins=team['wins'],
#             losses=team['losses'],
#             points=team['points'],
#             win_rate=team['win_rate'],
#             kda=team['kda'],
#             kills=team['kills'],
#             deaths=team['deaths'],
#             assists=team['assists'],
#             season=team['season']
#         )