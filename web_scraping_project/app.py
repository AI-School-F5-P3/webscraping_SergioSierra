from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Quote

app = Flask(__name__)

engine = create_engine('postgresql://username:password@db:5432/quotes_db')
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    session = Session()
    quotes = session.query(Quote).all()
    session.close()
    return render_template('index.html', quotes=quotes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
