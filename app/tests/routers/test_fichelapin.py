"""
Tests pour le router de fiches lapin
Couvre les opérations CRUD et les règles métier
"""

import pytest
import jwt
import os
from datetime import datetime
from models import FicheLapin, User


@pytest.fixture
def auth_token(test_user):
    """Fixture pour générer un token JWT valide pour l'utilisateur de test"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
    JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")
    return jwt.encode(
        {"user_id": str(test_user.id)},
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )


@pytest.fixture
def test_user_2(test_db_session):
    """Fixture pour un second utilisateur de test"""
    from services.auth import hash_password

    user = User(username="testuser2", password=hash_password("testpassword2"))
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    yield user
    test_db_session.delete(user)
    test_db_session.commit()


@pytest.fixture
def auth_token_user_2(test_user_2):
    """Fixture pour générer un token JWT valide pour le second utilisateur"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
    JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")
    return jwt.encode(
        {"user_id": str(test_user_2.id)},
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )


@pytest.fixture
def test_fiche_lapin(test_db_session, test_user):
    """Fixture pour créer une fiche lapin de test"""
    fiche = FicheLapin(
        nom="Pompon",
        numero_arrivee_association=1,
        date_creation_fiche=datetime.now(),
        date_arrivee_association=datetime.now(),
        numero_identification="250269123456789",
        sexe="M",
        poids_actuel=2000,
        auteur_id=test_user.id
    )
    test_db_session.add(fiche)
    test_db_session.commit()
    test_db_session.refresh(fiche)
    fiche_id = fiche.id
    yield fiche
    # Cleanup
    existing_fiche = test_db_session.query(FicheLapin).filter(FicheLapin.id == fiche_id).first()
    if existing_fiche:
        test_db_session.delete(existing_fiche)
        test_db_session.commit()


# ============================================================================
# TESTS CREATE (POST)
# ============================================================================

def test_create_fiche_lapin_success(client, test_db_session, test_user, auth_token):
    """
    Test de création d'une fiche lapin avec succès
    
    Scénario: Utilisateur authentifié crée une nouvelle fiche
    Résultat attendu: Fiche créée avec status 201
    """
    # Arrange
    fiche_data = {
        "nom": "Caramel",
        "numero_arrivee_association": 2,
        "sexe": "F",
        "poids_actuel": 1800,
        "numero_identification": "250269987654321",
        "date_creation_fiche": datetime.now().isoformat(),
        "date_arrivee_association": datetime.now().isoformat(),
        "auteur_id": str(test_user.id)
    }
    
    # Act
    response = client.post(
        "/ficheslapin/",
        json=fiche_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Caramel"
    assert data["sexe"] == "F"
    assert data["auteur_id"] == str(test_user.id)
    assert data["numero_identification"] == "250269987654321"
    assert data["poids_actuel"] == 1800 
    assert data["numero_arrivee_association"] == 2
    assert data["date_creation_fiche"] is not None
    assert data["date_arrivee_association"] is not None 


    # Vérifier en base de données
    created_fiche = test_db_session.query(FicheLapin).filter(
        FicheLapin.nom == "Caramel"
    ).first()
    assert created_fiche is not None
    
    # Cleanup
    test_db_session.delete(created_fiche)
    test_db_session.commit()


def test_create_fiche_lapin_unauthorized(client):
    """
    Test de création sans authentification
    
    Scénario: Tentative de création sans token
    Résultat attendu: Erreur 422 (missing required header)
    """
    # Arrange
    fiche_data = {
        "nom": "Flocon",
        "numero_arrivee_association": 3,
        "sexe": "M"
    }
    
    # Act
    response = client.post("/ficheslapin/", json=fiche_data)
    
    # Assert
    assert response.status_code == 403



def test_create_fiche_lapin_invalid_token(client):
    """
    Test de création avec token invalide
    
    Scénario: Token JWT invalide
    Résultat attendu: Erreur 401
    """
    # Arrange
    fiche_data = {
        "nom": "Noisette",
        "numero_arrivee_association": 4
    }
    
    # Act
    response = client.post(
        "/ficheslapin/",
        json=fiche_data,
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    # Assert
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]




def test_create_fiche_lapin_missing_required_fields(client, auth_token):
    """
    Test de création avec champs obligatoires manquants
    
    Scénario: Données incomplètes
    Résultat attendu: Erreur 422 (validation error)
    """
    # Arrange
    incomplete_data = {
        "sexe": "M"
        # nom manquant (si requis)
    }
    
    # Act
    response = client.post(
        "/ficheslapin/",
        json=incomplete_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 422


# ============================================================================
# TESTS READ (GET)
# ============================================================================

def test_get_all_fiches_lapin_success(client, test_db_session, test_user, auth_token, test_fiche_lapin):
    """
    Test de récupération de toutes les fiches
    
    Scénario: Utilisateur authentifié récupère ses fiches
    Résultat attendu: Liste de fiches avec status 200
    """
    # Act
    response = client.get(
        "/ficheslapin/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(fiche["nom"] == "Pompon" for fiche in data)


def test_get_fiche_lapin_by_id_success(client, auth_token, test_fiche_lapin):
    """
    Test de récupération d'une fiche par ID
    Scénario: Récupération d'une fiche existante
    Résultat attendu: Fiche avec status 200
    """
    # Arrange
    fiche_id = test_fiche_lapin.id
    
    # Act
    response = client.get(
        f"/ficheslapin/{fiche_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(fiche_id)
    assert data["nom"] == "Pompon"


def test_get_fiche_lapin_not_found(client, auth_token):
    """
    Test de récupération d'une fiche inexistante
    
    Scénario: ID n'existe pas
    Résultat attendu: Erreur 404
    """
    # Arrange
    fake_id = "00000000-0000-0000-0000-000000000000"
    
    # Act
    response = client.get(
        f"/ficheslapin/{fake_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Fiche lapin not found"}


def test_get_fiches_lapin_unauthorized(client):
    """
    Test de récupération sans authentification
    
    Scénario: Pas de token fourni
    Résultat attendu: Erreur 422
    """
    # Act
    response = client.get("/ficheslapin")
    
    # Assert
    assert response.status_code == 403



# ============================================================================
# TESTS UPDATE (PUT/PATCH)
# ============================================================================

def test_update_fiche_lapin_success(client, test_db_session, test_user, auth_token, test_fiche_lapin):

    fiche_id = test_fiche_lapin.id
    update_data = {
        "poids_actuel": 2200,
        "caractere": "Sociable et joueur"
    }

    response = client.put(
        f"/ficheslapin/{fiche_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200

    updated_fiche = test_db_session.query(FicheLapin).filter(
        FicheLapin.id == fiche_id
    ).first()

    # Force SQLAlchemy to reload fresh values
    test_db_session.refresh(updated_fiche)

    assert updated_fiche.poids_actuel == 2200
    assert updated_fiche.caractere == "Sociable et joueur"




def test_update_fiche_lapin_forbidden_wrong_author(
    client, test_db_session, test_user_2, auth_token_user_2, test_fiche_lapin
):
    """
    Test de mise à jour par un utilisateur non-auteur
    
    Scénario: Utilisateur tente de modifier une fiche d'un autre
    Résultat attendu: Erreur 403 (Forbidden)
    """
    # Arrange
    fiche_id = test_fiche_lapin.id
    update_data = {"poids_actuel": 2500}
    
    # Act
    response = client.put(
        f"/ficheslapin/{fiche_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token_user_2}"}
    )
    
    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "Only author can update their fiche"}


def test_update_fiche_lapin_not_found(client, auth_token):
    """
    Test de mise à jour d'une fiche inexistante
    
    Scénario: ID n'existe pas
    Résultat attendu: Erreur 404
    """
    # Arrange
    fake_id = "00000000-0000-0000-0000-000000000000"
    update_data = {"nom": "Nouveau nom"}
    
    # Act
    response = client.put(
        f"/ficheslapin/{fake_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Fiche lapin not found"}


# ============================================================================
# TESTS DELETE
# ============================================================================

def test_delete_fiche_lapin_success(client, test_db_session, test_user, auth_token, test_fiche_lapin):
    """
    Test de suppression d'une fiche par son auteur
    
    Scénario: Auteur supprime sa propre fiche
    Résultat attendu: Fiche supprimée avec status 200
    """
    # Arrange
    fiche_id = test_fiche_lapin.id
    
    # Act
    response = client.delete(
        f"/ficheslapin/{fiche_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(fiche_id)
    
    # Vérifier suppression en base
    deleted_fiche = test_db_session.query(FicheLapin).filter(
        FicheLapin.id == fiche_id
    ).first()
    assert deleted_fiche is None



def test_delete_fiche_lapin_not_found(client, auth_token):
    """
    Test de suppression d'une fiche inexistante
    
    Scénario: ID n'existe pas
    Résultat attendu: Erreur 404
    """
    # Arrange
    fake_id = "00000000-0000-0000-0000-000000000000"
    
    # Act
    response = client.delete(
        f"/ficheslapin/{fake_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Fiche lapin not found"}


def test_delete_fiche_lapin_cascade_posts(client, test_db_session, test_user, auth_token, test_fiche_lapin):
    """
    Test de suppression en cascade des posts liés
    
    Scénario: Suppression d'une fiche avec posts associés
    Résultat attendu: Fiche et posts supprimés
    """
    from models import Post
    
    # Arrange - créer un post lié à la fiche
    post = Post(
        title="Update sur Pompon",
        content="Il va bien !",
        author_id=test_user.id,
        fiche_lapin_id=test_fiche_lapin.id,
        date_creation_post=datetime.now()
    )
    test_db_session.add(post)
    test_db_session.commit()
    post_id = post.id
    
    # Act - supprimer la fiche
    response = client.delete(
        f"/ficheslapin/{test_fiche_lapin.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Vérifier que le post a aussi été supprimé (cascade)
    deleted_post = test_db_session.query(Post).filter(Post.id == post_id).first()
    assert deleted_post is None


# ============================================================================
# TESTS VALIDATION MÉTIER
# ============================================================================

def test_create_fiche_lapin_poids_validation(client, auth_token):
    """
    Test de validation du poids
    
    Scénario: Poids négatif ou trop élevé
    Résultat attendu: Erreur de validation
    """
    # Arrange
    invalid_data = {
        "nom": "TestPoids",
        "numero_arrivee_association": 10,
        "poids_actuel": -100  # Poids négatif
    }
    
    # Act
    response = client.post(
        "/ficheslapin",
        json=invalid_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code in [400, 422]


def test_create_fiche_lapin_sexe_validation(client, auth_token):
    """
    Test de validation du sexe
    
    Scénario: Sexe invalide (ni M ni F)
    Résultat attendu: Erreur de validation
    """
    # Arrange
    invalid_data = {
        "nom": "TestSexe",
        "numero_arrivee_association": 11,
        "sexe": "X"  # Valeur invalide
    }
    
    # Act
    response = client.post(
        "/ficheslapin",
        json=invalid_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert
    assert response.status_code in [400, 422]


def test_get_fiches_lapin_filtered_by_author(
    client, test_db_session, test_user, test_user_2, auth_token, auth_token_user_2
):
    """
    Test que chaque utilisateur voit uniquement ses fiches
    
    Scénario: Deux utilisateurs avec leurs propres fiches
    Résultat attendu: Chacun voit seulement ses fiches
    """
    # Arrange - créer une fiche pour user_2
    fiche_user_2 = FicheLapin(
        nom="FicheUser2",
        numero_arrivee_association=20,
        auteur_id=test_user_2.id,
        date_creation_fiche=datetime.now()
    )
    test_db_session.add(fiche_user_2)
    test_db_session.commit()
    
    # Act - user 1 récupère ses fiches
    response_user_1 = client.get(
        "/ficheslapin",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Assert - user 1 ne voit pas les fiches de user 2
    assert response_user_1.status_code == 200  # Vérifier d'abord le status
    data_user_1 = response_user_1.json()
    assert isinstance(data_user_1, list)  # Vérifier que c'est une liste
    assert not any(fiche["nom"] == "FicheUser2" for fiche in data_user_1)
    
    # Cleanup
    test_db_session.delete(fiche_user_2)
    test_db_session.commit()