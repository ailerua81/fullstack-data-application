import os
from database import SessionLocal, engine, BaseSQL
from models.user import User
from models.ficheLapin import FicheLapin
from models.post import Post
from services.auth import hash_password
import uuid
from datetime import datetime


def seed():
    # Création des tables
    BaseSQL.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # -------------------------
        # Création des utilisateurs
        # -------------------------

        # Admin
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                id=str(uuid.uuid4()),
                username="admin",
                password=hash_password("adminpass"),
                role="admin",
                firstName="Admin",
                lastName="",
                email=""
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Admin created:", admin.username)

        # Bénévole
        benevole1 = User(
            id=str(uuid.uuid4()),
            username="aurelia",
            password=hash_password("aurelia"),
            role="benevole",
            firstName="Aurélia",
            lastName="PESQUET",
            email="aurelia.pesquet@edu.esiee.fr"
        )
        db.add(benevole1)
        db.commit()
        db.refresh(benevole1)
        print("Benevole created:", benevole1.username)

        # Fondateur 1
        fondateur1 = User(
            id=str(uuid.uuid4()),
            username="camille",
            password=hash_password("camille"),
            role="fondateur",
            firstName="Camille",
            lastName="L",
            email=""
        )
        db.add(fondateur1)
        db.commit()
        db.refresh(fondateur1)
        print("Fondateur created:", fondateur1.username)

        # Fondateur 2
        fondateur2 = User(
            id=str(uuid.uuid4()),
            username="cedric",
            password=hash_password("cedric"),
            role="fondateur",
            firstName="Cédric",
            lastName="D",
            email=""
        )
        db.add(fondateur2)
        db.commit()
        db.refresh(fondateur2)
        print("Fondateur created:", fondateur2.username)

        # ------------------------------------
        # Création d'une fiche lapin d'exemple
        # ------------------------------------

        fondateur = db.query(User).filter(User.username == "cedric").first()
        if fondateur and not db.query(FicheLapin).filter(FicheLapin.nom == "Kala").first():
            fiche = FicheLapin(
                id=str(uuid.uuid4()),
                nom="Kala",
                auteur_id=fondateur.id,
                numero_arrivee_association=32,
                date_creation_fiche=datetime.utcnow(),
                date_arrivee_association=datetime(2022, 4, 21),
                photo="",
                numero_identification="",
                statut_vetonac="",
                date_naissance=None,
                sexe="Femelle",
                poids_actuel=2,
                poids_ideal=None,
                nom_veterinaire="",
                date_sterilisation=None,
                date_dernier_vaccin=None,
                nom_dernier_vaccin="",
                date_prochain_vaccin=None,
                date_dernier_controle_sante=None,
                date_deparasitage=None,
                nom_deparasitage="",
                problemes_sante_connus="",
                type_litiere_actuelle="",
                type_foin="",
                marque_granules="",
                quantite_granules=None,
                verdure_introduite="",
                quantite_verdure=None,
                caractere="",
                sociabilite_autres_lapins="",
                sociabilite_autres_animaux="",
                sociabilite_enfants="",
                proprete="",
                dynamisme=""
            )
            db.add(fiche)
            db.commit()
            db.refresh(fiche)
            print("Sample fiche created")

        # -------------------------
        # Post lié à la fiche Kala
        # -------------------------

        if fondateur and not db.query(Post).filter(Post.title == "Arrivée").first():
            fiche_kala = db.query(FicheLapin).filter(FicheLapin.nom == "Kala").first()

            post = Post(
                id=str(uuid.uuid4()),
                title="Arrivée",
                author_id=fondateur.id,
                content="Kala est arrivée aujourd'hui à l'association. C'est une lapine très douce et sociable.",
                date_creation_post=datetime.utcnow(),
                fiche_lapin_id=fiche_kala.id if fiche_kala else None
            )
            db.add(post)
            db.commit()
            print("Post created")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
