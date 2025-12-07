from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth import decode_jwt

# Schéma de sécurité HTTP Bearer pour Swagger UI
bearer_scheme = HTTPBearer(
    scheme_name="Bearer Token",
    description="Entrez votre token JWT (sans le préfixe 'Bearer')"
)


def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    """
    Extrait et valide l'ID utilisateur depuis le token JWT.
    
    Args:
        credentials: Les credentials HTTP Bearer extraits du header Authorization
        
    Returns:
        str: L'ID de l'utilisateur authentifié
        
    Raises:
        HTTPException: Si le token est invalide ou expiré
    """
    try:
        token = credentials.credentials
        payload = decode_jwt(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_id missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id
    
    except HTTPException:
        # Re-lever les HTTPException de decode_jwt (token expiré, invalide, etc.)
        raise
    
    except Exception as e:
        # Gérer toute autre erreur inattendue
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )