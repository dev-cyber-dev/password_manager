from sqlalchemy.orm import Session
from . import models, utils


def upsert_password(db: Session, service_name: str, password: str):
    db_password = db.query(models.Password).filter_by(
        service_name=service_name).first()
    encrypted = utils.encrypt_password(password)
    if db_password:
        db_password.encrypted_password = encrypted
    else:
        db_password = models.Password(
            service_name=service_name, encrypted_password=encrypted)
        db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


def get_password(db: Session, service_name: str):
    db_password = db.query(models.Password).filter_by(
        service_name=service_name).first()
    if db_password:
        return utils.decrypt_password(db_password.encrypted_password)
    return None


def search_passwords(db: Session, service_name_part: str):
    return db.query(models.Password).filter(models.Password.service_name.ilike(f"%{service_name_part}%")).all()
