import os
import requests
from bs4 import BeautifulSoup
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import Quote, Base
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuoteScraper:
    def __init__(self):
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_page(self, url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_quote(self, quote_div):
        text = quote_div.find('span', class_='text').get_text(strip=True)
        author = quote_div.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_div.find_all('a', class_='tag')]
        return Quote(quote=text, author=author, tags=','.join(tags))

    def get_quotes_from_page(self, url):
        try:
            html = self.get_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            quotes = soup.find_all('div', class_='quote')

            with self.Session() as session:
                for quote_div in quotes:
                    new_quote = self.parse_quote(quote_div)
                    session.add(new_quote)
                    logger.info(f"Inserted quote: {new_quote.quote[:30]}...")
                session.commit()
        except requests.RequestException as e:
            logger.error(f"Error fetching page {url}: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Database error while processing page {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error scraping page {url}: {e}")

    def scrape_quotes(self):
        base_url = 'http://quotes.toscrape.com/page/'
        page = 1
        while True:
            url = base_url + str(page)
            try:
                html = self.get_page(url)
                if "No quotes found!" in html:
                    logger.info("No more quotes found. Scraping complete.")
                    break
                logger.info(f"Scraping page: {page}")
                self.get_quotes_from_page(url)
                page += 1
            except Exception as e:
                logger.error(f"Error with page {page}: {e}")
                break

if __name__ == "__main__":
    scraper = QuoteScraper()
    scraper.scrape_quotes()