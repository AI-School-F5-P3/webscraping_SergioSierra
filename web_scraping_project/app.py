from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from web_scraping_project.models import Quote
import os
import logging.config
from web_scraping_project.filters import filter_by_author, filter_by_tag
from web_scraping_project.search import search_quotes  # Importa la función de búsqueda
from web_scraping_project.pagination import get_paginated_quotes

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
try:
    logging.config.fileConfig('web_scraping_project/logging.conf', disable_existing_loggers=False)
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
    page = request.args.get('page', 1, type=int)  # Obtiene el número de página de los argumentos de la solicitud
    search = request.args.get('search', '', type=str)  # Obtiene el término de búsqueda de los argumentos de la solicitud
    author = request.args.get('author', '', type=str)  # Obtiene el autor de los argumentos de la solicitud
    tag = request.args.get('tag', '', type=str)  # Obtiene la etiqueta de los argumentos de la solicitud
    offset = (page - 1) * PAGE_SIZE  # Calcula el offset para la paginación

    try:
        with Session() as session:
            app.logger.info(f"Buscando citas. Página: {page}, Búsqueda: '{search}', Autor: '{author}', Etiqueta: '{tag}'")

            # Construir la consulta
            query = session.query(Quote)

            if search:
                query = query.filter(Quote.quote.ilike(f'%{search}%'))
            if author:
                query = query.filter(Quote.author.ilike(f'%{author}%'))
            if tag:
                query = query.filter(Quote.tags.ilike(f'%{tag}%'))

            # Aplicar la paginación
            quotes = query.order_by(Quote.id).offset(offset).limit(PAGE_SIZE).all()
            total_quotes = query.count()  # Contar el total de citas para la paginación
            total_pages = (total_quotes + PAGE_SIZE - 1) // PAGE_SIZE  # Calcular el número total de páginas

            app.logger.info(f"Se encontraron {total_quotes} citas. Total páginas: {total_pages}")
            return render_template(
                'index.html',
                quotes=quotes,
                page=page,
                page_size=PAGE_SIZE,
                total_pages=total_pages,
                search=search,
                author=author,
                tag=tag
            )
            
    except Exception as e:
        app.logger.error(f"Error al obtener citas: {str(e)}")
        return "Ha ocurrido un error al cargar las citas.", 500
    finally:
        Session.remove()


@app.route('/log_bio_view', methods=['POST'])
def log_bio_view():
    data = request.get_json()
    author = data.get('author')
    app.logger.info(f"Biografía de {author} vista.")
    return jsonify({"status": "success", "message": f"Biografía de {author} vista."})

@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning("Página no encontrada: 404")
    return render_template('index.html', quotes=[], page=1, page_size=PAGE_SIZE, total_pages=1), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error("Error interno del servidor: 500")
    return render_template('index.html', quotes=[], page=1, page_size=PAGE_SIZE, total_pages=1), 500

if __name__ == '__main__':
    app.logger.info("Iniciando la aplicación Flask.")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)