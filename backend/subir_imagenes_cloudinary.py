#!/usr/bin/env python3
"""
Script para subir imágenes a Cloudinary y generar maestro con URLs actualizadas
"""

import os
from pathlib import Path
import pandas as pd
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import time

# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

# Cloudinary
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

EXTRACTED_IMAGES_PATH = Path("extracted_images")
MAESTRO_FILE = Path("MAESTRO_FINAL_CON_IMAGENES.xlsx")
OUTPUT_FILE = Path("MAESTRO_CON_URLS_CLOUDINARY.xlsx")

# ============================================================
# FUNCIONES
# ============================================================

def upload_image_to_cloudinary(image_path, coleccion_name):
    """Sube imagen a Cloudinary y retorna la URL"""
    try:
        # Nombre único para la imagen en Cloudinary
        public_id = f"gestion-telas/{coleccion_name}/{image_path.stem}"
        
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            str(image_path),
            public_id=public_id,
            overwrite=True,
            resource_type="auto"
        )
        
        return result.get('secure_url')
    
    except Exception as e:
        print(f"❌ Error subiendo {image_path.name}: {str(e)[:50]}")
        return None

def process_and_upload():
    """Procesa maestro, sube imágenes y genera URLs"""
    
    print("=" * 70)
    print("🚀 SUBIENDO IMÁGENES A CLOUDINARY...")
    print("=" * 70)
    
    # Verificar credenciales
    if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
        print("❌ FALTA configurar variables de Cloudinary en .env")
        print("   Necesitas:")
        print("   CLOUDINARY_CLOUD_NAME=tu_cloud_name")
        print("   CLOUDINARY_API_KEY=tu_api_key")
        print("   CLOUDINARY_API_SECRET=tu_api_secret")
        return False
    
    print(f"\n✓ Cloudinary configurado: {CLOUDINARY_CLOUD_NAME}")
    
    # Leer maestro actual
    if not MAESTRO_FILE.exists():
        print(f"❌ Archivo no encontrado: {MAESTRO_FILE}")
        return False
    
    df = pd.read_excel(MAESTRO_FILE)
    print(f"✓ Maestro cargado: {len(df)} productos\n")
    
    uploaded = 0
    skipped = 0
    errors = 0
    urls_generadas = 0
    
    # Procesar cada producto
    for idx, row in df.iterrows():
        codigo = str(row['Cod Producto']).strip()
        coleccion = str(row['Colección']).strip()
        folder_name = None
        
        # Encontrar carpeta de imágenes
        for folder in EXTRACTED_IMAGES_PATH.iterdir():
            if folder.is_dir() and folder.name in coleccion:
                folder_name = folder.name
                break
        
        if not folder_name:
            # Buscar por código
            for folder in EXTRACTED_IMAGES_PATH.iterdir():
                if folder.is_dir():
                    image_file = folder / f"{codigo}.jpg"
                    if image_file.exists():
                        folder_name = folder.name
                        break
        
        if not folder_name:
            print(f"[{idx+1}/{len(df)}] {codigo} - ⚠️  Carpeta no encontrada")
            skipped += 1
            continue
        
        # Buscar imagen
        image_path = EXTRACTED_IMAGES_PATH / folder_name / f"{codigo}.jpg"
        
        if not image_path.exists():
            print(f"[{idx+1}/{len(df)}] {codigo} - ✗ Imagen no encontrada")
            errors += 1
            continue
        
        print(f"[{idx+1}/{len(df)}] {codigo} - Subiendo...", end=" ")
        
        # Subir a Cloudinary
        url = upload_image_to_cloudinary(image_path, folder_name)
        
        if url:
            df.at[idx, 'URL_Imagen'] = url
            urls_generadas += 1
            uploaded += 1
            print("✓")
        else:
            print("✗")
            errors += 1
        
        # Esperar un poco para no saturar
        time.sleep(0.2)
    
    # Guardar maestro actualizado
    print(f"\n" + "=" * 70)
    print(f"📊 RESULTADOS")
    print("=" * 70)
    print(f"Imágenes subidas: {uploaded}")
    print(f"URLs generadas: {urls_generadas}")
    print(f"Errores: {errors}")
    print(f"Omitidas: {skipped}")
    
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n✅ Archivo generado: {OUTPUT_FILE}")
    print(f"   LISTO PARA ACTUALIZAR EN RAILWAY")
    
    return True

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("\n⚠️  REQUISITOS:")
    print("   1. .env con credenciales de Cloudinary")
    print("   2. MAESTRO_FINAL_CON_IMAGENES.xlsx")
    print("   3. Carpeta extracted_images con imágenes")
    print("\n" + "=" * 70)
    
    input("Presiona ENTER para continuar...\n")
    
    success = process_and_upload()
    
    if success:
        print("\n✅ ¡IMÁGENES SUBIDAS A CLOUDINARY!")
        print(f"Siguiente paso: Actualizar maestro en la app")
    else:
        print("\n❌ Error en el proceso")
