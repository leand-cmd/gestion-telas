#!/usr/bin/env python3
"""
Script para matchear maestro Excel con imágenes y generar URLs de Cloudinary
"""

import pandas as pd
from pathlib import Path
import json

# ============================================================
# CONFIGURACIÓN
# ============================================================

MAESTRO_FILE = Path("Maestro_Telas_.xlsx")
EXTRACTED_IMAGES_PATH = Path("extracted_images")
OUTPUT_FILE = Path("MAESTRO_FINAL_CON_IMAGENES.xlsx")

# Mapeo de colecciones a carpetas (según lo que vimos)
COLLECTION_TO_FOLDER = {
    "Organic Garden": "NEW COLLECTION-ORGANIC GARDEN",
    "Tull 3D - Haute Couture": "NEW COLLECTION-TULL 3D",
    "Camiseria F50 - DSN A": "CAMISERIA F50 DSN A-B-C-D-E",
    "Camiseria F50 - DSN B": "CAMISERIA F50 DSN A-B-C-D-E",
    "Camiseria F50 - DSN C/D/E": "CAMISERIA F50 DSN A-B-C-D-E",
    "Raso Opaco": "RASO OPACO",
    "Rayon Challis - SS": "NEW COLLECTION-RAYON CHALLIS",
    "Colección Sport - Malha Fit Air": "NEW COLLECTION SPORT",
    "Colección Sport - Techno 160 Uni": "NEW COLLECTION SPORT",
    "Colección Sport - Dynamic Supreme": "DYNAMIC SUPREME_",
    "Alfaiataria Boston": "NEW COLLECTION-ALFAIATERIA BOSTON",
    "Cotton Julie": "NEW COLLECTION-COTTON JULIE",
    "Marrakesh Print - Verano": "NEW COLLECTION-MARRAKESH PRINT",
    "Lino Sonoma / Onit": "LINO- NEW COLLECTION",
    "Lino Santorini": "LINO- NEW COLLECTION",
    "Knitting Stripe Foil": "KNITTING STRIPE FOIL- NEW COLLECTION",
    "Milano F50 Span": "MILANO F50 SPAN-NEW COLLECTION",
    "Colección Encajes": "ENCAJES-KRRTL",
    "Foil Cristal Print": "FOIL CRISTAL PRINT_",
    "Crepe Foil": "CREPE FOIL",
    "Delicata Flower": "DELICATA FLOWER_ NEW COLLECTION",
    "Cotton Oxford Arket": "COTTON OXFORD ARKET-NEW COLLECTION",
    "Charmeuse de Colección": "CHARMEUSE - KRRTL",
    "Digital Charmeuse Elastizado": "CHARMEUSE OFERTA",
    "Cotton Rayón": "COTTON RAYÓN",
    "Classic Mozart": "EXCLUSIVO MOZART- CATALOGO",
    "Rayon Baby Twill": "RAYON BABY TWILL -NEW COLLECTION",
    "Viscose Slub": "VISCOSE SLUB_NEW COLLECTION",
    "Tiras y Randas": "TIRAS & RANDAS",
}

# URL de Cloudinary (actualizar con tu cloud_name)
CLOUDINARY_BASE = "https://res.cloudinary.com/bw1qcu31/image/upload/v1/"
CLOUDINARY_FOLDER = "gestion-telas"

# ============================================================
# FUNCIONES
# ============================================================

def find_image_for_codigo(codigo, folder_name):
    """Busca la imagen correspondiente al código en la carpeta"""
    folder_path = EXTRACTED_IMAGES_PATH / folder_name
    
    if not folder_path.exists():
        return None
    
    # Buscar imagen que matchee con el código
    # Formatos posibles: "21-9-1.jpg", "21_9_1.jpg", etc.
    codigo_variants = [
        f"{codigo}.jpg",
        codigo.replace("-", "_") + ".jpg",
        codigo.replace("-", "") + ".jpg",
    ]
    
    for image_file in folder_path.glob("*.jpg"):
        if image_file.name in codigo_variants:
            return image_file
        # También buscar si el código está en el nombre del archivo
        if codigo in image_file.name:
            return image_file
    
    return None

def generate_cloudinary_url(image_path):
    """Genera URL de Cloudinary para la imagen"""
    # Usar el patrón que ya usamos antes
    # Formato: gestion-telas/[colección]/[archivo]
    
    relative_path = image_path.relative_to(EXTRACTED_IMAGES_PATH)
    coleccion = relative_path.parts[0]
    filename = relative_path.name
    
    # URL en Cloudinary
    url = f"{CLOUDINARY_BASE}{CLOUDINARY_FOLDER}/{coleccion}/{filename}"
    return url

def process_maestro():
    """Procesa el maestro y matchea con imágenes"""
    
    print("=" * 70)
    print("📊 PROCESANDO MAESTRO Y MATCHEANDO IMÁGENES...")
    print("=" * 70)
    
    # Leer maestro
    if not MAESTRO_FILE.exists():
        print(f"❌ Archivo no encontrado: {MAESTRO_FILE}")
        return False
    
    df = pd.read_excel(MAESTRO_FILE)
    print(f"\n✓ Maestro cargado: {len(df)} productos")
    
    # Agregar columna de URL
    df['URL_Imagen'] = ""
    df['Imagen_Encontrada'] = ""
    
    matched = 0
    not_found = 0
    
    # Procesar cada producto
    for idx, row in df.iterrows():
        codigo = str(row['Cod Producto']).strip()
        coleccion = str(row['Colección']).strip()
        
        # Buscar carpeta correspondiente
        folder_name = COLLECTION_TO_FOLDER.get(coleccion)
        
        if not folder_name:
            print(f"[{idx+1}/{len(df)}] {codigo} - ⚠️  Colección no mapeada: {coleccion}")
            not_found += 1
            continue
        
        # Buscar imagen
        image_path = find_image_for_codigo(codigo, folder_name)
        
        if image_path:
            url = generate_cloudinary_url(image_path)
            df.at[idx, 'URL_Imagen'] = url
            df.at[idx, 'Imagen_Encontrada'] = "SÍ"
            matched += 1
            print(f"[{idx+1}/{len(df)}] {codigo} - ✓ {image_path.name}")
        else:
            df.at[idx, 'Imagen_Encontrada'] = "NO"
            not_found += 1
            print(f"[{idx+1}/{len(df)}] {codigo} - ✗ No encontrada en {folder_name}")
    
    # Guardar maestro final
    print(f"\n" + "=" * 70)
    print(f"📊 RESULTADOS:")
    print("=" * 70)
    print(f"✓ Imágenes encontradas: {matched}")
    print(f"✗ No encontradas: {not_found}")
    print(f"Total: {len(df)}")
    
    # Guardar
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n✅ Archivo generado: {OUTPUT_FILE}")
    
    # Resumen por colección
    print(f"\n📋 Resumen por colección:")
    for col in sorted(df['Colección'].unique()):
        subset = df[df['Colección'] == col]
        encontradas = len(subset[subset['Imagen_Encontrada'] == "SÍ"])
        total = len(subset)
        print(f"   • {col}: {encontradas}/{total}")
    
    return True

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("\n⚠️  REQUISITOS:")
    print("   1. Maestro_Telas_.xlsx en esta carpeta")
    print("   2. Carpeta extracted_images con imágenes")
    print("   3. Imágenes con nombres que matcheen códigos (ej: 21-9-1.jpg)")
    print("\n" + "=" * 70)
    
    input("Presiona ENTER para continuar...\n")
    
    success = process_maestro()
    
    if success:
        print("\n✅ ¡PROCESO COMPLETADO!")
        print(f"\nArchivo generado: {OUTPUT_FILE}")
        print("YA LISTO PARA SUBIR A LA APP")
    else:
        print("\n❌ Error en el proceso")
