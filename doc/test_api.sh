# ============================================================================
# Script de test API pour Windows PowerShell
# ============================================================================

Write-Host "🚀 Test de l'API SPI LOEN" -ForegroundColor Cyan
Write-Host ""

# 1. Créer un utilisateur
Write-Host "1️⃣ Création d'un utilisateur..." -ForegroundColor Yellow

$createUserBody = @{
    username = "testadmin"
    password = "test123"
    firstName = "Test"
    lastName = "Admin"
    email = "test@test.fr"
    role = "admin"
} | ConvertTo-Json

try {
    $createResponse = Invoke-RestMethod -Uri "http://localhost:5001/users/" `
        -Method Post `
        -ContentType "application/json" `
        -Body $createUserBody

    Write-Host "✅ Utilisateur créé avec succès !" -ForegroundColor Green
    Write-Host "ID: $($createResponse.id)" -ForegroundColor Gray
    Write-Host "Username: $($createResponse.username)" -ForegroundColor Gray
    Write-Host ""
}
catch {
    Write-Host "❌ Erreur lors de la création de l'utilisateur" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
}

# 2. Obtenir un token JWT
Write-Host "2️⃣ Obtention d'un token JWT..." -ForegroundColor Yellow

$authBody = @{
    username = "testadmin"
    password = "test123"
} | ConvertTo-Json

try {
    $authResponse = Invoke-RestMethod -Uri "http://localhost:5001/auth/token" `
        -Method Post `
        -ContentType "application/json" `
        -Body $authBody

    $token = $authResponse.access_token
    Write-Host "✅ Token obtenu avec succès !" -ForegroundColor Green
    Write-Host "Token: $token" -ForegroundColor Gray
    Write-Host ""
}
catch {
    Write-Host "❌ Erreur lors de l'obtention du token" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    exit
}

# 3. Tester l'accès à un endpoint protégé
Write-Host "3️⃣ Test d'accès aux fiches lapins (endpoint protégé)..." -ForegroundColor Yellow

$headers = @{
    "Authorization" = "Bearer $token"
}

try {
    $fichesResponse = Invoke-RestMethod -Uri "http://localhost:5001/ficheslapin/" `
        -Method Get `
        -Headers $headers

    Write-Host "✅ Accès autorisé ! Nombre de fiches: $($fichesResponse.Count)" -ForegroundColor Green
    Write-Host ""
    
    if ($fichesResponse.Count -gt 0) {
        Write-Host "📋 Première fiche:" -ForegroundColor Cyan
        $fichesResponse[0] | Format-List
    }
}
catch {
    Write-Host "❌ Erreur lors de l'accès aux fiches" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
}

# 4. Créer une fiche lapin
Write-Host "4️⃣ Création d'une fiche lapin..." -ForegroundColor Yellow

$ficheBody = @{
    nom = "Pompon Test"
    numero_arrivee_association = 999
    date_creation_fiche = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
    date_arrivee_association = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
    sexe = "M"
    poids_actuel = 2000
    auteur_id = "dummy" # sera remplacé par le backend
} | ConvertTo-Json

try {
    $createFicheResponse = Invoke-RestMethod -Uri "http://localhost:5001/ficheslapin/" `
        -Method Post `
        -Headers $headers `
        -ContentType "application/json" `
        -Body $ficheBody

    Write-Host "✅ Fiche lapin créée avec succès !" -ForegroundColor Green
    Write-Host "ID: $($createFicheResponse.id)" -ForegroundColor Gray
    Write-Host "Nom: $($createFicheResponse.nom)" -ForegroundColor Gray
    Write-Host ""
}
catch {
    Write-Host "❌ Erreur lors de la création de la fiche" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
}

Write-Host "✨ Tests terminés !" -ForegroundColor Cyan