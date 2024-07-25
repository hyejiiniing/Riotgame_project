import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Scrape the latest videos from the LCK YouTube channel'

    def handle(self, *args, **kwargs):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get('https://www.youtube.com/@LCK/videos')
            wait = WebDriverWait(driver, 10)
            videos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-grid-video-renderer')))
            
            latest_videos = []
            for video in videos[:4]:
                try:
                    title_element = video.find_element(By.CSS_SELECTOR, '#video-title')
                    title = title_element.get_attribute('title')
                    url = title_element.get_attribute('href')
                    thumbnail_element = video.find_element(By.CSS_SELECTOR, 'img')
                    thumbnail_url = thumbnail_element.get_attribute('src')
                    latest_videos.append({
                        'title': title,
                        'url': url,
                        'thumbnail_url': thumbnail_url,
                    })
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error extracting video info: {e}'))
            
            # 캐시에 저장
            cache.set('latest_videos', latest_videos, timeout=60*60)  # 1시간 동안 캐시 유지

            self.stdout.write(self.style.SUCCESS('Successfully scraped latest videos'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error scraping videos: {e}'))
        finally:
            driver.quit()
