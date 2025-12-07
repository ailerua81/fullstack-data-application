"""
Schémas Pydantic pour les fiches lapin
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from serializers import User


class FicheLapin(BaseModel):
    """Schéma de base pour une fiche lapin"""
    model_config = ConfigDict(from_attributes=True)

    nom: str
    auteur_id: str
    numero_arrivee_association: int
    date_creation_fiche: datetime
    date_arrivee_association: Optional[datetime] = None
    photo: Optional[str] = None
     
    numero_identification: Optional[str] = None
    statut_vetonac: Optional[str] = None
    date_naissance: Optional[datetime] = None
    sexe: Optional[str] = None
    poids_actuel: Optional[int] = None
    poids_ideal: Optional[int] = None

    nom_veterinaire: Optional[str] = None
    date_sterilisation: Optional[datetime] = None
    date_dernier_vaccin: Optional[datetime] = None
    nom_dernier_vaccin: Optional[str] = None
    date_prochain_vaccin: Optional[datetime] = None
    date_dernier_controle_sante: Optional[datetime] = None
    nom_deparasitage: Optional[str] = None
    problemes_sante_connus: Optional[str] = None
    type_litiere_actuelle: Optional[str] = None

    type_foin: Optional[str] = None
    marque_granules: Optional[str] = None
    quantite_granules: Optional[int] = None
    verdure_introduite: Optional[str] = None
    quantite_verdure: Optional[int] = None

    caractere: Optional[str] = None
    sociabilite_autres_lapins: Optional[str] = None
    sociabilite_autres_animaux: Optional[str] = None
    sociabilite_enfants: Optional[str] = None
    proprete: Optional[str] = None
    dynamisme: Optional[str] = None



class FicheLapinCreate(FicheLapin):

    nom: str 
    numero_arrivee_association: int 

class FicheLapinUpdate(FicheLapin):
    pass

class FicheLapinWithAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nom: str
    auteur_id: str
    numero_arrivee_association: int
    date_creation_fiche: datetime
    date_arrivee_association: Optional[datetime] = None
    photo: Optional[str] = None
     
    numero_identification: Optional[str] = None
    statut_vetonac: Optional[str] = None
    date_naissance: Optional[datetime] = None
    sexe: Optional[str] = None
    poids_actuel: Optional[int] = None
    poids_ideal: Optional[int] = None

    nom_veterinaire: Optional[str] = None
    date_sterilisation: Optional[datetime] = None
    date_dernier_vaccin: Optional[datetime] = None
    nom_dernier_vaccin: Optional[str] = None
    date_prochain_vaccin: Optional[datetime] = None
    date_dernier_controle_sante: Optional[datetime] = None
    date_deparasitage: Optional[datetime] = None
    nom_deparasitage: Optional[str] = None
    problemes_sante_connus: Optional[str] = None
    type_litiere_actuelle: Optional[str] = None

    type_foin: Optional[str] = None
    marque_granules: Optional[str] = None
    quantite_granules: Optional[int] = None
    verdure_introduite: Optional[str] = None
    quantite_verdure: Optional[int] = None

    caractere: Optional[str] = None
    sociabilite_autres_lapins: Optional[str] = None
    sociabilite_autres_animaux: Optional[str] = None
    sociabilite_enfants: Optional[str] = None
    proprete: Optional[str] = None
    dynamisme: Optional[str] = None
    auteur: User

    model_config = {
        "from_attributes": True  
    }

class FicheLapinOutput(FicheLapin):
    id: str
    auteur_id: str

    model_config = {
        "from_attributes": True  
    }

        