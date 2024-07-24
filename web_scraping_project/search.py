from sqlalchemy.orm import Session
from web_scraping_project.models import Quote

def search_quotes(session: Session, keyword: str):
    return session.query(Quote).filter(Quote.quote.ilike(f'%{keyword}%')).all()
