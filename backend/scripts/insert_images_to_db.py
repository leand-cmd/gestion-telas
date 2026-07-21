import psycopg2
import cloudinary
import cloudinary.api
import os
from dotenv import load_dotenv
import time

# Cargar variables
load_dotenv()

# Database
DATABASE_URL = "postgresql://postgres:SjUafZYzpKWrXzOpSDgNQISoUGTNTMYw@tokaido.proxy.rlwy.net:44666/railway"

# Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

print("Conectando a PostgreSQL...\n")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("OK: Conectado a PostgreSQL\n")
except Exception as e:
    print(f"ERROR: No se pudo conectar: {e}")
    exit()

# Obtener imágenes de Cloudinary
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
        })
    
    print(f"OK: {len(all_images)} imágenes encontradas\n")

except Exception as e:
    print(f"ERROR: {e}")
    exit()

if len(all_images) == 0:
    print("Sin imágenes en Cloudinary")
    exit()

# Insertar en base de datos
print("Insertando en base de datos...\n")

product_id = 579
images_per_product = 0
max_images_per_product = 3
inserted = 0
errors = 0

for img in all_images:
    try:
        image_url = img['url']
        alt_text = img['public_id'].split('/')[-1][:100]
        
        print(f"INSERT: Producto {product_id} - {alt_text[:40]}", end=" ")
        
        # Insertar en tabla product_images
        cursor.execute("""
            INSERT INTO product_images (product_id, image_url, alt_text, orden, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
        """, (product_id, image_url, alt_text, images_per_product))
        
        conn.commit()
        print("OK")
        inserted += 1
    
    except Exception as e:
        conn.rollback()
        print(f"ERROR: {str(e)[:40]}")
        errors += 1
    
    # Cambiar a siguiente producto
    images_per_product += 1
    if images_per_product >= max_images_per_product:
        product_id += 1
        images_per_product = 0
    
    time.sleep(0.1)

cursor.close()
conn.close()

print()
print("="*60)
print(f"RESUMEN FINAL")
print("="*60)
print(f"Imágenes insertadas: {inserted}")
print(f"Errores: {errors}")
print("="*60)
print(f"\n✅ Proceso completado!")
