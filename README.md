
---

# Web Scraping Project - Sergio Sierra

Este proyecto realiza web scraping para extraer citas de la web [Quotes to Scrape](http://quotes.toscrape.com) y almacena los datos en una base de datos PostgreSQL. Incluye un frontend básico para visualizar las citas, todo dockerizado para facilitar el despliegue.

## Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Configuración](#configuración)
- [Uso](#uso)
- [Pruebas](#pruebas)
- [Despliegue](#despliegue)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Descripción del Proyecto

Este proyecto es una aplicación de web scraping que extrae citas de la web `Quotes to Scrape`. Utiliza `BeautifulSoup` para el scraping, `SQLAlchemy` para la gestión de la base de datos y `Flask` para el frontend. Los datos extraídos se almacenan en una base de datos PostgreSQL y la aplicación está dockerizada para facilitar su despliegue.

## Características

- Extracción de citas, autores y tags desde la web.
- Almacenamiento de datos en una base de datos PostgreSQL.
- Frontend básico para visualizar las citas.
- Dockerización para un entorno de ejecución consistente.
- Gestión de errores robusta y pruebas unitarias.

## Estructura del Proyecto

```plaintext
webscraping_SergioSierra/
├── pyproject.toml            # Configuración del proyecto y dependencias.
├── README.md                 # Este archivo.
├── web_scraping_project/     # Código fuente del proyecto.
│   ├── __init__.py           # Inicializa el paquete.
│   ├── scraper.py            # Script principal de web scraping.
│   ├── app.py                # Aplicación Flask para el frontend.
│   ├── models.py             # Modelos de datos para SQLAlchemy.
│   └── templates/            # Plantillas HTML para el frontend.
│       └── index.html
├── tests/                    # Pruebas unitarias.
│   ├── __init__.py           # Inicializa el paquete de pruebas.
│   ├── test_scraper.py       # Pruebas para el scraper.
│   └── test_app.py           # Pruebas para la aplicación Flask.
├── Dockerfile                # Dockerfile para construir la imagen del proyecto.
├── docker-compose.yml        # Configuración de Docker Compose.
└── .env.example              # Archivo de ejemplo para variables de entorno.
```

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación.
- **BeautifulSoup**: Librería para web scraping.
- **Requests**: Para realizar solicitudes HTTP.
- **SQLAlchemy**: ORM para interactuar con PostgreSQL.
- **Flask**: Microframework para el frontend.
- **PostgreSQL**: Sistema de gestión de bases de datos.
- **Docker**: Para la contenedorización y despliegue.
- **pytest**: Para la realización de pruebas unitarias.

## Configuración

1. **Instalar Dependencias**

   Crea un entorno virtual y activa:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa .venv\Scripts\activate
   ```

   Instala las dependencias con Poetry:

   ```bash
   poetry install
   ```

2. **Configuración de Docker**

   Copia el archivo `.env.example` a `.env` y ajusta las variables según tu configuración:

   ```bash
   cp .env.example .env
   ```

   **Ejemplo `.env`**:
   ```env
   DB_URL=postgresql://username:password@db:5432/quotes_db
   ```

## Uso

1. **Iniciar el Proyecto con Docker**

   Construye y levanta los contenedores:

   ```bash
   docker-compose up --build
   ```

   La aplicación estará disponible en [http://localhost:5000](http://localhost:5000).

2. **Ejecutar el Scraper**

   Puedes ejecutar el scraper manualmente dentro del contenedor si deseas realizar scraping en cualquier momento:

   ```bash
   docker-compose run web python web_scraping_project/scraper.py
   ```

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
poetry run pytest
```

## Despliegue

Para desplegar en un servidor:

1. **Configura tu servidor** (DigitalOcean, AWS, etc.).
2. **Instala Docker y Docker Compose** en el servidor.
3. **Sube el código al servidor** y ejecuta:

   ```bash
   docker-compose up --build
   ```

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request en GitHub para discutir cualquier cambio.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

---
