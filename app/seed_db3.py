import os
import sys
from database import SessionLocal, engine, BaseSQL
from models.user import User
from models.ficheLapin import FicheLapin
from models.post import Post
from services.auth import hash_password
import uuid
from datetime import datetime, timedelta
import random

# -------------------------
# Données de génération
# -------------------------

NOMS_LAPINS = [
    "Luna", "Pixel", "Némo", "Câlin", "Moka", "Pistache", "Oréo", "Plume",
    "Caramel", "Noisette", "Biscotte", "Flocon", "Paprika", "Bounty"
]

CARACTERES = ["Calme", "Joueur", "Timide", "Curieux", "Peureux", "Très sociable", "Dominant"]
SOCIA_OPTIONS = ["Bonne", "Moyenne", "Faible"]
LITIERES = ["Chanvre", "Lin", "Granulés bois", "Papier recyclé"]
FOINS = ["Foin de Crau", "Foin de montagne", "Foin premium", "Foin bio"]
GRANULES = ["Cuni Complete", "Versele Laga", "Oxbow", "JR Farm"]
VACCINS = ["Filavac", "RHD2", "Myxo-RHD"]

SEXE = ["Mâle", "Femelle"]

# ------------------------------------------------
# Fonction utilitaire pour créer une date aléatoire
# ------------------------------------------------

def random_date(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


# -------------------------
# SEED PRINCIPAL
# -------------------------

def seed():
    print("=" * 60)
    print(" Démarrage du script de seed")
    print("=" * 60)
    
    # Créer les tables si elles n'existent pas
    print("\n Vérification des tables...")
    BaseSQL.metadata.create_all(bind=engine)
    print(" Tables vérifiées")
    
    db = SessionLocal()

    try:
        # -------------------------
        # Création d'utilisateurs
        # -------------------------
        print("\n👥 Création des utilisateurs...")

        users = []
        exemples_users = [
            ("admin", "adminpass", "admin", "Admin", "", "admin@test.fr"),
            ("camille", "camille", "fondateur", "Camille", "L", "c.l@test.fr"),
            ("cedric", "cedric", "fondateur", "Cédric", "D", "c.d@test.fr"),
            ("aurelia", "aurelia", "benevole", "Aurélia", "PESQUET", "aurelia@test.fr"),
            ("marion", "marion", "benevole", "Marion", "T", "marion@test.fr"),
        ]

        for username, pwd, role, first, last, email in exemples_users:
            existing = db.query(User).filter(User.username == username).first()
            if not existing:
                u = User(
                    id=str(uuid.uuid4()),
                    username=username,
                    password=hash_password(pwd),
                    role=role,
                    firstName=first,
                    lastName=last,
                    email=email
                )
                db.add(u)
                db.commit()
                db.refresh(u)
                users.append(u)
                print(f"   Utilisateur créé: {username} (role: {role})")
            else:
                users.append(existing)
                print(f"   Utilisateur existant: {username}")

        print(f"\n {len(users)} utilisateurs disponibles")

        #--------------------------
        # Création de la 1ere fiche lapin de référence
        #--------------------------
        print("\n Création de la fiche lapin de référence...")

        nom1 = "Kala"
        existing_kala = db.query(FicheLapin).filter(FicheLapin.nom == nom1).first()
        
        if not existing_kala:
            lapin1 = FicheLapin(
                id=str(uuid.uuid4()),
                nom=nom1,
                auteur_id=users[3].id,
                numero_arrivee_association=1,
                date_creation_fiche=datetime(2022, 4, 21),
                date_arrivee_association=datetime(2022, 4, 21),
                # photo="",
                photo = "../frontend/src/assets/Kala.jpg",
                numero_identification="ABC12345",
                statut_vetonac="À jour",
                date_naissance=datetime(2019, 5, 1),
                sexe="Femelle",
                poids_actuel=1800,
                poids_ideal=1800,
                nom_veterinaire="Claire Vincent",
                date_sterilisation=datetime(2022, 4, 26),
                date_dernier_vaccin=datetime(2025, 5, 15),
                nom_dernier_vaccin="Filavac",
                date_prochain_vaccin=datetime(2026, 5, 15),
                date_dernier_controle_sante=datetime(2025, 5, 15),
                date_deparasitage=datetime(2025, 5, 15),
                nom_deparasitage="Advantage",
                problemes_sante_connus="Aucun",
                type_litiere_actuelle="Chanvre",
                type_foin="Foin de Normandie",
                marque_granules="-",
                quantite_granules=0,
                verdure_introduite="Oui",
                quantite_verdure=170,
                caractere="Calme",
                sociabilite_autres_lapins="Bonne",
                sociabilite_autres_animaux="Inconnu",
                sociabilite_enfants="Bonne",
                proprete="Bonne",
                dynamisme="Normal"
            )
            db.add(lapin1)
            db.commit()
            db.refresh(lapin1)
            print(f"   Fiche lapin créée: {nom1}")     
        else:
            print(f"   Fiche lapin existante: {nom1}")

        # -------------------------
        # Création de 20 fiches lapins
        # -------------------------
        print("\n Création de fiches lapins supplémentaires...")
        
        fiches_created = 0

        for i in range(20):
            nom = random.choice(NOMS_LAPINS) + f"_{i}"
            existing = db.query(FicheLapin).filter(FicheLapin.nom == nom).first()
            
            if not existing:
                auteur = random.choice(users)

                lapin = FicheLapin(
                    id=str(uuid.uuid4()),
                    nom=nom,
                    auteur_id=auteur.id,
                    numero_arrivee_association=random.randint(2, 300),
                    date_creation_fiche=datetime.utcnow(),
                    date_arrivee_association=random_date(),
                    photo="",
                    numero_identification=str(uuid.uuid4())[:8],
                    statut_vetonac=random.choice(["À jour", "À contrôler", "Inconnu"]),
                    date_naissance=random_date(2018, 2023),
                    sexe=random.choice(SEXE),
                    poids_actuel=random.randint(1000, 3000),
                    poids_ideal=random.randint(1500, 2500),
                    nom_veterinaire="Clinique Lapinou",
                    date_sterilisation=random_date(2020, 2024),
                    date_dernier_vaccin=random_date(2022, 2024),
                    nom_dernier_vaccin=random.choice(VACCINS),
                    date_prochain_vaccin=datetime.utcnow() + timedelta(days=180),
                    date_dernier_controle_sante=random_date(2022, 2024),
                    date_deparasitage=random_date(2022, 2024),
                    nom_deparasitage="Advantage",
                    problemes_sante_connus=random.choice(["", "Pododermatite légère", "Surpoids", "Dents à surveiller"]),
                    type_litiere_actuelle=random.choice(LITIERES),
                    type_foin=random.choice(FOINS),
                    marque_granules=random.choice(GRANULES),
                    quantite_granules=random.randint(10, 30),
                    verdure_introduite=random.choice(["Oui", "Non", "Partiellement"]),
                    quantite_verdure=random.randint(30, 200),
                    caractere=random.choice(CARACTERES),
                    sociabilite_autres_lapins=random.choice(SOCIA_OPTIONS),
                    sociabilite_autres_animaux=random.choice(SOCIA_OPTIONS),
                    sociabilite_enfants=random.choice(SOCIA_OPTIONS),
                    proprete=random.choice(["Bonne", "Correcte", "À travailler"]),
                    dynamisme=random.choice(["Actif", "Normal", "Calme"])
                )

                db.add(lapin)
                db.commit()
                db.refresh(lapin)
                fiches_created += 1

                # -------------------------
                # Création de posts liés
                # -------------------------
                nb_posts = random.randint(1, 4)
                for j in range(nb_posts):
                    p = Post(
                        id=str(uuid.uuid4()),
                        title=f"Note {random.randint(1,100)}",
                        content=f"Observation automatique générée pour {nom}.",
                        author_id=auteur.id,
                        fiche_lapin_id=lapin.id,
                        date_creation_post=datetime.utcnow()
                    )
                    db.add(p)
                db.commit()
                
                print(f"   Fiche créée: {nom} avec {nb_posts} posts")

        print(f"\n {fiches_created} nouvelles fiches lapins créées")
        
        # -------------------------
        # Statistiques finales
        # -------------------------
        print("\n" + "=" * 60)
        print(" STATISTIQUES FINALES")
        print("=" * 60)
        
        total_users = db.query(User).count()
        total_fiches = db.query(FicheLapin).count()
        total_posts = db.query(Post).count()
        
        print(f" Utilisateurs : {total_users}")
        print(f" Fiches lapins: {total_fiches}")
        print(f" Posts        : {total_posts}")
        
        print("\n" + "=" * 60)
        print(" SEED TERMINÉ AVEC SUCCÈS !")
        print("=" * 60)

    except Exception as e:
        print(f"\n ERREUR lors du seed: {e}")
        print(f"Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    
    finally:
        db.close()


if __name__ == "__main__":
    seed()