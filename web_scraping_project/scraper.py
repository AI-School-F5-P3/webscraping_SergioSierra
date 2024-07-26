import os
import sys
import requests
from bs4 import BeautifulSoup
import logging
from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Añadir el directorio del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar el modelo después de agregar el directorio al PYTHONPATH
from web_scraping_project.models import Quote, Base

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
try:
    fileConfig(os.path.join(os.path.dirname(__file__), 'logging.conf'), disable_existing_loggers=False)
except FileNotFoundError:
    print("El archivo de configuración de logging 'logging.conf' no se encuentra.")
except Exception as e:
    print(f"Error al configurar el logging: {e}")

# Obtener el logger específico después de configurar el logging
logger = logging.getLogger('webscraper')

class QuoteScraper:
    def __init__(self):
        logger.info("Inicializando el scraper de citas.")
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        logger.debug(f"URL de la base de datos: {db_url}")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Conexión a la base de datos establecida y tablas creadas (si no existían).")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_page(self, url):
        logger.info(f"Intentando obtener la página: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Página obtenida exitosamente: {url}")
        return response.text

    def parse_quote(self, quote_div):
        text = quote_div.find('span', class_='text').get_text(strip=True)
        author = quote_div.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_div.find_all('a', class_='tag')]
        logger.debug(f"Quote parsed: texto={text}, autor={author}, etiquetas={tags}")
        return Quote(quote=text, author=author, tags=','.join(tags))

    def get_quotes_from_page(self, url):
        try:
            html = self.get_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            logger.info(f"{len(quotes)} citas encontradas en la página: {url}")

            with self.Session() as session:
                for quote_div in quotes:
                    new_quote = self.parse_quote(quote_div)
                    session.add(new_quote)
                    logger.info(f"Cita insertada: {new_quote.quote[:30]}...")
                session.commit()
                logger.info("Transacción completada y cambios guardados en la base de datos.")
        except requests.RequestException as e:
            logger.error(f"Error al obtener la página {url}: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos al procesar la página {url}: {e}")
        except Exception as e:
            logger.error(f"Error inesperado al analizar la página {url}: {e}")

    def scrape_quotes(self):
        base_url = 'http://quotes.toscrape.com/page/'
        page = 1
        logger.info("Inicio del proceso de scraping de citas.")
        while True:
            url = base_url + str(page)
            try:
                html = self.get_page(url)
                if "No quotes found!" in html:
                    logger.info("No se encontraron más citas. Proceso de scraping completado.")
                    break
                logger.info(f"Analizando la página: {page}")
                self.get_quotes_from_page(url)
                page += 1
            except Exception as e:
                logger.error(f"Error en la página {page}: {e}")
                break

if __name__ == "__main__":
    scraper = QuoteScraper()
    scraper.scrape_quotes()
