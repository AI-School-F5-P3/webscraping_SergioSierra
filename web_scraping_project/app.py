import os
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from .models import Quote

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar la conexión a la base de datos usando variables de entorno
db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)

# Crear una sesión con ámbito para manejar múltiples hilos
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

@app.route('/')
def index():
    try:
        quotes = Session.query(Quote).all()
        return render_template('index.html', quotes=quotes)
    except Exception as e:
        app.logger.error(f"Error al obtener citas: {str(e)}")
        return "Ha ocurrido un error al cargar las citas.", 500
    finally:
        Session.remove()  # Asegura que la sesión se cierre correctamente

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('FLASK_DEBUG', 'False') == 'True')