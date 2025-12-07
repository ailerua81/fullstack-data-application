from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime

from models.ficheLapin import FicheLapin
import serializers
from services import user as user_service
from exceptions.ficheLapin import FicheLapinNotFound, FicheLapinAlreadyExists, WrongAuthor


def get_all_ficheslapin(db: Session, user_id: str = None):
    if user_id:
        return db.query(FicheLapin).filter(FicheLapin.auteur_id == user_id).all()
    return db.query(FicheLapin).all()


def get_fichelapin_by_id(fichelapin_id: str, db: Session):
    record = db.query(FicheLapin).filter(FicheLapin.id == fichelapin_id).first()
    if not record:
        raise FicheLapinNotFound
    return record


def create_fichelapin(db: Session, fichelapin: serializers.FicheLapin):
    author_id = fichelapin.auteur_id

    # Vérifie que l’auteur existe
    user_service.get_user_by_id(user_id=author_id, db=db)

    db_fichelapin = FicheLapin(**fichelapin.model_dump())

    db.add(db_fichelapin)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise FicheLapinAlreadyExists

    db.refresh(db_fichelapin)
    return db_fichelapin



def update_fichelapin(fichelapin_id: str, db: Session, updates: dict, user_id: str):
    fiche = db.query(FicheLapin).filter(FicheLapin.id == fichelapin_id).first()

    if not fiche:
        raise FicheLapinNotFound

    if fiche.auteur_id != user_id:
        raise WrongAuthor

    
    for key, value in updates.items():
        if hasattr(fiche, key):
            setattr(fiche, key, value)

    db.commit()
    db.refresh(fiche)

    return fiche



def delete_fichelapin_by_user(fichelapin_id: str, db: Session, user_id: str):
    fiche = get_fichelapin_by_id(fichelapin_id, db)

    if fiche.auteur_id != user_id:
        raise WrongAuthor

    db.delete(fiche)
    db.commit()
    return fiche
