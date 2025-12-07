from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.auth import auth_router
from routers.post import post_router
from routers.user import user_router
from routers.health import health_router
from routers.ficheLapin import ficheLapin_router
from database import BaseSQL, engine
from models import User, Post, FicheLapin
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Cycle de vie de l'application.
    Crée les tables au démarrage.
    """
    print("🚀 Démarrage de l'application...")
    print("📊 Création des tables dans la base de données...")
    
    # Créer toutes les tables
    BaseSQL.metadata.create_all(bind=engine)
    
    print("✅ Tables créées avec succès !")
    print(f"📋 Tables disponibles : {list(BaseSQL.metadata.tables.keys())}")
    
    yield
    
    print("👋 Arrêt de l'application...")


app = FastAPI(
    title="SPI LOEN - Console d'administration des fiches lapins",
    version="0.0.1",
    description="""
    API de gestion des fiches lapins pour l'association SPI LOEN.
    
    ## Authentification
    
    Pour utiliser les endpoints sécurisés :
    1. Créez un utilisateur avec POST /users/
    2. Obtenez un token avec POST /auth/token
    3. Cliquez sur le bouton "Authorize" 🔒 en haut à droite
    4. Entrez votre token (sans le préfixe "Bearer")
    5. Cliquez sur "Authorize"
    
    Vous pouvez maintenant utiliser tous les endpoints protégés !
    """,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(ficheLapin_router)

# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# from routers.auth import auth_router
# from routers.post import post_router
# from routers.user import user_router
# from routers.health import health_router
# from routers.ficheLapin import ficheLapin_router
# from database import BaseSQL, engine


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     BaseSQL.metadata.create_all(bind=engine)
#     yield


# app = FastAPI(
#     title="SPI LOEN - Console d'administration des fiches lapins",
#     version="0.0.1",
#     description="""
#     API de gestion des fiches lapins pour l'association SPI LOEN.
    
#     ## Authentification
    
#     Pour utiliser les endpoints sécurisés :
#     1. Créez un utilisateur avec POST /users/
#     2. Obtenez un token avec POST /auth/token
#     3. Cliquez sur le bouton "Authorize" 🔒 en haut à droite
#     4. Entrez votre token (sans le préfixe "Bearer")
#     5. Cliquez sur "Authorize"
    
#     Vous pouvez maintenant utiliser tous les endpoints protégés !
#     """,
#     lifespan=lifespan,
# )


# app.include_router(health_router)
# app.include_router(auth_router)
# app.include_router(user_router)
# app.include_router(post_router)
# app.include_router(ficheLapin_router)


# from fastapi import FastAPI
# from fastapi.security import HTTPBearer
# from contextlib import asynccontextmanager

# from routers.auth import auth_router
# from routers.ficheLapin import ficheLapin_router
# from routers.post import post_router
# from routers.user import user_router
# from routers.health import health_router
# from database import BaseSQL, engine
# from models import user, post, ficheLapin


# security = HTTPBearer()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     BaseSQL.metadata.create_all(bind=engine)
#     yield


# # app = FastAPI(
# #     title="SPI LOEN - Console d'aministration des fiches lapins",
# #     description="Gestion des rescapés pour l'association SPI LOEN par les bénévoles de l'association",
# #     version="0.0.1",
# #     lifespan=lifespan,
# # )


# # # 🔥 Ajouter le schéma Bearer dans la doc OpenAPI
# # app.openapi_schema = None
# # def custom_openapi():
# #     if app.openapi_schema:
# #         return app.openapi_schema
# #     openapi_schema = app.openapi()
# #     openapi_schema["components"]["securitySchemes"] = {
# #         "BearerAuth": {
# #             "type": "http",
# #             "scheme": "bearer",
# #             "bearerFormat": "JWT",
# #         }
# #     }
# #     openapi_schema["security"] = [{"BearerAuth": []}]
# #     app.openapi_schema = openapi_schema
# #     return app.openapi_schema

# #app.openapi = custom_openapi

# from fastapi.openapi.utils import get_openapi

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title="SPI LOEN - Console d'administration des fiches lapins",
#         version="0.0.1",
#         description="Gestion des rescapés pour l'association SPI LOEN",
#         routes=app.routes,
#     )

#     # Ajout de la sécurité globale
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }
#     }

#     openapi_schema["security"] = [{"BearerAuth": []}]

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi



# app.include_router(ficheLapin_router)
# app.include_router(post_router)
# app.include_router(user_router)
# app.include_router(auth_router)
# app.include_router(health_router)


# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from database import BaseSQL, engine
# from models import user, post, ficheLapin
# from routers.auth import auth_router
# from routers.ficheLapin import ficheLapin_router
# from routers.post import post_router
# from routers.user import user_router
# from routers.health import health_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # maintenant que les modèles sont importés, create_all() créera les tables
#     BaseSQL.metadata.create_all(bind=engine)
#     yield

# app = FastAPI(
#     title="SPI LOEN - Console d'administration des fiches lapins",
#     description="Gestion des rescapés pour l'association SPI LOEN",
#     version="0.0.1",
#     lifespan=lifespan,
# )

# # include routers...
# app.include_router(ficheLapin_router)
# app.include_router(post_router)
# app.include_router(user_router)
# app.include_router(auth_router)
# app.include_router(health_router)



# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# from routers.auth import auth_router
# from routers.post import post_router
# from routers.user import user_router
# from routers.health import health_router
# from routers.ficheLapin import ficheLapin_router
# from database import BaseSQL, engine


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     BaseSQL.metadata.create_all(bind=engine)
#     yield


# app = FastAPI(
#     title="SPI LOEN - Console d'administration des fiches lapins",
#     version="0.0.1",
#     lifespan=lifespan,
# )


# app.include_router(post_router)
# app.include_router(user_router)
# app.include_router(auth_router)
# app.include_router(health_router)
# app.include_router(ficheLapin_router)





