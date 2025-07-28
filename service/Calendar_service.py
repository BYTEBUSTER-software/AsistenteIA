# services/calendar_service.py

from sqlalchemy.orm import Session
from db import SessionLocal
from ModelosBD import Calendar, User

class CalendarService:
    def __init__(self):
        print("Calendar service en línea")

    # Crear calendario asociado a un usuario
    def crear_calendario(self, user_id: int, name: str = "Calendario"):
        db: Session = SessionLocal()
        calendario = Calendar(name=name, user_id=user_id)
        db.add(calendario)
        db.commit()
        db.refresh(calendario)
        db.close()
        return calendario

    # Obtener calendario de un usuario
    def obtener_calendario_por_usuario(self, user_id: int):
        db: Session = SessionLocal()
        calendario = db.query(Calendar).filter(Calendar.user_id == user_id).first()
        db.close()
        return calendario

    # Eliminar calendario por ID
    def eliminar_calendario(self, calendar_id: int):
        db: Session = SessionLocal()
        calendario = db.query(Calendar).filter(Calendar.id == calendar_id).first()
        if calendario:
            db.delete(calendario)
            db.commit()
        db.close()

