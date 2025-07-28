# services/user_service.py

from sqlalchemy.orm import Session
from db import SessionLocal
from ModelosBD import User 

class UserService :
    def __init__(self):
        print("servise en linea")
        pass
    
    # Crear usuario
    def crear_usuario(self,nombre: str,email: str, password: str):
        db: Session = SessionLocal()
        nuevo = User(Nombre =nombre ,email=email, password=password)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        db.close()
        return nuevo


    # Obtener todos los usuarios
    def obtener_usuarios(self):
        db: Session = SessionLocal()
        usuarios = db.query(User).all()
        db.close()
        return usuarios


    # Buscar usuario por email
    def buscar_usuario_por_email(self,email: str):
        db: Session = SessionLocal()
        usuario = db.query(User).filter(User.email == email).first()
        db.close()
        return usuario


    # Eliminar usuario por ID
    def eliminar_usuario_por_id(self,user_id: int):
        db: Session = SessionLocal()
        usuario = db.query(User).filter(User.id == user_id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
        db.close()
