from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey , Text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os


Base = declarative_base()

DATABASE_URL = ""
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # RELACIÓN 1:1
    calendar = relationship("Calendar", back_populates="user", uselist=False)

class Calendar(Base):
    __tablename__ = "calendars"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="Calendario")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="calendar")
    notes = relationship("Note", back_populates="calendar", cascade="all, delete")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, default="media")  # baja, media, alta
    status = Column(String, default="pendiente")  # completado, pendiente

    calendar_id = Column(Integer, ForeignKey("calendars.id"))
    calendar = relationship("Calendar", back_populates="notes")



