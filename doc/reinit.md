#🎯 Procédure complète de réinitialisation

## 1. TOUT ARRÊTER
docker-compose down -v
docker system prune -f

## 2. Vérifier que tout est bien arrêté
docker ps -a
docker volume ls

## 3. Si des volumes persistent, les supprimer manuellement
docker volume rm app_postgres_data_auth

## 4. Remplacer votre docker-compose.yml avec la version ci-dessus

## 5. Reconstruire SANS cache
docker-compose build --no-cache

## 6. Démarrer
docker-compose up -d

## 7. Suivre les logs en temps réel
docker-compose logs -f


## TOKEN 
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjZhNTNkOTctMzE3MC00MjYwLTlkNmUtYmU1NWFlYmU4MjQxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY0MjYxNTAyfQ.IEUrpSdueerGCOtnVjsx31hoIYcZS0f7205Un1be2RY


