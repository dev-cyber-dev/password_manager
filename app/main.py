from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud, utils
from .db import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/password/{service_name}", response_model=schemas.PasswordResponse)
def create_password(service_name: str, password_in: schemas.PasswordCreate, db: Session = Depends(get_db)):
    db_entry = crud.upsert_password(db, service_name, password_in.password)
    return {"service_name": db_entry.service_name, "password": password_in.password}


@app.get("/password/{service_name}", response_model=schemas.PasswordResponse)
def read_password(service_name: str, db: Session = Depends(get_db)):
    password = crud.get_password(db, service_name)
    if not password:
        raise HTTPException(status_code=404, detail="Password not found")
    return {"service_name": service_name, "password": password}


@app.get("/password/")
def search(service_name: str, db: Session = Depends(get_db)):
    results = crud.search_passwords(db, service_name)
    return [{"service_name": p.service_name, "password": utils.decrypt_password(p.encrypted_password)} for p in results]
