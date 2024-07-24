from sqlalchemy.orm import Session
from web_scraping_project.models import Quote

def get_paginated_quotes(session: Session, page: int, page_size: int = 10):
    return session.query(Quote).offset((page - 1) * page_size).limit(page_size).all()
