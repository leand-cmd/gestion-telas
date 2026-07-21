import requests
import time
from pathlib import Path
import cloudinary
import cloudinary.api
import os
from dotenv import load_dotenv

# Cargar variables
load_dotenv()

BASE_URL = "https://gestion-telas-production.up.railway.app"
EMAIL = "aracellipaciellobaez@gmail.com"
PASSWORD = "123456789"

# Configurar Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

print("Iniciando login...\n")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"email": EMAIL, "password": PASSWORD},
    verify=False
)

if response.status_code != 200:
    print(f"ERROR: No se pudo loguear")
    exit()

token = response.json()["token"]
print("OK: Login exitoso\n")

headers = {"Authorization": f"Bearer {token}"}

# Obtener lista de imágenes de Cloudinary
print("Obteniendo imágenes de Cloudinary...\n")

try:
    resources = cloudinary.api.resources(
        type='upload',
        prefix='gestion-telas/',
        max_results=500
    )
    
    all_images = []
    for resource in resources.get('resources', []):
        all_images.append({
            'url': resource['secure_url'],
            'public_id': resource['public_id'],
            'folder': resource.get('folder', '')
        })
    
    print(f"OK: {len(all_images)} imágenes encontradas en Cloudinary\n")

except Exception as e:
    print(f"ERROR: {e}")
    exit()

if len(all_images) == 0:
    print("Sin imágenes en Cloudinary")
    exit()

# Distribuir imágenes a productos
print("Asociando imágenes a productos...\n")

product_id = 579  # Empezar desde primer producto creado
images_per_product = 0
max_images_per_product = 3
associated = 0
errors = 0

for img in all_images:
    try:
        image_url = img['url']
        alt_text = img['public_id'].split('/')[-1]
        
        print(f"ASSOCIATE: Producto {product_id} - {alt_text}", end=" ")
        
        # Crear ProductImage directamente
        payload = {
            "product_id": product_id,
            "image_url": image_url,
            "alt_text": alt_text,
            "order": images_per_product
        }
        
        # Intentar crear via API
        response = requests.post(
            f"{BASE_URL}/api/product-images",  # Endpoint para crear product images
            json=payload,
            headers=headers,
            verify=False,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("OK")
            associated += 1
        else:
            # Si falla el endpoint, intentar via uploads
            try:
                # Descargar la imagen de Cloudinary y subirla
                img_response = requests.get(image_url, timeout=10)
                if img_response.status_code == 200:
                    files = {"file": (alt_text + ".jpg", img_response.content)}
                    data = {"alt_text": alt_text}
                    
                    upload_response = requests.post(
                        f"{BASE_URL}/api/uploads/product/{product_id}",
                        files=files,
                        data=data,
                        headers=headers,
                        verify=False,
                        timeout=30
                    )
                    
                    if upload_response.status_code in [200, 201]:
                        print("OK (via upload)")
                        associated += 1
                    else:
                        print(f"ERROR {upload_response.status_code}")
                        errors += 1
                else:
                    print("ERROR (download)")
                    errors += 1
            except Exception as e:
                print(f"ERROR {str(e)[:30]}")
                errors += 1
    
    except Exception as e:
        print(f"ERROR: {str(e)[:40]}")
        errors += 1
    
    # Cambiar a siguiente producto
    images_per_product += 1
    if images_per_product >= max_images_per_product:
        product_id += 1
        images_per_product = 0
    
    time.sleep(1)

print()
print("="*60)
print(f"RESUMEN FINAL")
print("="*60)
print(f"Imágenes asociadas: {associated}")
print(f"Errores: {errors}")
print("="*60)
print(f"\n✅ Proceso completado!")
