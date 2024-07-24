import os
import sys
import logging.config
from flask import Flask, render_template, request
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from web_scraping_project.models import Quote

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
try:
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
except FileNotFoundError:
    print("El archivo de configuración de logging 'logging.conf' no se encuentra.")
except Exception as e:
    print(f"Error al configurar el logging: {e}")

app = Flask(__name__)

# Configuración de la base de datos
db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Tamaño de página para la paginación
PAGE_SIZE = 10

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    offset = (page - 1) * PAGE_SIZE

    try:
        with Session() as session:
            # Filtrar citas según el término de búsqueda
            query = session.query(Quote)
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        Quote.quote.ilike(search_term),
                        Quote.author.ilike(search_term),
                        Quote.tags.ilike(search_term)
                    )
                )

            quotes = query.order_by(Quote.id).offset(offset).limit(PAGE_SIZE).all()
            total_quotes = query.count()
            total_pages = (total_quotes + PAGE_SIZE - 1) // PAGE_SIZE

            return render_template(
                'index.html', 
                quotes=quotes, 
                page=page, 
                page_size=PAGE_SIZE, 
                total_pages=total_pages, 
                search=search
            )
    except Exception as e:
        app.logger.error(f"Error al obtener citas: {str(e)}")
        return "Ha ocurrido un error al cargar las citas.", 500
    finally:
        Session.remove()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', quotes=[], page=1, page_size=PAGE_SIZE, total_pages=1), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('index.html', quotes=[], page=1, page_size=PAGE_SIZE, total_pages=1), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
