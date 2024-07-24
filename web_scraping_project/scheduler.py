import schedule
import time
from web_scraping_project.scraper import QuoteScraper

def job():
    scraper = QuoteScraper()
    scraper.scrape_quotes()

schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  # Espera un minuto antes de verificar nuevamente
