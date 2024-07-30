
---

# Web Scraping Project - Sergio Sierra
Este proyecto es una aplicación de web scraping que extrae citas de la web [Quotes to Scrape](http://quotes.toscrape.com). Utiliza `BeautifulSoup` para el scraping, `SQLAlchemy` para la gestión de la base de datos y `Flask` para el frontend. Los datos extraídos se almacenan en una base de datos PostgreSQL.

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

## Descripción del Proyecto

Este proyecto es una aplicación de web scraping que extrae citas de la web `Quotes to Scrape`. Utiliza `BeautifulSoup` para el scraping, `SQLAlchemy` para la gestión de la base de datos y `Flask` para el frontend. Los datos extraídos se almacenan en una base de datos PostgreSQL.

## Características

- Extracción de citas, autores, biografías y tags desde la web.
- Almacenamiento de datos en una base de datos PostgreSQL.
- Frontend básico para visualizar las citas.
- Programación de tareas de scraping automatizadas.
- Gestión de errores robusta y pruebas unitarias.

## Estructura del Proyecto

```
webscraping_SergioSierra/
├── pyproject.toml            # Configuración del proyecto y dependencias.
├── README.md                 # Este archivo.
├── web_scraping_project/     # Código fuente del proyecto.
│   ├── __init__.py           # Inicializa el paquete.
│   ├── scraper.py            # Script principal de web scraping.
│   ├── app.py                # Aplicación Flask para el frontend.
│   ├── models.py             # Modelos de datos para SQLAlchemy.
│   ├── templates/            # Plantillas HTML para el frontend.
│   │   └── index.html
│   └── static
│        ├── scripts.js       # Scripts JavaScript.
│        └── styles.css       # Estilos CSS.
├── tests/                    # Pruebas unitarias.
│   ├── __init__.py           # Inicializa el paquete de pruebas.
│   └── test_scraper.py       # Pruebas para el scraper.   
└── .env.example              # Archivo de ejemplo para variables de entorno.
```

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación.
- **BeautifulSoup**: Librería para web scraping.
- **Requests**: Para realizar solicitudes HTTP.
- **SQLAlchemy**: ORM para interactuar con PostgreSQL.
- **Flask**: Microframework para el frontend.
- **PostgreSQL**: Sistema de gestión de bases de datos.
- **pytest**: Para la realización de pruebas unitarias.

## Configuración

**Instalar Dependencias**

   Crea un entorno virtual y activa:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa .venv\Scripts\activate
   ```

   Instala las dependencias con Poetry:

   ```bash
   requirements install
   ```

   **Ejemplo `.env`**:
   ```env
   DB_URL=postgresql://username:password@db:5432/quotes_db
   ```

## Uso

   Scraping
   Para iniciar el scraping de las citas:
   ```
   python scraper.py
   ```
   El script obtendrá citas de Quotes to Scrape y las almacenará en la base de datos configurada.

   Para iniciar la aplicación web:

   ```
   python web_scraping_project/app.py
   ```
## Pruebas

   Para ejecutar las pruebas unitarias:
   ```
   pytest
   ```
## Despliegue

   Para desplegar la aplicación:
   ```
   python -m web_scraping_project.app
   ```

## Contribución

Las contribuciones son bienvenidas. Abre un issue o envía un pull request en GitHub para discutir cualquier cambio. ¡Gracias!


