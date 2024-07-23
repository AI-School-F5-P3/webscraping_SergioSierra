# webscraping_SergioSierra

---

# Proyecto de Web Scraping para XYZ Corp

## Descripción del Proyecto

Este proyecto tiene como objetivo desarrollar un programa en Python para realizar web scraping en la web [Quotes to Scrape](http://quotes.toscrape.com/). El programa extrae todas las frases, junto con la información adicional (autor, tags) y la página "about" de los autores. Los datos extraídos se almacenan en una base de datos PostgreSQL.

## Tecnologías Utilizadas

- **Python**: BeautifulSoup, Requests, psycopg2
- **Docker**: Para crear un entorno de ejecución consistente
- **PostgreSQL**: Base de datos para almacenar los datos extraídos

## Estructura del Proyecto

```
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── scraper.py
└── db
    ├── init.sql
```

## Requisitos Previos

- Docker instalado en tu máquina
- Docker Compose instalado

## Instrucciones de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/AI-School-F5-P3/webscraping_SergioSierra.git
cd webscraping_SergioSierra
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:

```
POSTGRES_DB=quotes_db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
```

### 3. Construir y Levantar los Servicios con Docker Compose

```bash
docker-compose up --build
```

Esto construirá la imagen de Docker y levantará los servicios definidos en `docker-compose.yml`.

## Uso del Script

El script `scraper.py` se ejecuta automáticamente cuando el contenedor de Docker se levanta. Extrae los datos de la web y los almacena en la base de datos PostgreSQL.

### Acceso a la Base de Datos

Puedes acceder a la base de datos PostgreSQL utilizando cualquier cliente de base de datos con las siguientes credenciales:

- **Host**: `localhost`
- **Puerto**: `5432`
- **Usuario**: El definido en `.env`
- **Contraseña**: La definida en `.env`
- **Base de Datos**: `quotes_db`

## Documentación del Código

### `scraper.py`

Este archivo contiene el script principal para realizar el web scraping. Utiliza las bibliotecas BeautifulSoup y Requests para extraer los datos, y psycopg2 para insertarlos en la base de datos.

```python
import requests
from bs4 import BeautifulSoup
import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host='db'
    )
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            quote TEXT,
            author TEXT,
            tags TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def get_quotes_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')

    conn = get_db_connection()
    cur = conn.cursor()

    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        cur.execute("INSERT INTO quotes (quote, author, tags) VALUES (%s, %s, %s)", (text, author, ','.join(tags)))

    conn.commit()
    cur.close()
    conn.close()

def main():
    create_table()
    base_url = 'http://quotes.toscrape.com/page/'
    page = 1
    while True:
        url = base_url + str(page)
        response = requests.get(url)
        if "No quotes found!" in response.text:
            break
        get_quotes_from_page(url)
        page += 1

if __name__ == '__main__':
    main()
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue los siguientes pasos para contribuir:

1. Realiza un fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`).
3. Realiza tus cambios y haz commit (`git commit -m 'Agregar nueva feature'`).
4. Haz push a la rama (`git push origin feature/nueva-feature`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia XYZ. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

