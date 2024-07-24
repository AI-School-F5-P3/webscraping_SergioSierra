import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
from web_scraping_project.models import Base

# Añadir el directorio del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Alembic Config object
config = context.config

# Verificar que todas las variables de entorno necesarias estén presentes
required_env_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"La variable de entorno {var} no está definida")

# Configurar la URL de la base de datos dinámicamente
db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
config.set_main_option('sqlalchemy.url', db_url)

# Imprimir la URL de la base de datos para depuración
print(f"Base de datos URL: {db_url}")

# Interpretar el archivo de configuración para el logging
if config.config_file_name is not None:
    fileConfig(os.path.join(os.path.dirname(__file__), 'logging.conf'))

# MetaData object para soporte de 'autogenerate'
target_metadata = Base.metadata

def run_migrations_offline():
    """Ejecutar migraciones en modo 'offline'."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
