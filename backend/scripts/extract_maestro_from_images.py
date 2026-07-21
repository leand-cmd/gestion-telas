#!/usr/bin/env python3
"""
Script para extraer datos de imágenes de telas y generar maestro Excel
Extrae: código, nombre, color, categoría, subcategoría, tipo diseño, composición, etc.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
from PIL import Image
import numpy as np
try:
    import pytesseract
except:
    print("⚠️  pytesseract no instalado. Ejecuta: pip install pytesseract")

# ============================================================
# CONFIGURACIÓN
# ============================================================

EXTRACTED_IMAGES_PATH = Path("extracted_images")
OUTPUT_FILE = Path("MAESTRO_GENERADO_DESDE_IMAGENES.xlsx")

# Categorías inferidas por colección
COLLECTION_CATEGORIES = {
    "CAMISERIA": ("Eventos / Formal", "Sastrería / Camisas"),
    "CHARMEUSE": ("Eventos / Formal", "Vestidos"),
    "COTTON": ("Casual", "Camisería"),
    "CREPE": ("Eventos / Formal", "Vestidos"),
    "DELICATA": ("Eventos / Fiesta", "Encajes"),
    "DYNAMIC": ("Casual", "Casual"),
    "ENCAJES": ("Eventos / Fiesta", "Encajes"),
    "EXCLUSIVO": ("Eventos / Formal", "Alta Costura"),
    "FOIL": ("Eventos / Fiesta", "Diseños Especiales"),
    "KNITTING": ("Eventos / Fiesta", "Tejidos Tejidos"),
    "LINO": ("Casual", "Lino"),
    "MILANO": ("Eventos / Formal", "Camisería"),
    "NEW COLLECTION": ("General", "Colección"),
    "RASO": ("Eventos / Formal", "Satenes"),
    "RAYON": ("Casual", "Rayón"),
    "TIRAS": ("Accesorios", "Tiras"),
    "TULL": ("Eventos / Fiesta", "Encajes"),
    "VISCOSE": ("Casual", "Viscosa"),
    "MOZART": ("Eventos / Formal", "Alta Costura"),
    "OXFORD": ("Casual", "Camisería"),
}

# ============================================================
# FUNCIONES
# ============================================================

def get_dominant_color(image_path):
    """Obtiene el color dominante de la imagen"""
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((150, 150))
        pixels = np.array(img)
        pixels = pixels.reshape((-1, 3))
        
        # Encontrar color dominante
        from PIL import Image as PILImage
        unique, counts = np.unique(pixels.reshape(-1, pixels.shape[-1]), axis=0, return_counts=True)
        dominant_color_rgb = unique[counts.argmax()]
        
        # Inferir nombre de color
        r, g, b = dominant_color_rgb
        
        if r > 200 and g > 200 and b > 200:
            return "Blanco"
        elif r < 50 and g < 50 and b < 50:
            return "Negro"
        elif r > g and r > b:
            if r > 150:
                return "Rojo"
            else:
                return "Marrón"
        elif g > r and g > b:
            return "Verde"
        elif b > r and b > g:
            return "Azul"
        elif r > 150 and g > 150 and b < 100:
            return "Amarillo"
        elif r > 150 and g < 100 and b > 100:
            return "Rosa"
        elif r > 100 and g > 100 and b > 100:
            return "Gris"
        else:
            return "Multicolor"
    except:
        return "Desconocido"

def extract_text_from_image(image_path):
    """Extrae texto de la imagen usando OCR"""
    try:
        img = Image.open(image_path)
        # Simplificar imagen para mejor OCR
        img = img.convert('L')  # Convertir a escala de grises
        text = pytesseract.image_to_string(img, lang='spa+eng')
        return text.strip()
    except:
        return ""

def infer_category_from_collection(collection_name):
    """Infiere categoría y subcategoría por nombre de colección"""
    collection_upper = collection_name.upper()
    
    for key, (categoria, subcategoria) in COLLECTION_CATEGORIES.items():
        if key in collection_upper:
            return categoria, subcategoria
    
    return "Tejido", "General"

def infer_design_type(image_path, text_extracted):
    """Infiere tipo de diseño basado en imagen y texto"""
    text_lower = text_extracted.lower()
    
    if any(word in text_lower for word in ["floral", "flores", "flower"]):
        return "Floral"
    elif any(word in text_lower for word in ["liso", "plain", "solid"]):
        return "Liso"
    elif any(word in text_lower for word in ["rayado", "stripe", "stripes"]):
        return "Rayado"
    elif any(word in text_lower for word in ["encaje", "lace", "puntilla"]):
        return "Encaje"
    elif any(word in text_lower for word in ["estampado", "print", "printed"]):
        return "Estampado"
    elif any(word in text_lower for word in ["foil", "brillante", "shiny"]):
        return "Foil"
    elif any(word in text_lower for word in ["calado", "openwork"]):
        return "Calado"
    else:
        return "Diseño"

def infer_composition(text_extracted, collection_name):
    """Infiere composición basada en texto"""
    text_lower = text_extracted.lower()
    collection_lower = collection_name.lower()
    
    if "algodón" in text_lower or "cotton" in text_lower or "cotton" in collection_lower:
        return "100% Algodón"
    elif "poliamida" in text_lower or "poliamid" in text_lower:
        return "Poliamida"
    elif "viscosa" in text_lower or "viscose" in text_lower or "viscose" in collection_lower:
        return "Viscosa"
    elif "rayón" in text_lower or "rayon" in text_lower:
        return "Rayón"
    elif "lino" in text_lower or "linen" in text_lower:
        return "Lino"
    elif "seda" in text_lower or "silk" in text_lower:
        return "Seda"
    elif "poliéster" in text_lower or "polyester" in text_lower:
        return "Poliéster"
    else:
        return "Tela"

def process_images():
    """Procesa todas las imágenes y genera maestro"""
    
    if not EXTRACTED_IMAGES_PATH.exists():
        print(f"❌ Carpeta no encontrada: {EXTRACTED_IMAGES_PATH}")
        print(f"   Asegúrate que exista en: {Path.cwd() / EXTRACTED_IMAGES_PATH}")
        return False
    
    productos = []
    id_counter = 1
    total_images = 0
    processed_images = 0
    errors = 0
    
    print("=" * 70)
    print("🚀 EXTRAYENDO DATOS DE IMÁGENES...")
    print("=" * 70)
    
    # Procesar cada carpeta (colección)
    for collection_folder in sorted(EXTRACTED_IMAGES_PATH.iterdir()):
        if not collection_folder.is_dir():
            continue
        
        collection_name = collection_folder.name
        images = sorted(collection_folder.glob("*.jpg"))
        
        if not images:
            print(f"\n⊘ {collection_name}: Sin imágenes")
            continue
        
        print(f"\n📁 {collection_name} ({len(images)} imágenes)")
        
        # Procesar cada imagen
        for img_idx, image_path in enumerate(images, 1):
            total_images += 1
            
            try:
                print(f"   [{img_idx}/{len(images)}] {image_path.name}...", end=" ")
                
                # Extraer datos
                filename = image_path.stem
                text_extracted = extract_text_from_image(image_path)
                color = get_dominant_color(image_path)
                categoria, subcategoria = infer_category_from_collection(collection_name)
                tipo_diseno = infer_design_type(image_path, text_extracted)
                composicion = infer_composition(text_extracted, collection_name)
                
                # Generar código (basado en nombre de archivo)
                codigo_parts = filename.split("_")
                cod_producto = f"{codigo_parts[0][:3].upper()}-{str(img_idx).zfill(3)}"
                
                # Crear producto
                producto = {
                    'ID': id_counter,
                    'Proveedor': 'KARRETEL',
                    'Marca': 'KARRETEL',
                    'Colección': collection_name,
                    'Nombre Tejido': collection_name,
                    'Cod Producto': cod_producto,
                    'Cod Color': '',
                    'Color (Inferido visualmente)': color,
                    'Color General': color,
                    'Categoría': categoria,
                    'Sub Categoría': subcategoria,
                    'Tipo Diseño': tipo_diseno,
                    'Composicion': composicion,
                    'Línea Sugerida': collection_name,
                    'Ancho_cm': 150,
                    'Gramaje_gm2': 0,
                    'Precio_Rollo': 0,
                    'Precio_Media_Rollo': 0,
                    'Precio_Corte': 0,
                    'Stock': 0,
                    'Activo': True,
                    'URL_Imagen': '',
                    'Descripcion_Completa': f"Tela {collection_name} - {tipo_diseno} - {color}",
                    'Fecha_Creacion': datetime.now().strftime('%Y-%m-%d'),
                    'Notas': text_extracted[:100] if text_extracted else ''
                }
                
                productos.append(producto)
                id_counter += 1
                processed_images += 1
                print("✓")
                
            except Exception as e:
                print(f"✗ Error: {str(e)[:50]}")
                errors += 1
    
    # Crear DataFrame y guardar
    if not productos:
        print("\n❌ No se procesaron imágenes")
        return False
    
    print("\n" + "=" * 70)
    print("📊 GENERANDO EXCEL...")
    print("=" * 70)
    
    df = pd.DataFrame(productos)
    
    # Reordenar columnas
    columnas_orden = [
        'ID', 'Proveedor', 'Marca', 'Colección', 'Nombre Tejido', 'Cod Producto',
        'Cod Color', 'Color (Inferido visualmente)', 'Color General',
        'Categoría', 'Sub Categoría', 'Tipo Diseño', 'Composicion',
        'Línea Sugerida', 'Ancho_cm', 'Gramaje_gm2',
        'Precio_Rollo', 'Precio_Media_Rollo', 'Precio_Corte',
        'Stock', 'Activo', 'URL_Imagen', 'Descripcion_Completa',
        'Fecha_Creacion', 'Notas'
    ]
    
    df = df[columnas_orden]
    df.to_excel(OUTPUT_FILE, index=False)
    
    print(f"\n✅ Archivo generado: {OUTPUT_FILE}")
    print(f"\n📊 RESUMEN:")
    print(f"   Total imágenes: {total_images}")
    print(f"   Procesadas: {processed_images}")
    print(f"   Errores: {errors}")
    print(f"   Productos en Excel: {len(df)}")
    print(f"\n   Colecciones:")
    for col in sorted(df['Colección'].unique()):
        count = len(df[df['Colección'] == col])
        print(f"      • {col}: {count}")
    
    return True

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("\n⚠️  ANTES DE EJECUTAR:")
    print("   1. Instala Tesseract: pip install pytesseract pillow numpy pandas openpyxl")
    print("   2. En Windows también: https://github.com/UB-Mannheim/tesseract/wiki")
    print("\n" + "=" * 70)
    
    input("Presiona ENTER para continuar...\n")
    
    success = process_images()
    
    if success:
        print("\n✅ ¡PROCESO COMPLETADO!")
    else:
        print("\n❌ Error en el proceso")
        sys.exit(1)
