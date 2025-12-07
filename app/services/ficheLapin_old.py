# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session
# from datetime import datetime

# from models.ficheLapin import FicheLapin
# import serializers

# from typing import List, Optional
# from services import user as user_service
# from exceptions.ficheLapin import FicheLapinNotFound, FicheLapinAlreadyExists, WrongAuthor

# def get_all_ficheslapin(db: Session, skip: int = 0, limit: int = 10) -> list[FicheLapin]:
#     records = db.query(FicheLapin).offset(skip).limit(limit).all()
#     for record in records:
#         record.id = str(record.id)
#     return records


# def get_fichelapin_by_id(fichelapin_id: str, db: Session) -> FicheLapin:
#     record = db.query(FicheLapin).filter(FicheLapin.id == ficheLapin_id).first()
#     if not record:
#         raise FicheLapinNotFound

#     record.id = str(record.id)
#     return record


# def get_fichelapin_by_name(name: str, db: Session) -> list[FicheLapin]:
#     records = db.query(FicheLapin).filter(FicheLapin.nom == name).all()
#     for record in records:
#         record.id = str(record.id)
#     return records


# def update_fichelapin(fichelapin_id: str, db: Session, fichelapin: serializers.FicheLapin) -> FicheLapin:
#     db_fichelapin = get_fichelapin_by_id(fichelapin_id=fichelapin_id, db=db)
#     # for var, value in vars(fichelapin).items():
#     #     setattr(db_fichelapin, var, value) if value else None

#     fichelapin.model_dump(exclude_unset=True)    
#     db_fichelapin.updated_at = datetime.now()
#     db.add(db_fichelapin)
#     db.commit()
#     db.refresh(db_fichelapin)
#     return db_fichelapin    


# def delete_fichelapin(fichelapin_id: str, db: Session) -> FicheLapin:
#     db_fichelapin = get_fichelapin_by_id(fichelapin_id=fichelapin_id, db=db)
#     db.delete(db_fichelapin)
#     db.commit()
#     return db_fichelapin

# def delete_fichelapin_by_user(fichelapin_id: str, db: Session, user_id: str) -> FicheLapin:
#     db_fichelapin = get_fichelapin_by_id(fichelapin_id=fichelapin_id, db=db)
#     if db_fichelapin.auteur_id != user_id:
#         raise WrongAuthor
#     db.delete(db_fichelapin)
#     db.commit()
#     return db_fichelapin

# def delete_all_ficheslapin(db: Session) -> list[FicheLapin]:
#     records = db.query(FicheLapin).filter()
#     for record in records:
#         db.delete(record)
#     db.commit()
#     return records

# def create_fichelapin(db: Session, fichelapin: serializers.FicheLapin) -> FicheLapin:    
#     # A vérifier
#     auteur_id = fichelapin.auteur_id

#     # Peut raise un UserNotFound
#     user_service.get_user_by_id(user_id=auteur_id, db=db)  

#     db_fichelapin = FicheLapin(**fichelapin.model_dump())
#     db.add(db_fichelapin)
#     try:
#         db.commit()
#     except IntegrityError:
#         db.rollback()
#         raise FicheLapinAlreadyExists   

#     db.refresh(db_fichelapin)
#     return db_fichelapin 

