[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}

$BaseUrl = "https://nurturing-miracle-production-c3b3.up.railway.app"
$Email = "aracellipaciellobaez@gmail.com"
$Password = "123456789"

Write-Host "Probando login..."

try {
    $response = Invoke-WebRequest `
        -Uri "$BaseUrl/api/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body (@{email = $Email; password = $Password} | ConvertTo-Json) `
        -ErrorAction Stop
    
    Write-Host "EXITO" -ForegroundColor Green
    Write-Host $response.Content
}
catch {
    Write-Host "ERROR" -ForegroundColor Red
    Write-Host $_
}