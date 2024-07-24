from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    quote = Column(String, nullable=False)
    author = Column(String, nullable=False)
    tags = Column(String)

# Setup the database engine and session
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
Session = sessionmaker(bind=engine)
session = Session()

