#!/usr/bin/env python3
"""
Script para verificar integridad del maestro y imágenes antes de subida masiva
"""

import pandas as pd
from pathlib import Path
import json

# ============================================================
# CONFIGURACIÓN
# ============================================================

MAESTRO_FILE = Path("MAESTRO_FINAL_CON_IMAGENES.xlsx")
EXTRACTED_IMAGES_PATH = Path("extracted_images")

# ============================================================
# VERIFICACIONES
# ============================================================

print("=" * 70)
print("🔍 VERIFICACIÓN DE INTEGRIDAD")
print("=" * 70)

# 1. Verificar maestro
print("\n1️⃣  MAESTRO EXCEL:")
print("-" * 70)

if not MAESTRO_FILE.exists():
    print(f"❌ MAESTRO NO ENCONTRADO: {MAESTRO_FILE}")
else:
    try:
        df = pd.read_excel(MAESTRO_FILE)
        print(f"✅ Archivo encontrado: {MAESTRO_FILE}")
        print(f"   Total productos: {len(df)}")
        print(f"   Columnas: {len(df.columns)}")
        
        # Verificar columnas críticas
        columnas_criticas = ['Cod Producto', 'Colección', 'URL_Imagen', 'Imagen_Encontrada']
        for col in columnas_criticas:
            if col in df.columns:
                print(f"   ✅ {col}")
            else:
                print(f"   ❌ FALTA: {col}")
        
        # Contar imágenes encontradas
        encontradas = len(df[df['Imagen_Encontrada'] == "SÍ"])
        no_encontradas = len(df[df['Imagen_Encontrada'] == "NO"])
        print(f"\n   Imágenes encontradas: {encontradas}")
        print(f"   Imágenes no encontradas: {no_encontradas}")
        
        # Colecciones
        print(f"\n   Colecciones ({df['Colección'].nunique()}):")
        for col in sorted(df['Colección'].unique()):
            count = len(df[df['Colección'] == col])
            print(f"      • {col}: {count}")
        
    except Exception as e:
        print(f"❌ ERROR al leer maestro: {str(e)}")

# 2. Verificar imágenes locales
print("\n\n2️⃣  IMÁGENES LOCALES:")
print("-" * 70)

if not EXTRACTED_IMAGES_PATH.exists():
    print(f"❌ CARPETA NO ENCONTRADA: {EXTRACTED_IMAGES_PATH}")
else:
    print(f"✅ Carpeta encontrada: {EXTRACTED_IMAGES_PATH}")
    
    total_images = 0
    folders_info = {}
    
    for folder in sorted(EXTRACTED_IMAGES_PATH.iterdir()):
        if folder.is_dir():
            images = list(folder.glob("*.jpg"))
            total_images += len(images)
            folders_info[folder.name] = len(images)
    
    print(f"   Total carpetas: {len(folders_info)}")
    print(f"   Total imágenes: {total_images}")
    
    print(f"\n   Carpetas de imágenes:")
    for folder, count in sorted(folders_info.items()):
        print(f"      • {folder}: {count} imágenes")

# 3. Verificar Cloudinary URLs
print("\n\n3️⃣  URLS DE CLOUDINARY:")
print("-" * 70)

if MAESTRO_FILE.exists():
    try:
        df = pd.read_excel(MAESTRO_FILE)
        urls_con_valor = df[df['URL_Imagen'].notna() & (df['URL_Imagen'] != "")]
        print(f"✅ URLs generadas: {len(urls_con_valor)}")
        
        # Ver ejemplos
        print(f"\n   Ejemplos de URLs:")
        for idx, url in enumerate(urls_con_valor['URL_Imagen'].head(3).values, 1):
            print(f"      {idx}. {url[:80]}...")
        
        # Verificar patrón de URLs
        cloudinary_urls = [url for url in urls_con_valor['URL_Imagen'] if 'cloudinary' in str(url)]
        print(f"\n   URLs válidas de Cloudinary: {len(cloudinary_urls)}/{len(urls_con_valor)}")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

# 4. Resumen final
print("\n\n" + "=" * 70)
print("✅ RESUMEN FINAL")
print("=" * 70)

try:
    if MAESTRO_FILE.exists():
        df = pd.read_excel(MAESTRO_FILE)
        encontradas = len(df[df['Imagen_Encontrada'] == "SÍ"])
        total = len(df)
        
        print(f"\n✅ Estado para subida masiva:")
        print(f"   • Maestro: {total} productos")
        print(f"   • Imágenes matcheadas: {encontradas}/{total} ({(encontradas/total)*100:.1f}%)")
        print(f"   • Listo para subir: {'SÍ ✅' if encontradas > 0 else 'NO ❌'}")
        
        if encontradas == total:
            print(f"\n🎉 ¡¡¡PERFECTO!!! Todos los productos tienen imágenes")
        elif encontradas >= total * 0.9:
            print(f"\n⚠️  Casi listo: {total - encontradas} productos sin imagen")
        else:
            print(f"\n❌ Revisar: Muchos productos sin imagen")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

print("\n" + "=" * 70)
