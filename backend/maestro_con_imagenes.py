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

MAESTRO_FILE = Path("Maestro_Telas .xlsx")
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

# Códigos de productos por colección (primeros dígitos)
# Ej: 21-10 = Camiseria, 26-48 = Charmeuse, etc.
CODE_PREFIXES = {
    "47": "Organic Garden",
    "46": "Tull 3D - Haute Couture",
    "21-10": "Camiseria F50 - DSN A",
    "21-11": "Camiseria F50 - DSN B",
    "21-12": "Camiseria F50 - DSN C/D/E",
    "21-13": "Camiseria F50 - DSN C/D/E",
    "17-16": "Raso Opaco",
    "26-53": "Rayon Challis - SS",
    "86-6": "Colección Sport - Techno 160 Uni",
    "87-1": "Colección Sport - Dynamic Supreme",
    "82-15": "Alfaiataria Boston",
    "26-51": "Cotton Julie",
    "20-118": "Marrakesh Print - Verano",
    "52-4": "Lino Sonoma / Onit",
    "16-13": "Knitting Stripe Foil",
    "53-8": "Milano F50 Span",
    "18-15": "Colección Encajes",
    "20-80": "Colección Encajes",
    "42-8": "Colección Encajes",
    "16-15": "Foil Cristal Print",
    "16-11": "Crepe Foil",
    "48-1": "Delicata Flower",
    "21-8": "Cotton Oxford Arket",
    "26-48": "Charmeuse de Colección",
    "26-41": "Digital Charmeuse Elastizado",
    "24-36": "Cotton Rayón",
    "24-51": "Rayon Baby Twill",
    "15-10": "Classic Mozart",
    "26-54": "Viscose Slub",
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
    
    # El nombre del archivo es exactamente el código + .jpg
    # Ej: 21-10-1.jpg, 26-48-1305.jpg, etc.
    target_file = folder_path / f"{codigo}.jpg"
    
    if target_file.exists():
        return target_file
    
    # Si no está exacto, buscar por prefijo del código
    codigo_prefix = codigo.rsplit('-', 1)[0]  # Ej: "21-10" de "21-10-1"
    
    for image_file in folder_path.glob(f"{codigo_prefix}*.jpg"):
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

def get_folder_for_codigo(codigo):
    """Determina la carpeta correcta basada en el código del producto"""
    # Buscar en CODE_PREFIXES por orden de especificidad
    # Primero prefijos completos (ej: 21-10), luego simples (ej: 21)
    
    for prefix in sorted(CODE_PREFIXES.keys(), key=len, reverse=True):
        if codigo.startswith(prefix):
            coleccion = CODE_PREFIXES[prefix]
            folder = COLLECTION_TO_FOLDER.get(coleccion)
            if folder:
                return folder
    
    return None

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
        
        # Buscar carpeta correspondiente usando el código
        folder_name = get_folder_for_codigo(codigo)
        
        if not folder_name:
            # Fallback: usar colección del maestro
            folder_name = COLLECTION_TO_FOLDER.get(coleccion)
        
        if not folder_name:
            print(f"[{idx+1}/{len(df)}] {codigo} - ⚠️  No se puede determinar carpeta")
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
