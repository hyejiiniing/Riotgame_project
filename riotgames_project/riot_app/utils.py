import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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


def get_lck_schedule():
    url = 'https://lolesports.com/ko-KR/schedule?leagues=lck'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 실제 HTML 구조에 맞게 데이터를 추출합니다.
    schedule = []

    matches = soup.find_all('div', class_='EventMatch')  # 실제 HTML 구조에 맞는 클래스 이름 사용
    for match in matches:
        # 날짜 정보 추출
        date_str = match.find('span', class_='EventMatch__date--1mdGh').text.strip()  # 클래스 이름 확인 및 수정
        match_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')  # 날짜 형식 확인 및 수정
        teams = match.find_all('span', class_='EventMatch__team--1jGd5')  # 클래스 이름 확인 및 수정
        team1 = teams[0].text.strip()
        team2 = teams[1].text.strip()
        schedule.append({'date': match_date, 'team1': team1, 'team2': team2})

    # 다음 예정된 5개의 경기를 반환
    return schedule[:5]
