import requests
from bs4 import BeautifulSoup
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Quote, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuoteScraper:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_quotes_from_page(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')

            session = self.Session()
            for quote in quotes:
                text = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
                new_quote = Quote(quote=text, author=author, tags=','.join(tags))
                session.add(new_quote)
                logger.info(f"Inserted quote: {text}")

            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Error scraping page {url}: {e}")
            raise

    def scrape_quotes(self):
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
