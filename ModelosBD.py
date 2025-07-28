from sqlalchemy import Column, Integer, String, DateTime, ForeignKey , Text
from sqlalchemy.orm import relationship

from dotenv import load_dotenv

import db



class User(db.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    Nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # RELACIÓN 1:1
    calendar = relationship("Calendar", back_populates="user", uselist=False)

class Calendar(db.Base):
    __tablename__ = "calendars"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="Calendario")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="calendar")
    notes = relationship("Note", back_populates="calendar", cascade="all, delete")
    events = relationship("Event", back_populates="calendar", cascade="all, delete")

class Note(db.Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, default="media")  # baja, media, alta
    status = Column(String, default="pendiente")  # completado, pendiente

    calendar_id = Column(Integer, ForeignKey("calendars.id"))
    calendar = relationship("Calendar", back_populates="notes")

class Event(db.Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    category = Column(String, default="general")

    calendar_id = Column(Integer, ForeignKey("calendars.id"))
    calendar = relationship("Calendar", back_populates="events")


