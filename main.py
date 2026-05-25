from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from database import create_db_and_tables, get_session, engine
from models import User, UserCreate, UserResponse
from auth import get_password_hash, verify_password

@asynccontextmanager
async def lifespan(app: FastAPI):
   
    create_db_and_tables()
    
  
    with Session(engine) as session:
        statement = select(User).where(User.username == "admin")
        user = session.exec(statement).first()
        if not user:
           
            hashed_pwd = get_password_hash("admin123")
            new_user = User(username="admin", hashed_password=hashed_pwd)
            session.add(new_user)
            session.commit()
            print("Usuario de ejemplo 'admin' (clave: 'admin123') creado exitosamente.")

    yield
  

app = FastAPI(title="API de Autenticación Segura", lifespan=lifespan)

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_pwd)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

@app.post("/login")
def login(user_data: UserCreate, session: Session = Depends(get_session)):
   
    statement = select(User).where(User.username == user_data.username)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
   
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    return {"message": "Autenticación exitosa", "user_id": user.id, "username": user.username}

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Autenticación Segura"}
