from fastapi import FastAPI, HTTPException
from models import Event, EventIn, get_events
from utils.summarizer import generate_summary
from utils.classifier import classify_event
from utils.searcher import search_events



app = FastAPI()

# Base de datos temporal (lista)
events = []


@app.get("/")
def list_events():
    return {"message": "¡Funciona!"}

@app.post("/event")
def create_event(event: EventIn):
    category = classify_event(event.description)
    new_event = Event(**event.dict(), category=category)
    events.append(new_event)
    return new_event

@app.get("/events")
def list_events():
    return events

@app.get("/summary")
def get_summary():  #resumen 
    return generate_summary(events)

@app.get("/search")
def search(q: str): #buscar 
    return search_events(events, q)
