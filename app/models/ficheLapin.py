from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from database import BaseSQL

class FicheLapin(BaseSQL):
    __tablename__ = "fiche_lapin"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    nom = Column(String, nullable=False)
    numero_arrivee_association = Column(Integer, nullable=False)
    date_creation_fiche = Column(DateTime, default=datetime.utcnow)
    date_arrivee_association = Column(DateTime)
    photo = Column(String)

    # Identité
    numero_identification = Column(String)
    statut_vetonac = Column(String)
    date_naissance = Column(DateTime)
    sexe = Column(String)
    poids_actuel = Column(Integer)
    poids_ideal = Column(Integer)

    # Santé
    nom_veterinaire = Column(String)
    date_sterilisation = Column(DateTime)
    date_dernier_vaccin = Column(DateTime)
    nom_dernier_vaccin = Column(String)
    date_prochain_vaccin = Column(DateTime)
    date_dernier_controle_sante = Column(DateTime)
    date_deparasitage = Column(DateTime)
    nom_deparasitage = Column(String)
    problemes_sante_connus = Column(String)
    type_litiere_actuelle = Column(String)

    # Alimentation
    type_foin = Column(String)
    marque_granules = Column(String)
    quantite_granules = Column(Integer)
    verdure_introduite = Column(String)
    quantite_verdure = Column(Integer)

    # Comportement
    caractere = Column(String)
    sociabilite_autres_lapins = Column(String)
    sociabilite_autres_animaux = Column(String)
    sociabilite_enfants = Column(String)
    proprete = Column(String)
    dynamisme = Column(String)

    auteur_id = Column(String, ForeignKey("users.id"), nullable=False)
    auteur = relationship("User", back_populates="ficheLapin")

    # posts attachés
    posts = relationship(
        "Post",
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="fiche_lapin"
    )
