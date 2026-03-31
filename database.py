import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from config import get_settings


settings=get_settings()

engine = create_engine(
    settings.database_url,
    pool_size=5,        # keep 5 connections open always
    max_overflow=10,    # allow 10 extra in traffic spikes
    pool_timeout=30,    # wait max 30 seconds for a connection
    pool_recycle=1800,  # recycle connections every 30 mins
    pool_pre_ping=True                    # prevents stale connections
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
