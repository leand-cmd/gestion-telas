import requests
from pathlib import Path

BASE_URL = "https://gestion-telas-production.up.railway.app"
EMAIL = "aracellipaciellobaez@gmail.com"
PASSWORD = "123456789"

# Login
print("Iniciando login...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"email": EMAIL, "password": PASSWORD},
    verify=False
)

if response.status_code != 200:
    print(f"ERROR: {response.status_code}")
    exit()

token = response.json()["token"]
print("OK: Login exitoso\n")

headers = {"Authorization": f"Bearer {token}"}

# Probar crear 1 producto para ver qué error exacto da
print("Probando creación de 1 producto para ver el error...\n")

prod_data = {
    "codigo": "TEST-001",
    "nombre": "Producto Test",
    "descripcion": "Test",
    "precio": 100.0,
    "stock": 10
}

print(f"Enviando: {prod_data}\n")

prod_response = requests.post(
    f"{BASE_URL}/api/productos",
    json=prod_data,
    headers=headers,
    verify=False
)

print(f"Status: {prod_response.status_code}")
print(f"Response: {prod_response.text}")
print(f"\n")

# Si está OK, continuar con el resto
if prod_response.status_code in [200, 201]:
    print("✓ Producto creado exitosamente!")
else:
    print("✗ Fallo en creación. Ver respuesta arriba para entender qué campo falta.")
