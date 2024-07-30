import schedule
import time
import logging
import logging.config
from web_scraping_project.scraper import QuoteScraper  

# Cargar la configuración de logging desde logging.conf
try:
    logging.config.fileConfig('web_scraping_project/logging.conf', disable_existing_loggers=False)
except FileNotFoundError:
    print("El archivo de configuración de logging 'logging.conf' no se encuentra.")
except Exception as e:
    print(f"Error al configurar el logging: {e}")

# Obtener el logger específico
logger = logging.getLogger('scheduler')

def job():
    logger.info("Inicio del trabajo de scraping.")
    try:
        scraper = QuoteScraper()
        scraper.scrape_quotes()
        logger.info("Trabajo de scraping completado exitosamente.")
    except Exception as e:
        logger.error(f"Error durante el trabajo de scraping: {e}")

# Programar el trabajo para que se ejecute todos los días a medianoche
schedule.every().day.at("00:00").do(job)
logger.info("Trabajo de scraping programado para ejecutarse todos los días a medianoche.")

logger.info("Scheduler iniciado, esperando para ejecutar trabajos.")

# Bucle infinito para mantener el script en ejecución y verificar trabajos pendientes
while True:
    schedule.run_pending()
    logger.debug("Ejecutando trabajos programados si los hay.")
    time.sleep(60)  # Espera un minuto antes de verificar nuevamente
