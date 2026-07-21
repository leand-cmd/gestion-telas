import requests
import time
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

# Obtener TODOS los productos existentes
print("Obteniendo productos existentes...")
try:
    prod_response = requests.get(
        f"{BASE_URL}/api/productos?limit=1000",
        headers=headers,
        verify=False
    )
    
    if prod_response.status_code == 200:
        productos = prod_response.json()
        if isinstance(productos, dict):
            productos = productos.get("data", [])
        print(f"OK: {len(productos)} productos encontrados\n")
    else:
        print(f"ERROR: {prod_response.status_code}")
        productos = []
except Exception as e:
    print(f"ERROR: {e}")
    productos = []

# Procesar imágenes y asignarlas a productos
images_base = Path("extracted_images")

print("Subiendo imágenes...\n")
uploaded_images = 0
errors = 0
product_idx = 0

# Recolectar todas las imágenes
all_images = []
for folder_path in sorted(images_base.iterdir()):
    if not folder_path.is_dir():
        continue
    
    collection_name = folder_path.name
    images = sorted(folder_path.glob("*.jpg"))
    
    if not images:
        print(f"SKIP: {collection_name} (sin imagenes)")
        continue
    
    print(f"PROC: {collection_name} ({len(images)} imagenes)")
    
    for img in images:
        all_images.append((img, collection_name))

print(f"\nTotal: {len(all_images)} imagenes, {len(productos)} productos\n")

if len(all_images) == 0 or len(productos) == 0:
    print("ERROR: Sin imagenes o productos")
    exit()

# Distribuir imágenes entre productos
print("Distribuyendo imágenes...\n")

product_idx = 0
images_per_product = 0
max_images_per_product = 3

for img, collection_name in all_images:
    if product_idx >= len(productos):
        product_idx = 0
    
    product = productos[product_idx]
    product_id = product.get("id") if isinstance(product, dict) else product
    
    try:
        print(f"UPLOAD: Producto {product_id} - {img.name}", end=" ")
        
        with open(img, "rb") as f:
            files = {"file": f}
            data = {"alt_text": img.stem}
            
            upload_response = requests.post(
                f"{BASE_URL}/api/uploads/product/{product_id}",
                files=files,
                data=data,
                headers=headers,
                verify=False,
                timeout=30
            )
        
        if upload_response.status_code in [200, 201]:
            print("✓")
            uploaded_images += 1
        else:
            print(f"✗ ({upload_response.status_code})")
            errors += 1
    
    except Exception as e:
        print(f"✗ Error: {str(e)[:30]}")
        errors += 1
    
    # Cambiar a siguiente producto después de X imágenes
    images_per_product += 1
    if images_per_product >= max_images_per_product:
        product_idx += 1
        images_per_product = 0
    
    # Delay para no saturar servidor
    time.sleep(0.5)

print()
print("="*60)
print(f"RESUMEN FINAL")
print("="*60)
print(f"Imagenes subidas: {uploaded_images}")
print(f"Errores: {errors}")
print("="*60)
print(f"\n✅ Proceso completado!")
