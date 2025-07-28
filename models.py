from pydantic import BaseModel
from datetime import datetime
from typing import List

#Define la estructura de los datos (modelo de evento)
#evento recibido desde el frontend
class EventIn(BaseModel):
    title: str
    description: str
    start: datetime
    end: datetime


class Event(EventIn): 
    category: str

class Usuario(BaseModel): 
    nombre: str
    email: str
    password: str


def get_events() -> List[Event]:
    # Aquí iría la consulta real si usas base de datos
    return []
