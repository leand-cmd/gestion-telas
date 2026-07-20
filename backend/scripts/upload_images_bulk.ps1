# backend/scripts/upload_images_bulk.ps1
# Script para subir masivamente imágenes a Cloudinary en Railway

param(
    [string]$BaseUrl = "https://gestion-telas.railway.app",  # REEMPLAZA CON TU URL
    [string]$Email = "admin@test.com",                         # Tu email de admin
    [string]$Password = "admin123"                              # Tu password de admin
)

# Colores para output
$Green = 'Green'
$Red = 'Red'
$Yellow = 'Yellow'
$Cyan = 'Cyan'

function Write-Success { Write-Host "✓ $args" -ForegroundColor $Green }
function Write-Error { Write-Host "✗ $args" -ForegroundColor $Red }
function Write-Info { Write-Host "• $args" -ForegroundColor $Cyan }
function Write-Warning { Write-Host "⚠ $args" -ForegroundColor $Yellow }

# ============================================
# 1. LOGIN
# ============================================

Write-Host "`n🚀 Iniciando carga masiva de imágenes...`n" -ForegroundColor Cyan

Write-Info "Login en: $BaseUrl"

try {
    $loginResponse = Invoke-WebRequest `
        -Uri "$BaseUrl/api/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body (@{
            email = $Email
            password = $Password
        } | ConvertTo-Json) `
        -SkipHttpsValidation `
        -ErrorAction Stop
    
    $loginData = $loginResponse.Content | ConvertFrom-Json
    $token = $loginData.access_token
    
    Write-Success "Login exitoso"
    Write-Info "Token: $($token.Substring(0, 20))..."
}
catch {
    Write-Error "No se pudo login: $_"
    exit 1
}

# ============================================
# 2. MAPEAR COLECCIONES CON PRODUCTOS
# ============================================

Write-Host "`n📊 Obteniendo información de productos...`n" -ForegroundColor Cyan

$collectionMapping = @{
    "ORGANIC_GARDEN" = @(1, 2)
    "FOIL_WASHED_PRINT" = @(3, 4)
    "CREPE_FOIL" = @(5, 6)
    "COTTON_JULIE" = @(7, 8)
    "CHARMEUSE_KRRTL" = @(9, 10)
    "DELICATA_FLOWER" = @(11, 12)
    "FOIL_CRISTAL_PRINT" = @(13, 14)
    "KNITTING_STRIPE_FOIL" = @(15, 16)
    "MILANO_F50_SPAN" = @(17, 18)
    "RAYON_BABY_TWILL" = @(19, 20)
    "VISCOSE_SLUB" = @(21, 22)
    "DYNAMIC_SUPREME" = @(23, 24)
    "ENCAJES_KRRTL" = @(25, 26)
    "ALFAIATERIA_BOSTON" = @(27, 28)
}

# ============================================
# 3. SUBIR IMÁGENES
# ============================================

Write-Host "📸 Subiendo imágenes...`n" -ForegroundColor Cyan

$stats = @{
    uploaded = 0
    errors = 0
    skipped = 0
}

foreach ($folder in $collectionMapping.Keys) {
    $folderPath = "extracted_images\$folder"
    
    if (-not (Test-Path $folderPath)) {
        Write-Warning "Carpeta no encontrada: $folder"
        continue
    }
    
    $images = Get-ChildItem "$folderPath\*.jpg" -ErrorAction SilentlyContinue
    
    if ($images.Count -eq 0) {
        Write-Warning "Sin imágenes en $folder"
        continue
    }
    
    Write-Info "$folder ($(($images | Measure-Object).Count) imágenes)"
    
    $productIds = $collectionMapping[$folder]
    $imgIndex = 0
    
    foreach ($productId in $productIds) {
        # Cada producto obtiene 1-2 imágenes
        for ($i = 0; $i -lt 2; $i++) {
            if ($imgIndex -ge $images.Count) {
                break
            }
            
            $image = $images[$imgIndex]
            
            try {
                Write-Host "   ⏳ Subiendo a producto $productId: $($image.Name)" -NoNewline
                
                $form = @{
                    file = $image
                    alt_text = $image.BaseName
                }
                
                $uploadResponse = Invoke-WebRequest `
                    -Uri "$BaseUrl/api/uploads/product/$productId" `
                    -Method POST `
                    -Headers @{
                        Authorization = "Bearer $token"
                    } `
                    -Form $form `
                    -SkipHttpsValidation `
                    -ErrorAction Stop
                
                Write-Host " ✓" -ForegroundColor Green
                $stats.uploaded++
                $imgIndex++
            }
            catch {
                Write-Host " ✗" -ForegroundColor Red
                Write-Warning "Error: $_"
                $stats.errors++
            }
        }
    }
    
    Write-Host ""
}

# ============================================
# 4. RESUMEN
# ============================================

Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "📊 RESUMEN DE CARGA" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "✓ Imágenes subidas: $($stats.uploaded)" -ForegroundColor Green
Write-Host "✗ Errores: $($stats.errors)" -ForegroundColor $(if ($stats.errors -gt 0) { 'Red' } else { 'Green' })
Write-Host "⊘ Omitidas: $($stats.skipped)" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "`n✅ Proceso completado`n" -ForegroundColor Green

exit 0
