from fastapi import FastAPI, HTTPException , Depends
from models import Event,Usuario, EventIn, get_events
from utils.summarizer import generate_summary
from utils.classifier import classify_event
from utils.searcher import search_events
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service.User_service import UserService
from jose import jwt
from Seguridad import Segutridad;
import db
from ModelosBD import User, Calendar, Note
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from service.Note_service import NoteService
from service.Calendar_service import CalendarService
from fastapi.middleware.cors import CORSMiddleware

db.Base.metadata.create_all(bind=db.engine)
user_service = UserService()
seg=Segutridad()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #  puedes reemplazar "*" por ["http://localhost:3000"] si solo permites tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
calendar_service = CalendarService()
note_service = NoteService()
#app.run(host="0.0.0.0", port=5000, debug=True)

load_dotenv()
SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
# Base de datos temporal (lista)


@app.get("/")
def list_events():
    return {"message": "¡Funciona!"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual =user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual:
        raise HTTPException(status_code=404 ,detail="usuario no encontrado")
    if not seg.verify_password(form_data.password, usuarioActual.password):
        raise HTTPException(status_code=401 ,detail="contraseña errorena ")
    payload = {
        "sub": form_data.username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}
@app.post("/singUp")
def crearUsuario(user:Usuario):
    if user_service.buscar_usuario_por_email(user.email):
        raise HTTPException(status_code=400 , detail="gmail existente")
    passwordSegura=seg.hash_password(user.password)
    nuevo = user_service.crear_usuario(user.nombre,user.email, passwordSegura)
    return nuevo

# Crear evento IA y guardar como nota en base de datos
@app.post("/event")
def create_event(event: EventIn, form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual = user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    category = classify_event(event.description)

    # Crear nota asociada al calendario del usuario
    if not usuarioActual.calendar:
        raise HTTPException(status_code=400, detail="Usuario no tiene calendario")

    nueva_nota = note_service.crear_nota(
        calendar_id=usuarioActual.calendar.id,
        title=event.title,
        content=event.description,
        due_date=event.start
    )

    return {"nota": nueva_nota, "categoria": category}

# Listar todas las notas del usuario autenticado
@app.get("/events")
def list_user_notes(form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual = user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual or not usuarioActual.calendar:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    notas = note_service.obtener_notas_por_calendario(usuarioActual.calendar.id)
    return notas

@app.get("/summary")
def get_summary(form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual = user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual or not usuarioActual.calendar:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    notas = note_service.obtener_notas_por_calendario(usuarioActual.calendar.id)
    return generate_summary(notas)


@app.get("/search")
def search(q: str, form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual = user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual or not usuarioActual.calendar:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    notas = note_service.obtener_notas_por_calendario(usuarioActual.calendar.id)
    return search_events(notas, q)

@app.get("/prioridad")
def notas_por_prioridad(form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual = user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual or not usuarioActual.calendar:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    notas = note_service.obtener_notas_por_calendario(usuarioActual.calendar.id)
    return sorted(notas, key=lambda x: x.priority, reverse=True)

@app.get("/resumen_dia")
def resumen_por_dia(dia: str, form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual = user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual or not usuarioActual.calendar:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    notas = note_service.obtener_notas_por_calendario(usuarioActual.calendar.id)
    dia_dt = datetime.strptime(dia, "%Y-%m-%d")
    notas_dia = [n for n in notas if n.due_date.date() == dia_dt.date()]
    return generate_summary(notas_dia)

@app.get("/tareas_curso")
def tareas_por_titulo(titulo: str, form_data: OAuth2PasswordRequestForm = Depends()):
    usuarioActual = user_service.buscar_usuario_por_email(form_data.username)
    if not usuarioActual or not usuarioActual.calendar:
        raise HTTPException(status_code=404, detail="Calendario no encontrado")
    notas = note_service.obtener_notas_por_calendario(usuarioActual.calendar.id)
    return [n for n in notas if titulo.lower() in n.title.lower()]