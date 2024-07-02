# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# from django.core.management.base import BaseCommand
# from riot_app.models import TeamRanking

# class Command(BaseCommand):
#     help = 'Crawl LCK team rankings and update the database'

#     def handle(self, *args, **kwargs):
#         self.crawl_rankings()

#     def crawl_rankings(self):
#         # Setup Chrome options
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")  # Ensure GUI is off
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")

#         # Set path to chromedriver as per your configuration
#         webdriver_service = Service('/usr/local/bin/chromedriver')  # Change this to your actual path

#         # Choose Chrome Browser
#         browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        
#         url = 'https://game.naver.com/esports/League_of_Legends/record/lck/team/lck_2024_summer'
#         browser.get(url)

#         try:
#             # Wait until the rankings table is loaded
#             WebDriverWait(browser, 40).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, 'record_list_item__2fFsp'))
#             )
            
#             # Get page source and parse with BeautifulSoup
#             page_source = browser.page_source
#             soup = BeautifulSoup(page_source, 'html.parser')
#             teams = soup.find_all('li', class_='record_list_item__2fFsp')
#             season = "2024 LCK 서머"

#             if not teams:
#                 self.stdout.write(self.style.ERROR('No teams found on the page.'))
#                 return

#             # Clear existing data
#             TeamRanking.objects.all().delete()

#             for team in teams:
#                 try:
#                     rank = team.find('span', class_='record_list_rank__3mn_o').text.strip()
#                     logo_style = team.find('span', class_='record_list_thumb_logo__1s1BT')['style']
#                     logo_url = logo_style.split('url("')[1].split('");')[0]
#                     team_name = team.find('span', class_='record_list_name__27huQ').text.strip()
#                     stats = team.find_all('span', class_='record_list_data__3wyY7')
#                     wins = stats[0].text.strip()
#                     losses = stats[1].text.strip()
#                     points = stats[2].text.strip()
#                     win_rate = stats[3].text.strip().replace('%', '')
#                     kda = stats[4].text.strip()
#                     kills = stats[5].text.strip()
#                     deaths = stats[6].text.strip()
#                     assists = stats[7].text.strip()

#                     # 디버깅 출력
#                     print(f"Rank: {rank}, Season: {season}, Logo URL: {logo_url}, Team Name: {team_name}, Wins: {wins}, Losses: {losses}, Points: {points}, Win Rate: {win_rate}, KDA: {kda}, Kills: {kills}, Deaths: {deaths}, Assists: {assists}")

#                     # Save data to database
#                     TeamRanking.objects.create(
#                         rank=int(rank),
#                         season=season,
#                         team_logo=logo_url,
#                         team_name=team_name,
#                         wins=int(wins),
#                         losses=int(losses),
#                         points=int(points),
#                         win_rate=float(win_rate),
#                         kda=float(kda),
#                         kills=int(kills),
#                         deaths=int(deaths),
#                         assists=int(assists)
#                     )
#                 except IndexError as e:
#                     self.stdout.write(self.style.ERROR(f'Error processing team data: list index out of range: {e}'))
#                 except AttributeError as e:
#                     self.stdout.write(self.style.ERROR(f'Error processing team data: attribute error: {e}'))

#             self.stdout.write(self.style.SUCCESS('Successfully updated rankings'))
        
#         finally:
#             browser.quit()
