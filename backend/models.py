from sqlalchemy import Column, Integer, String, Date, create_engine, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class AstrologyRecord(Base):
    __tablename__ = "astrology_records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    birth_date = Column(Date)
    planet = Column(String)
    position = Column(JSON)

# SQLite database setup
DATABASE_URL = "sqlite:///./astrology.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
