import cloudinary
import cloudinary.uploader
import time
from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

print("Iniciando upload directo a Cloudinary...\n")

# Verificar credenciales
if not all([os.getenv('CLOUDINARY_CLOUD_NAME'), os.getenv('CLOUDINARY_API_KEY'), os.getenv('CLOUDINARY_API_SECRET')]):
    print("ERROR: Faltan credenciales de Cloudinary en .env")
    exit(1)

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

# Subir directamente a Cloudinary
print("Subiendo a Cloudinary...\n")

uploaded = 0
errors = 0

for img, collection_name in all_images:
    try:
        print(f"UPLOAD: {img.name}", end=" ")
        
        result = cloudinary.uploader.upload(
            str(img),
            folder=f"gestion-telas/{collection_name}",
            resource_type='auto',
            use_filename=True,
            unique_filename=True,
            overwrite=False
        )
        
        image_url = result.get('secure_url')
        print(f"OK ({image_url[:50]}...)")
        uploaded += 1
    
    except Exception as e:
        print(f"ERROR: {str(e)[:50]}")
        errors += 1
    
    # Delay para no saturar Cloudinary
    time.sleep(0.2)

print()
print("="*60)
print(f"RESUMEN FINAL")
print("="*60)
print(f"Imagenes subidas: {uploaded}")
print(f"Errores: {errors}")
print("="*60)
print(f"\n✅ Proceso completado!")
