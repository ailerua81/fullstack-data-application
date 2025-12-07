# import serializers
# import database
# from fastapi import APIRouter, Depends, HTTPException


# from exceptions.ficheLapin import FicheLapinNotFound, FicheLapinAlreadyExists, WrongAuthor
# from exceptions.user import UserNotFound
# from routers.utils import get_user_id
# from serializers.ficheLapin import FicheLapinWithAuthor
# from services import ficheLapin as ficheLapin_service
# from sqlalchemy.orm import Session

# ficheLapin_router = APIRouter(prefix="/ficheslapin")

# @ficheLapin_router.post("/", tags=["ficheslapin"])
# async def create_fichelapin(fichelapin: serializers.FicheLapin, db: Session = Depends(database.get_db)):
#     try:
#         return ficheLapin_service.create_fichelapin(fichelapin=fichelapin, db=db)
#     except UserNotFound:
#         raise HTTPException(status_code=404, detail="User not found")
#     except FicheLapinAlreadyExists:
#         raise HTTPException(status_code=409, detail="FicheLapin already exists")



# @ficheLapin_router.get("/", tags=["ficheslapin"], response_model=list[FicheLapinWithAuthor])
# async def get_all_ficheslapin(db: Session = Depends(database.get_db)):
#     return ficheLapin_service.get_all_ficheslapin(db=db)        


# @ficheLapin_router.delete("/{fichelapin_id}", tags=["ficheslapin"])
# async def delete_fichelapin_by_id(      
#     fichelapin_id: str,
#     db: Session = Depends(database.get_db),
#     user_id: str = Depends(get_user_id),
# ):
#     try:
#         return ficheLapin_service.delete_fichelapin_by_user(
#             fichelapin_id=fichelapin_id, db=db, user_id=user_id
#         )
#     except FicheLapinNotFound:
#         raise HTTPException(status_code=404, detail="FicheLapin not found")
#     except WrongAuthor:
#         raise HTTPException(status_code=403, detail="Only author can delete their fichelapin")


# @ficheLapin_router.delete("/", tags=["ficheslapin"])
# async def delete_all_ficheslapin(db: Session = Depends(database.get_db)):
#     return ficheLapin_service.delete_all_ficheslapin(db=db)        




