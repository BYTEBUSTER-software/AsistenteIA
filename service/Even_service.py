
from sqlalchemy.orm import Session
from db import SessionLocal
from ModelosBD import Event

class EventService:
    def __init__(self):
        print("Event service en línea")

    # Crear evento en un calendario
    def crear_evento(self, calendar_id: int, title: str, description: str, start, end, category: str):
        db: Session = SessionLocal()
        evento = Event(title=title, description=description, start=start, end=end,
                       category=category, calendar_id=calendar_id)
        db.add(evento)
        db.commit()
        db.refresh(evento)
        db.close()
        return evento

    # Obtener eventos de un calendario
    def obtener_eventos_por_calendario(self, calendar_id: int):
        db: Session = SessionLocal()
        eventos = db.query(Event).filter(Event.calendar_id == calendar_id).all()
        db.close()
        return eventos

    # Eliminar evento por ID
    def eliminar_evento(self, event_id: int):
        db: Session = SessionLocal()
        evento = db.query(Event).filter(Event.id == event_id).first()
        if evento:
            db.delete(evento)
            db.commit()
        db.close()