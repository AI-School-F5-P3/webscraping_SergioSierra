from sqlalchemy.orm import Session
from web_scraping_project.models import Quote

def filter_by_author(session: Session, author: str):
    return session.query(Quote).filter(Quote.author == author).all()

def filter_by_tag(session: Session, tag: str):
    return session.query(Quote).filter(Quote.tags.ilike(f'%{tag}%')).all()
