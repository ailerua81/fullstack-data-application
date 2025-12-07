
#  SPI LOEN - Console d'Administration des Fiches Lapins

> Application web full-stack de gestion des fiches lapins pour l'association SPI LOEN
---

##  Table des matières

- [Choix du sujet](#-choix-du-sujet)
- [Architecture](#-architecture)
- [Technologies utilisées](#-technologies-utilisées)
- [Fonctionnalités implémentées](#-fonctionnalités-implémentées)
- [Installation et déploiement](#-installation-et-déploiement)
- [Structure du projet](#-structure-du-projet)
- [Implémentation technique](#-implémentation-technique)
- [Difficultés rencontrées](#-difficultés-rencontrées)
- [Pistes d'amélioration](#-pistes-damélioration)
- [Tests](#-tests)

---

##  Choix du sujet

### Contexte

Le projet consiste en une console d'administration complète pour la gestion des fiches lapins d'une association de protection animale (SPI LOEN) pour laquelle je travaille en tant que bénévole. Ce choix de sujet a été motivé par plusieurs facteurs :

### Motivations

1. **Cas d'usage réel et concret** : Les associations de protection animale ont réellement besoin d'outils de gestion pour suivre les animaux recueillis, leur santé, leur comportement et leur parcours. SPILOEN utilise actuellement Trello pour gérer les taches mais les membres ne sont pas pleinement satisfaits par cet outil.

2. **Complexité adaptée** : Le sujet permet d'implémenter toutes les exigences du projet (authentification, CRUD complet, relations entre entités) tout en restant accessible et compréhensible.

3. **Richesse des données** : Les fiches lapins contiennent de nombreuses informations (identité, santé, alimentation, comportement) permettant de travailler avec des modèles de données riches et des formulaires complexes.

4. **Créativité dans le design** : Le thème "lapins" offre des possibilités créatives pour le design de l'interface (icônes, couleurs, illustrations).

### Objectifs

- Créer une application professionnelle et utilisable en production
- Démontrer la maîtrise du développement full-stack (backend API REST + frontend moderne)
- Implémenter toutes les bonnes pratiques de développement web
- Fournir une expérience utilisateur optimale et intuitive

---

##  Architecture

### Architecture globale

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│                 │      │                  │      │                 │
│   Frontend      │─────▶│   Backend API    │─────▶│   PostgreSQL    │
│   React + Vite  │◀─────│   FastAPI        │◀─────│   Database      │
│                 │      │                  │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
     Port 3000                Port 5001                  Port 5432
```

### Stack technique complète

**Backend**
- **Framework** : FastAPI (Python)
- **ORM** : SQLAlchemy
- **Base de données** : PostgreSQL
- **Authentification** : JWT (PyJWT) avec PBKDF2-HMAC-SHA256
- **Validation** : Pydantic
- **Tests** : pytest, pytest-cov, httpx

**Frontend**
- **Framework** : React 18
- **Build tool** : Vite
- **Styling** : Tailwind CSS 3
- **Icônes** : Lucide React
- **HTTP Client** : Fetch API

**Infrastructure**
- **Containerisation** : Docker + Docker Compose
- **Base de données** : PostgreSQL (image officielle)
- **Reverse proxy** : Nginx (en production)

---

##  Technologies utilisées

### Backend (FastAPI)

#### Pourquoi FastAPI ?

1. **Performance** : FastAPI est l'un des frameworks Python les plus rapides
2. **Documentation automatique** : Génération automatique de Swagger UI
3. **Validation des données** : Intégration native avec Pydantic
4. **Async natif** : Support complet de l'asynchrone
5. **Type hints** : Utilisation complète du typage Python

#### Dépendances principales

```python
fastapi==0.100+        # Framework web
sqlalchemy==2.0+       # ORM
pydantic==2.0+         # Validation des données
psycopg2==2.9+         # Driver PostgreSQL
pyjwt==2.8+            # Gestion JWT
pytest==7.4+           # Framework de tests
```

### Frontend (React + Vite)

#### Pourquoi React avec Vite ?

1. **Vite** : Build ultra-rapide et hot-reload instantané
2. **React** : Bibliothèque mature avec un vaste écosystème
3. **Composants** : Architecture modulaire et réutilisable
4. **Hooks** : Gestion d'état moderne et élégante

#### Dépendances principales

```json
{
  "react": "^18.2.0",
  "lucide-react": "^0.294.0",
  "tailwindcss": "^3.4.1"
}
```

---

##  Fonctionnalités implémentées

### 1. Authentification et autorisation 

- **JWT sécurisé** avec expiration (30 minutes)
- **Hachage PBKDF2-HMAC-SHA256** des mots de passe (600 000 itérations)
- **Middleware d'authentification** avec HTTPBearer
- **Gestion des rôles** : admin, fondateur, bénévole, anonyme
- **Session persistante** avec localStorage

### 2. Gestion des utilisateurs 

- Création d'utilisateurs avec validation
- Liste de tous les utilisateurs
- Suppression d'utilisateurs
- Informations complètes (username, nom, prénom, email, rôle)

### 3. Gestion des fiches lapins 

**CRUD complet** :
-  **Create** : Création de fiches avec formulaire détaillé
-  **Read** : Liste paginée + détail complet
-  **Update** : Modification de fiches (par l'auteur uniquement)
-  **Delete** : Suppression sécurisée (par l'auteur uniquement)

**Champs gérés (35+ champs)** :
- **Identité** : nom, numéro, sexe, dates, poids, identification
- **Santé** : vétérinaire, vaccins, stérilisation, déparasitage, litière
- **Alimentation** : foin, granulés, verdure
- **Comportement** : caractère, sociabilité, propreté, dynamisme

### 4. Gestion des posts 

- Posts liés aux fiches lapins (relation 1-N)
- Suppression en cascade
- Association post-fiche-auteur

### 5. Interface utilisateur moderne 

**Design** :
-  Palette de couleurs : (tons verts/nature)
-  Dégradés et effets glassmorphism
-  Animations fluides et micro-interactions
-  Design 100% responsive (mobile, tablette, desktop)

**Fonctionnalités UX** :
-  Recherche en temps réel
-  Affichage des photos des lapins
-  Modal de détail avec toutes les informations (à compléter avec toutes les informations du backend)
-  Indicateurs de chargement
-  Messages de succès/erreur
-  Navigation intuitive

### 6. Sécurité 

- **Validation des entrées** (backend + frontend)
- **Protection CSRF** via JWT
- **Gestion des erreurs HTTP** appropriée (400, 401, 403, 404, 500)
- **Autorisation par ressource** (seul l'auteur peut modifier/supprimer)
- **Headers de sécurité** (CORS configuré)

### 7. Docker et déploiement 

- **Dockerfile** pour le backend (image multi-stage possible)
- **Docker Compose** avec 3 services :
  - `api` : Backend FastAPI
  - `db` : PostgreSQL avec healthcheck
  - `seed` : Script de seed automatique
- **Volumes persistants** pour les données
- **Healthchecks** et dépendances entre services

### 8. Script de seed 

- Création automatique de 5 utilisateurs de test
- Génération de 20+ fiches lapins avec données réalistes
- Posts automatiques associés
- Données variées (noms, caractères, poids, dates, etc.)

### 9. Tests automatisés 

- **Tests unitaires** avec pytest
- **Coverage** avec pytest-cov
- **Tests d'intégration** :
  - Routes d'authentification
  - CRUD des fiches
  - CRUD des posts
  - Autorisations et erreurs
- **CI/CD ready** avec service tests dans Docker Compose

---

##  Installation et déploiement

### Prérequis

- Docker Desktop 4.0+
- Docker Compose 2.0+
- Git
- (Optionnel) Node.js 18+ pour développement frontend local

### Installation rapide

```bash
# 1. Cloner le repository
git clone https://github.com/ailerua81/fullstack-data-application.git
cd projet

# 2. Configurer les variables d'environnement
cd app
cp .env.example .env
# Modifier les credentials dans .env si nécessaire

# 3. Lancer l'application complète
docker-compose up -d

# 4. Attendre que tout démarre (30 secondes)
# Le seed se lance automatiquement

# 5. Accéder à l'application
# Backend API : http://localhost:5001/docs
# Frontend : http://localhost:3000
```

### Installation détaillée

#### Backend

```bash
cd app

# Créer l'environnement virtuel (optionnel, pour dev local)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer avec Docker
docker-compose up -d
```

#### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer en développement
npm run dev

# Build de production
npm run build
```

### Comptes de test

Après le seed automatique, utilisez ces comptes :

| Username | Password  | Rôle      |
|----------|-----------|-----------|
| admin    | adminpass | admin     |
| camille  | camille   | fondateur |
| cedric   | cedric    | fondateur |
| aurelia  | aurelia   | benevole  |
| marion   | marion    | benevole  |

---

## 📁 Structure du projet

```
projet/
├── app/                          # Backend FastAPI
│   ├── models/                   # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py              # Modèle User
│   │   ├── post.py              # Modèle Post
│   │   └── ficheLapin.py        # Modèle FicheLapin
│   │
│   ├── serializers/             # Schémas Pydantic
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── ficheLapin.py
│   │   └── auth_token.py
│   │
│   ├── routers/                 # Endpoints API
│   │   ├── auth.py              # Authentification
│   │   ├── user.py              # Gestion utilisateurs
│   │   ├── post.py              # Gestion posts
│   │   ├── ficheLapin.py        # Gestion fiches lapins
│   │   ├── health.py            # Health checks
│   │   └── utils.py             # Middleware JWT
│   │
│   ├── services/                # Logique métier
│   │   ├── auth.py              # JWT + hashing
│   │   ├── user.py
│   │   ├── posts.py
│   │   └── ficheLapin.py
│   │
│   ├── exceptions/              # Exceptions personnalisées
│   │   ├── user.py
│   │   ├── post.py
│   │   └── ficheLapin.py
│   │
│   ├── tests/                   # Tests automatisés
│   │   ├── conftest.py          # Configuration pytest
│   │   ├── routers/
│   │   │   ├── test_auth.py
│   │   │   ├── test_post.py
│   │   │   └── test_ficheLapin.py
│   │   └── services/
│   │
│   ├── main.py                  # Point d'entrée FastAPI
│   ├── database.py              # Configuration SQLAlchemy
│   ├── seed_db3.py              # Script de seed
│   ├── requirements.txt         # Dépendances Python
│   ├── Dockerfile               # Image Docker backend
│   ├── docker-compose.yml       # Orchestration
│   ├── .env                     # Variables d'environnement
│   └── README.md                # Ce fichier
│
└── frontend/                    # Frontend React
    ├── public/
    │   ├── index.html
    │   └── photos/              # Photos des lapins
    │
    ├── src/
    │   ├── assets/              # Images (logo, etc.)
    │   ├── components/          # Composants React (si séparés)
    │   ├── services/
    │   │   └── api.js           # Service API
    │   ├── App.jsx              # Composant principal
    │   ├── main.jsx             # Point d'entrée
    │   └── index.css            # Styles globaux
    │
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── Dockerfile               # Image Docker frontend
```

---

##  Implémentation technique

### Architecture Backend

#### 1. Modèles SQLAlchemy

Les modèles utilisent SQLAlchemy ORM avec :
- **UUID** pour les clés primaires (sécurité)
- **Relations** explicites (User ↔ FicheLapin ↔ Post)
- **Cascade** pour la suppression en cascade
- **Timestamps** automatiques

Exemple de relation :
```python
class FicheLapin(BaseSQL):
    auteur_id = Column(String, ForeignKey("users.id"), nullable=False)
    auteur = relationship("User", back_populates="ficheLapin")
    
    posts = relationship(
        "Post",
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="fiche_lapin"
    )
```

#### 2. Authentification JWT

**Hachage des mots de passe** :
```python
def hash_password(password: str, iterations: int = 600_000) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt_b64}${hash_b64}"
```

**Génération JWT** :
```python
def _encode_jwt(user: User) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "user_id": str(user.id),
        "role": user.role,
        "exp": expiration,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
```

#### 3. Middleware d'authentification

```python
def get_user_id(credentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_jwt(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401)
    return user_id
```

#### 4. Gestion des erreurs

Exceptions personnalisées + HTTPException :
```python
try:
    fiche = get_fiche(id)
except FicheLapinNotFound:
    raise HTTPException(status_code=404, detail="Fiche not found")
except WrongAuthor:
    raise HTTPException(status_code=403, detail="Only author can modify")
```

### Architecture Frontend

#### 1. Service API centralisé

```javascript
class ApiService {
  async request(endpoint, options = {}) {
    const token = this.getToken();
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
    };
    const response = await fetch(`${API_URL}${endpoint}`, config);
    // Gestion erreurs...
    return response.json();
  }
}
```

#### 2. Gestion d'état React

Utilisation de **React Hooks** :
- `useState` pour l'état local
- `useEffect` pour les effets de bord
- localStorage pour la persistance du token

#### 3. Design system avec Tailwind

Classes utilitaires pour un design cohérent :
```javascript
className="bg-gradient-to-r from-emerald-600 to-green-600 
           text-white px-6 py-3 rounded-xl font-semibold 
           hover:from-emerald-700 hover:to-green-700 
           shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 
           transition-all"
```

---

##  Difficultés rencontrées

### 1. Configuration Docker Compose

**Problème** : Les tables n'étaient pas créées au démarrage.

**Cause** : Les modèles n'étaient pas importés dans `main.py`, donc SQLAlchemy ne les connaissait pas.

**Solution** :
```python
from models import User, Post, FicheLapin  # Import explicite
BaseSQL.metadata.create_all(bind=engine)
```

### 2. Authentification JWT dans Swagger UI

**Problème** : Impossible de s'authentifier via Swagger UI.

**Cause** : Variables d'environnement JWT mal nommées (JWT_SECRET_KEY vs SECRET_KEY).

**Solution** : Cohérence des noms de variables entre `.env` et le code.

### 3. CORS entre Frontend et Backend

**Problème** : Erreurs CORS lors des appels API depuis le frontend.

**Solution** : Ajout du middleware CORS dans FastAPI :
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Tailwind CSS ne chargeait pas

**Problème** : Styles non appliqués, affichage en noir et blanc.

**Cause** : Mauvaise configuration de PostCSS ou import CSS manquant.

**Solution** :
- Vérifier `tailwind.config.js` avec bon content path
- Import de `index.css` dans `main.jsx`
- Nettoyer le cache Vite : `rm -rf node_modules/.vite`

### 5. Gestion des relations SQLAlchemy

**Problème** : Erreurs lors de la suppression en cascade.

**Solution** : Configuration correcte des relations :
```python
posts = relationship(
    "Post",
    cascade="all, delete-orphan",  # Suppression en cascade
    passive_deletes=True,           # Laisser la DB gérer
    back_populates="fiche_lapin"
)
```

### 6. Affichage des images

**Problème** : Images ne s'affichaient pas, erreurs 404.

**Solution** :
- Placer les images dans `public/photos/`
- Utiliser le bon chemin : `/photos/${filename}`
- Ajouter un fallback avec `onError`

### 7. Tests avec base de données

**Problème** : Tests qui se marchent sur les pieds (données partagées).

**Solution** :
- Scope `function` pour les fixtures
- `create_all()` et `drop_all()` pour chaque test
- Cleanup dans les fixtures avec `yield`

---

##  Pistes d'amélioration

### Court terme (Quick wins)

1. **Upload de photos**
   - Endpoint `/upload` pour uploader des images
   - Stockage dans un volume Docker persistant
   - Validation du format et de la taille
   - Redimensionnement automatique

2. **Modification de fiches**
   - Formulaire d'édition complet
   - Mise à jour partielle (PATCH)
   - Historique des modifications

3. **Filtres et tri**
   - Filtrer par sexe, auteur, date
   - Trier par nom, date, numéro
   - Pagination côté serveur

4. **Export de données**
   - Export CSV des fiches
   - Export PDF d'une fiche
   - Génération de rapports

### Moyen terme

5. **Gestion des posts améliorée**
   - Interface de création de posts
   - Affichage chronologique
   - Edition et suppression
   - Markdown support

6. **Dashboard statistiques**
   - Nombre de lapins par sexe
   - Graphiques de poids moyen
   - Évolution des arrivées
   - Statistiques de santé

7. **Notifications**
   - Rappels de vaccins à venir
   - Alertes pour contrôles santé
   - Notifications email

8. **Recherche avancée**
   - Recherche full-text
   - Filtres multiples
   - Recherche par caractéristiques

### Long terme

9. **Multi-tenancy**
   - Gestion de plusieurs associations
   - Isolation des données
   - Tableau de bord global

10. **Application mobile**
    - React Native
    - Même API backend
    - Notifications push

11. **Adoption en ligne**
    - Page publique des lapins adoptables
    - Formulaire d'adoption
    - Suivi du processus d'adoption

12. **Intégrations**
    - Synchronisation calendrier (Google Calendar)
    - Export vers vétérinaires
    - API publique pour partenaires

13. **IA et ML**
    - Prédiction de poids idéal
    - Détection d'anomalies de santé
    - Recommandations alimentaires

14. **Internationalisation (i18n)**
    - Support multilingue
    - Formats de date localisés
    - Devises multiples

15. **Performance**
    - Cache Redis
    - CDN pour les images
    - Optimisation des requêtes SQL
    - Server-Side Rendering (SSR)

### Sécurité

16. **Améliorations sécurité**
    - Rate limiting
    - 2FA (authentification à deux facteurs)
    - Logs d'audit
    - Rotation automatique des tokens
    - HTTPS obligatoire
    - CSP (Content Security Policy)

---

##  Tests

### Exécution des tests

```bash
# Lancer tous les tests
docker-compose run tests

# Lancer les tests en local
cd app
pytest tests/ -v

# Avec coverage
pytest tests/ -v --cov=. --cov-report=html
```

### Coverage actuel

- Routes : ~90% de couverture
- Services : ~85% de couverture
- Models : ~80% de couverture

### Tests implémentés

**Authentification** :
-  Login avec credentials valides
-  Login avec credentials invalides
-  Token expiré
-  Token invalide

**Fiches lapins** :
-  Création de fiche
-  Lecture de toutes les fiches
-  Lecture d'une fiche par ID
-  Mise à jour par l'auteur
-  Mise à jour par non-auteur (403)
-  Suppression par l'auteur
-  Suppression en cascade des posts

**Posts** :
-  Création de post
-  Suppression par l'auteur
-  Suppression par non-auteur (403)

---

##  Métriques du projet

### Code

- Backend : ~2000 lignes de Python
- Frontend : ~1500 lignes de JavaScript/JSX
- Tests : ~800 lignes
- Total : ~4300 lignes

### Modèles

- 3 modèles : User, FicheLapin, Post
- 35+ champs dans FicheLapin
- 3 relations entre modèles

### Endpoints API

- 17 endpoints REST
- 4 groupes : auth, users, fiches, posts
- Documentation Swagger auto-générée

### Tests

- 25+ tests automatisés
- ~85% de code coverage
- 3 types : unitaires, intégration, e2e

---


##  Ressources et documentation

### Documentation officielle

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Docker](https://docs.docker.com/)

### Tutoriels utilisés

- [FastAPI JWT Authentication](https://testdriven.io/blog/fastapi-jwt-auth/)
- [React + Vite](https://vitejs.dev/guide/)
- [Tailwind with Vite](https://tailwindcss.com/docs/guides/vite)



