import requests
from bs4 import BeautifulSoup
import psycopg2
import logging
import schedule
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuoteScraper:
    def __init__(self):
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.conn = self.get_db_connection()

    def get_db_connection(self):
        try:
            return psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            raise

    def create_table(self):
        try:
            cur = self.conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id SERIAL PRIMARY KEY,
                    quote TEXT,
                    author TEXT,
                    tags TEXT
                )
            ''')
            self.conn.commit()
            cur.close()
            logger.info('Table created or already exists')
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            raise

    def get_quotes_from_page(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')

            cur = self.conn.cursor()

            for quote in quotes:
                text = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
                cur.execute("INSERT INTO quotes (quote, author, tags) VALUES (%s, %s, %s)",
                             (text, author, ','.join(tags)))
                logger.info(f"Inserted quote: {text}")

            self.conn.commit()
            cur.close()
        except Exception as e:
            logger.error(f"Error scraping page {url}: {e}")
            raise

    def scrape_quotes(self):
        self.create_table()
        base_url = 'http://quotes.toscrape.com/page/'
        page = 1
        while True:
            url = base_url + str(page)
            try:
                response = requests.get(url)
                if "No quotes found!" in response.text:
                    break
                logger.info(f"Scraping page: {page}")
                self.get_quotes_from_page(url)
                page += 1
            except Exception as e:
                logger.error(f"Error with page {page}: {e}")
                break

    def run(self):
        schedule.every().day.at("00:00").do(self.scrape_quotes)
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    scraper = QuoteScraper()
    scraper.run()
