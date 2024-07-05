import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.core.management.base import BaseCommand
from riot_app.models import Player

class Command(BaseCommand):
    help = 'Crawl all teams and their player data and save to database'

    def handle(self, *args, **kwargs):
        # 크롬드라이버 설정
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # GUI 없이 실행
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service, options=options)

        team_urls = [
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R1040', # T1
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R479', # Gen.G
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R105', # KT
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R1152', # DK
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R480', # Hanwha
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R1070', # BNK
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R1118', # KDF
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R1071', # OK Savings
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R1041', # DRX
            'https://game.naver.com/esports/League_of_Legends/stoveleague/null?type=roster&teamId=R1072'  # NS RedForce
        ]

        # 팀 ID와 이름 매핑
        team_names = {
            'R1040': 'T1',
            'R479': 'Gen.G',
            'R105': 'KT',
            'R1152': 'DK',
            'R480': 'Hanwha',
            'R1070': 'BNK',
            'R1118': 'KDF',
            'R1071': 'OK Savings',
            'R1041': 'DRX',
            'R1072': 'NS RedForce'
        }

        # Explicit wait 설정
        wait = WebDriverWait(driver, 20)

        for team_url in team_urls:
            team_id = team_url.split('teamId=')[-1]
            team_name = team_names.get(team_id, 'Unknown')

            driver.get(team_url)
            time.sleep(5)  # 페이지 로딩 대기

            try:
                team_logo_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.filter_logo__3XxOU')))
                team_logo = team_logo_element.get_attribute('src')
                self.stdout.write(f'DEBUG: Team Logo: {team_logo}')

                self.stdout.write(f'DEBUG: Team Name: {team_name}')

                # 로스터 테이블 찾기
                roster_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.roster_table__3El2v')))
                rows = roster_table.find_elements(By.CSS_SELECTOR, 'tbody tr')
                self.stdout.write(f'DEBUG: Number of rows found: {len(rows)}')

                # 포지션 이름들을 각 열의 헤더에서 찾기
                headers = roster_table.find_elements(By.CSS_SELECTOR, 'thead th')
                position_names = [header.find_element(By.CSS_SELECTOR, 'span.roster_position__aG0p8').text for header in headers]
                self.stdout.write(f'DEBUG: Position Names: {position_names}')

                for row in rows:
                    columns = row.find_elements(By.CSS_SELECTOR, 'td')
                    for position_name, col in zip(position_names, columns):
                        players = col.find_elements(By.CSS_SELECTOR, 'li.roster_item__2Fksn')
                        for player in players:
                            try:
                                player_photo_element = player.find_element(By.CSS_SELECTOR, 'div.roster_thumbnail__2Y8cc')
                                player_photo = player_photo_element.get_attribute('style').split('"')[1]
                                self.stdout.write(f'DEBUG: Player Photo: {player_photo}')
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'Error finding player photo: {e}'))
                                continue
                            
                            try:
                                player_name_element = player.find_element(By.CSS_SELECTOR, 'strong.roster_nickname__3c3iB')
                                player_name = player_name_element.text
                                self.stdout.write(f'DEBUG: Player Name: {player_name}')
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'Error finding player name: {e}'))
                                continue

                            # 데이터 저장
                            try:
                                Player.objects.create(
                                    team_logo=team_logo,
                                    team_name=team_name,
                                    position_name=position_name,
                                    player_photo=player_photo,
                                    player_name=player_name
                                )
                                self.stdout.write(self.style.SUCCESS(f'Successfully saved player: {player_name}'))
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'Error saving player data: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error during crawling team: {e}'))
                # 스크린샷 저장
                screenshot_path = os.path.join(os.path.expanduser("~"), f'error_screenshot_{team_name}.png')
                driver.save_screenshot(screenshot_path)
                self.stdout.write(self.style.ERROR(f'Screenshot saved to: {screenshot_path}'))

        driver.quit()
        self.stdout.write(self.style.SUCCESS('Successfully crawled and saved player data for all teams'))
