#!/usr/bin/env python3
"""
Script para asignar precios por colección
"""

import pdfplumber
import re
from pathlib import Path
import pandas as pd
import psycopg2

# ============================================================
# CONFIGURACIÓN
# ============================================================

PDF_FILE = Path("Lista de precios - 14-07-26.pdf")
MAESTRO_FILE = Path("MAESTRO_CON_URLS_CLOUDINARY.xlsx")
DATABASE_URL = "postgresql://postgres:SjUafZYzpKWrXzOpSDgNQISoUGTNTMYw@tokaido.proxy.rlwy.net:44666/railway"

# Mapeo: prefijo del PDF → colección del maestro
PREFIJO_A_COLECCION = {
    "1": ["VISCOSE SLUB_NEW COLLECTION", "VISCOSE SLUB"],
    "2": ["RAYON BABY TWILL -NEW COLLECTION", "RAYON BABY TWILL"],
    # Agregar más mappeos según sea necesario
}

# ============================================================
# FUNCIONES
# ============================================================

def extract_prices_by_prefix(pdf_path):
    """Extrae precios agrupados por prefijo (1-X, 2-X, etc.)"""
    precios_por_prefijo = {}
    
    print("\n🔍 Extrayendo precios del PDF por prefijo...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if not tables:
                    continue
                
                for table in tables:
                    for row in table:
                        if not row:
                            continue
                        
                        codigo_str = str(row[0]).strip() if row[0] else ""
                        codigo_match = re.search(r'^(\d+)-', codigo_str)
                        
                        if codigo_match:
                            prefijo = codigo_match.group(1)
                            
                            # Extraer precios
                            precios = []
                            for cell in row[1:]:
                                if cell:
                                    try:
                                        valor = str(cell).replace('.', '').replace(',', '.')
                                        precio = float(valor)
                                        precios.append(precio)
                                    except:
                                        pass
                            
                            if precios and prefijo not in precios_por_prefijo:
                                # Tomar el primer precio (ROLLO) como referencia
                                precios_por_prefijo[prefijo] = {
                                    'precio_rollo': precios[0],
                                    'precio_corte': precios[1] if len(precios) > 1 else precios[0]
                                }
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}
    
    print(f"✓ {len(precios_por_prefijo)} prefijos encontrados en PDF")
    for prefijo, precios in precios_por_prefijo.items():
        print(f"  Prefijo {prefijo}: Rollo=${precios['precio_rollo']} | Corte=${precios['precio_corte']}")
    
    return precios_por_prefijo

def asignar_precios_por_coleccion(maestro_path, precios_por_prefijo):
    """Asigna precios a productos por colección"""
    
    print("\n📊 Leyendo maestro y asignando precios por colección...")
    
    df = pd.read_excel(maestro_path)
    
    # Agregar columnas si no existen
    if 'precio_rollo' not in df.columns:
        df['precio_rollo'] = 0.0
    if 'precio_corte' not in df.columns:
        df['precio_corte'] = 0.0
    
    asignados = 0
    
    # Crear mapeo de colecciones
    print("\n🔍 Mapeo de colecciones:")
    for prefijo, colecciones in PREFIJO_A_COLECCION.items():
        precios = precios_por_prefijo.get(prefijo, {})
        if not precios:
            continue
        
        for coleccion in colecciones:
            # Buscar productos de esta colección
            mask = df['Colección'].str.contains(coleccion, case=False, na=False)
            cantidad = mask.sum()
            
            if cantidad > 0:
                df.loc[mask, 'precio_rollo'] = precios['precio_rollo']
                df.loc[mask, 'precio_corte'] = precios['precio_corte']
                asignados += cantidad
                
                print(f"  ✓ {coleccion} ({cantidad}): Rollo=${precios['precio_rollo']} | Corte=${precios['precio_corte']}")
    
    print(f"\n✓ Total productos con precios asignados: {asignados}")
    
    return df

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("💰 ASIGNANDO PRECIOS POR COLECCIÓN")
    print("=" * 70)
    
    # 1. Extraer precios del PDF
    if not PDF_FILE.exists():
        print(f"❌ PDF no encontrado: {PDF_FILE}")
        exit()
    
    precios_por_prefijo = extract_prices_by_prefix(PDF_FILE)
    
    if not precios_por_prefijo:
        print("❌ No se encontraron precios en el PDF")
        exit()
    
    # 2. Asignar a maestro
    if not MAESTRO_FILE.exists():
        print(f"❌ Maestro no encontrado: {MAESTRO_FILE}")
        exit()
    
    df = asignar_precios_por_coleccion(MAESTRO_FILE, precios_por_prefijo)
    
    # 3. Guardar Excel
    output = Path("MAESTRO_CON_PRECIOS_COLECCION.xlsx")
    df.to_excel(output, index=False)
    print(f"\n✅ Archivo generado: {output}")
    
    # 4. Actualizar BD
    print("\n" + "=" * 70)
    response = input("¿Actualizar precios en PostgreSQL? (s/n): ")
    
    if response.lower() == 's':
        print("\n📤 Actualizando precios en PostgreSQL...")
        
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            updated = 0
            for idx, row in df.iterrows():
                codigo = str(row['Cod Producto']).strip()
                precio_rollo = float(row.get('precio_rollo', 0) or 0)
                precio_corte = float(row.get('precio_corte', 0) or 0)
                
                if precio_rollo > 0:
                    try:
                        cursor.execute("""
                            UPDATE productos 
                            SET precio_rollo = %s, precio_corte = %s
                            WHERE cod_producto = %s
                        """, (precio_rollo, precio_corte, codigo))
                        
                        conn.commit()
                        updated += 1
                    except:
                        conn.rollback()
            
            cursor.close()
            conn.close()
            
            print(f"✓ {updated} precios actualizados en la BD")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ ¡PROCESO COMPLETADO!")
    print("=" * 70)
