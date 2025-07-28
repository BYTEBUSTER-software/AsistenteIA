from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey , Text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL =os.getenv("DB_link")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
