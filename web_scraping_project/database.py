import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from web_scraping_project.models import Base

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Crear el motor de la base de datos
engine = create_engine(DB_URL, echo=True)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear todas las tablas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Función para inicializar la base de datos
def init_db():
    create_tables()

if __name__ == "__main__":
    init_db()
