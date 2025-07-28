
from sqlalchemy.orm import Session
from db import SessionLocal
from ModelosBD import Note

class NoteService:
    def __init__(self):
        print("Note service en línea")

    # Crear nota en un calendario
    def crear_nota(self, calendar_id: int, title: str, content: str, due_date=None, priority="media", status="pendiente"):
        db: Session = SessionLocal()
        nota = Note(title=title, content=content, due_date=due_date,
                    priority=priority, status=status, calendar_id=calendar_id)
        db.add(nota)
        db.commit()
        db.refresh(nota)
        db.close()
        return nota

    # Obtener notas de un calendario
    def obtener_notas_por_calendario(self, calendar_id: int):
        db: Session = SessionLocal()
        notas = db.query(Note).filter(Note.calendar_id == calendar_id).all()
        db.close()
        return notas

    # Eliminar nota por ID
    def eliminar_nota(self, note_id: int):
        db: Session = SessionLocal()
        nota = db.query(Note).filter(Note.id == note_id).first()
        if nota:
            db.delete(nota)
            db.commit()
        db.close()
