# 🔐 Guide d'authentification Swagger UI

## Étape 1 : Créer un utilisateur

1. Allez sur l'endpoint **POST /users/**
2. Cliquez sur "Try it out"
3. Entrez les données :

```json
{
  "username": "admin",
  "password": "admin123",
  "firstName": "Admin",
  "lastName": "Test",
  "email": "admin@test.fr",
  "role": "admin"
}
```

4. Cliquez sur "Execute"
5. Vous devriez recevoir un code 200 avec les détails de l'utilisateur créé

---

## Étape 2 : Obtenir un token JWT

1. Allez sur l'endpoint **POST /auth/token**
2. Cliquez sur "Try it out"
3. Entrez les credentials :

```json
{
  "username": "admin",
  "password": "admin123"
}
```

4. Cliquez sur "Execute"
5. **Copiez le token** dans la réponse :

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Étape 3 : S'authentifier dans Swagger

1. **Cliquez sur le bouton "Authorize" 🔒** en haut à droite de la page Swagger
2. Une fenêtre s'ouvre
3. **Collez votre token** dans le champ "Value" (SANS le préfixe "Bearer")
4. Cliquez sur **"Authorize"**
5. Cliquez sur **"Close"**

✅ **Vous êtes maintenant authentifié !** Le cadenas 🔒 à côté des endpoints devrait être fermé.

---

## Étape 4 : Tester un endpoint protégé

1. Allez sur **GET /ficheslapin/**
2. Cliquez sur "Try it out"
3. Cliquez sur "Execute"
4. Vous devriez recevoir la liste des fiches lapins (peut être vide au début)

---

## 🐛 Problèmes courants

### ❌ Erreur 403 "Not authenticated"
- Vous n'avez pas cliqué sur "Authorize" 
- Vérifiez que le cadenas 🔒 est bien fermé

### ❌ Erreur 401 "Invalid token"
- Votre token a expiré (30 minutes par défaut)
- Regénérez un nouveau token avec POST /auth/token

### ❌ Erreur 401 "Token expired"
- Votre token a expiré
- Regénérez-en un nouveau

### ❌ Erreur 404 "User not found"
- L'utilisateur n'existe pas
- Créez-le d'abord avec POST /users/

### ❌ Erreur 400 "Incorrect password"
- Le mot de passe est incorrect
- Vérifiez vos credentials

---

## 🔄 Alternative : Utiliser curl

Si Swagger ne fonctionne toujours pas, testez avec curl :

```bash
# 1. Créer un utilisateur
curl -X POST "http://localhost:5001/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123",
    "firstName": "Admin",
    "lastName": "Test",
    "email": "admin@test.fr",
    "role": "admin"
  }'

# 2. Obtenir un token
TOKEN=$(curl -X POST "http://localhost:5001/auth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"

# 3. Utiliser le token pour accéder aux endpoints protégés
curl -X GET "http://localhost:5001/ficheslapin/" \
  -H "Authorization: Bearer $TOKEN"
```

---

## ✅ Utilisateurs de test (après seed)

Le script de seed crée automatiquement ces utilisateurs :

| Username | Password | Role       |
|----------|----------|------------|
| admin    | adminpass| admin      |
| camille  | camille  | fondateur  |
| cedric   | cedric   | fondateur  |
| aurelia  | aurelia  | benevole   |
| marion   | marion   | benevole   |

Vous pouvez les utiliser directement !