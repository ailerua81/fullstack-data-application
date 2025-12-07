import os
from database import SessionLocal, engine, BaseSQL
from models.user import User
from models.ficheLapin import FicheLapin
from models.post import Post
from services.auth import hash_password
import uuid
from datetime import datetime

def seed():
    BaseSQL.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # user admin
        if not db.query(User).filter(User.username=="admin").first():
            # Ajout d'un utilisateur admin
            admin = User(id=str(uuid.uuid4()), username="admin", password=hash_password("adminpass"), role="admin", firstName="Admin")
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Admin created:", admin.username)
        # Ajout d'un utilisateur bénévole
        benevole1 = User(id=str(uuid.uuid4()), username="aurelia", password=hash_password("aurelia"), role="benevole", firstName="Aurélia", lastName="PESQUET", email="aurelia.pesquet@edu.esiee.fr")
        db.add(benevole1)
        db.commit() 
        db.refresh(benevole1)
        print("Benevole created:", benevole1.username)

        # Ajout d'un utilisateur fondateur
        fondateur1 = User(id=str(uuid.uuid4()), username="camille", password=hash_password("camille"), role="fondateur", firstName="Camille", lastName="L") 
        db.add(fondateur1)
        db.commit() 
        db.refresh(fondateur1)
        print("Fondateur created:", fondateur1.username)

        # Ajout d'un utilisateur fondateur
        fondateur2 = User(id=str(uuid.uuid4()), username="cedric", password=hash_password("cedric"), role="fondateur", firstName="Cédric", lastName="D") 
        db.add(fondateur2)
        db.commit() 
        db.refresh(fondateur2)
        print("Fondateur created:", fondateur2.username)

        # Ajout d'une fiche 
        fondateur = db.query(User).filter(User.username=="cedric").first()
        if fondateur and not db.query(FicheLapin).filter(FicheLapin.nom=="Kala").first():
            f = FicheLapin(
                nom="Kala", 
                auteur_id=fondateur.id, 
                numero_arrivee_association=32,
                date_creation_fiche=datetime.utcnow(),
                date_arrivee_association=datetime(2022,4,21),
                sexe="Femelle", 
                poids_actuel=2)
            db.add(f)
            db.commit()
            print("Sample fiche created")



        # Ajout d'un post lié à la fiche 
        fondateur = db.query(User).filter(User.username=="cedric").first()
        if fondateur and not db.query(Post).filter(Post.title=="Arrivée").first():
            note = Post(
                title="Arrivée", 
                author_id=fondateur.id, 
                content="Kala est arrivée aujourd'hui à l'association. C'est une lapine très douce et sociable.",
                date_creation_post=datetime.utcnow(),
                fiche_lapin_id=f.id)
            db.add(note)
            db.commit()
            print("Post created")    
    finally:
        db.close()

if __name__ == "__main__":
    seed()
