import serializers
import database
from fastapi import APIRouter, Depends, HTTPException, status
from exceptions.ficheLapin import FicheLapinNotFound, FicheLapinAlreadyExists, WrongAuthor
from exceptions.user import UserNotFound
from routers.utils import get_user_id
from serializers.ficheLapin import FicheLapinWithAuthor
from services import ficheLapin as ficheLapin_service
from sqlalchemy.orm import Session

ficheLapin_router = APIRouter(prefix="/ficheslapin", tags=["fichelapin"])


# ============================================================================
# CREATE
# ============================================================================
@ficheLapin_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_fichelapin(
    fichelapin: serializers.FicheLapin,
    db: Session = Depends(database.get_db),
    user_id: str = Depends(get_user_id)
):
    try:
        fichelapin.auteur_id = user_id
        return ficheLapin_service.create_fichelapin(db=db, fichelapin=fichelapin)
    except FicheLapinAlreadyExists:
        raise HTTPException(status_code=400, detail="FicheLapin already exists")



# ============================================================================
# READ ALL
# ============================================================================
@ficheLapin_router.get("/", response_model=list[FicheLapinWithAuthor])
async def get_all(db: Session = Depends(database.get_db), user_id: str = Depends(get_user_id)):
    return ficheLapin_service.get_all_ficheslapin(db=db, user_id=None)

   

# ============================================================================
# READ BY ID
# ============================================================================
@ficheLapin_router.get("/{fichelapin_id}", response_model=FicheLapinWithAuthor)
async def get_by_id(fichelapin_id: str, db: Session = Depends(database.get_db), user_id: str = Depends(get_user_id)):
    try:
        return ficheLapin_service.get_fichelapin_by_id(fichelapin_id, db)
    except FicheLapinNotFound:
        raise HTTPException(status_code=404, detail="Fiche lapin not found")


# ============================================================================
# UPDATE
# ============================================================================
@ficheLapin_router.put("/{fichelapin_id}")
async def update(
    fichelapin_id: str,
    updates: dict,
    db: Session = Depends(database.get_db),
    user_id: str = Depends(get_user_id),
):
    try:
        return ficheLapin_service.update_fichelapin(fichelapin_id, db, updates, user_id)
    except FicheLapinNotFound:
        raise HTTPException(status_code=404, detail="Fiche lapin not found")
    except WrongAuthor:
        raise HTTPException(status_code=403, detail="Only author can update their fiche")


# ============================================================================
# DELETE
# ============================================================================
@ficheLapin_router.delete("/{fichelapin_id}")
async def delete_by_user(
    fichelapin_id: str,
    db: Session = Depends(database.get_db),
    user_id: str = Depends(get_user_id),
):
    try:
        return ficheLapin_service.delete_fichelapin_by_user(fichelapin_id, db, user_id)
    except FicheLapinNotFound:
        raise HTTPException(status_code=404, detail="Fiche lapin not found")
    except WrongAuthor:
        raise HTTPException(status_code=403, detail="Only author can delete their fiche")
