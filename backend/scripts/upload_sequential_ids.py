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

# Recolectar todas las imágenes
images_base = Path("extracted_images")
all_images = []

print("Recolectando imágenes...\n")

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

print(f"\nTotal: {len(all_images)} imagenes\n")

if len(all_images) == 0:
    print("ERROR: Sin imagenes")
    exit()

# Subir imágenes usando IDs secuenciales empezando desde 579
print("Subiendo imágenes...\n")

uploaded_images = 0
errors = 0
product_id = 579  # Empezar desde ID 579 (primeros productos creados)
images_per_product = 0
max_images_per_product = 3

for img, collection_name in all_images:
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
            print("OK")
            uploaded_images += 1
        else:
            print(f"ERROR {upload_response.status_code}")
            errors += 1
    
    except Exception as e:
        print(f"ERROR: {str(e)[:40]}")
        errors += 1
    
    # Cambiar a siguiente producto después de X imágenes
    images_per_product += 1
    if images_per_product >= max_images_per_product:
        product_id += 1
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
