#!/usr/bin/env python3
"""
Script para extraer precios del PDF y actualizar maestro + PostgreSQL
"""

import pandas as pd
import pdfplumber
from pathlib import Path
import psycopg2
import re

# ============================================================
# CONFIGURACIÓN
# ============================================================

PDF_FILE = Path("Lista de precios - 14-07-26.pdf")
MAESTRO_FILE = Path("MAESTRO_CON_URLS_CLOUDINARY.xlsx")
OUTPUT_FILE = Path("MAESTRO_CON_PRECIOS.xlsx")
DATABASE_URL = "postgresql://postgres:SjUafZYzpKWrXzOpSDgNQISoUGTNTMYw@tokaido.proxy.rlwy.net:44666/railway"

# ============================================================
# FUNCIONES
# ============================================================

def extract_prices_from_pdf(pdf_path):
    """Extrae precios del PDF"""
    precios = {}
    
    print("\n🔍 Extrayendo precios del PDF...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"  Página {page_num}...", end=" ")
                
                tables = page.extract_tables()
                if not tables:
                    print("(sin tablas)")
                    continue
                
                for table in tables:
                    for row in table:
                        if not row or len(row) < 2:
                            continue
                        
                        # Buscar código (formato: X-Y o X-YY o X-YYY)
                        codigo_str = str(row[0]).strip() if row[0] else ""
                        
                        # Expresión regular para encontrar códigos
                        codigo_match = re.search(r'(\d+)-(\d+)(?:-(\d+))?', codigo_str)
                        
                        if codigo_match:
                            codigo = codigo_match.group(0)
                            
                            # Buscar precios (números con o sin decimales)
                            precios_en_fila = []
                            for cell in row[1:]:
                                if cell:
                                    try:
                                        # Limpiar y convertir
                                        valor = str(cell).replace('.', '').replace(',', '.')
                                        precio = float(valor)
                                        precios_en_fila.append(precio)
                                    except:
                                        pass
                            
                            # Asignar precios según cantidad
                            if len(precios_en_fila) >= 2:
                                precios[codigo] = {
                                    'precio_rollo': precios_en_fila[0],
                                    'precio_corte': precios_en_fila[1] if len(precios_en_fila) > 1 else precios_en_fila[0]
                                }
                
                print("✓")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return {}
    
    print(f"✓ {len(precios)} códigos con precios encontrados\n")
    return precios

def process_maestro_with_prices(maestro_path, precios_dict, output_path):
    """Actualiza maestro con precios"""
    
    print("📊 Actualizando maestro con precios...")
    
    df = pd.read_excel(maestro_path)
    
    # Agregar columnas si no existen
    if 'precio_rollo' not in df.columns:
        df['precio_rollo'] = 0.0
    if 'precio_corte' not in df.columns:
        df['precio_corte'] = 0.0
    
    matched = 0
    not_found = 0
    
    for idx, row in df.iterrows():
        codigo = str(row['Cod Producto']).strip()
        
        if codigo in precios_dict:
            df.at[idx, 'precio_rollo'] = precios_dict[codigo]['precio_rollo']
            df.at[idx, 'precio_corte'] = precios_dict[codigo]['precio_corte']
            matched += 1
            print(f"  [{idx+1}/{len(df)}] {codigo}: ✓ ${precios_dict[codigo]['precio_rollo']}")
        else:
            not_found += 1
    
    # Guardar
    df.to_excel(output_path, index=False)
    
    print(f"\n✓ Maestro actualizado: {output_path}")
    print(f"  Precios agregados: {matched}/{len(df)}")
    
    return df

def update_prices_in_db(df):
    """Actualiza precios en PostgreSQL"""
    
    print("\n📤 Actualizando precios en PostgreSQL...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        updated = 0
        
        for idx, row in df.iterrows():
            codigo = str(row['Cod Producto']).strip()
            precio_rollo = float(row.get('precio_rollo', 0) or 0)
            precio_corte = float(row.get('precio_corte', 0) or 0)
            
            print(f"  [{idx+1}/{len(df)}] {codigo}...", end=" ")
            
            try:
                cursor.execute("""
                    UPDATE productos 
                    SET precio_rollo = %s, precio_corte = %s
                    WHERE cod_producto = %s
                """, (precio_rollo, precio_corte, codigo))
                
                conn.commit()
                print("✓")
                updated += 1
                
            except Exception as e:
                conn.rollback()
                print(f"✗ {str(e)[:30]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n✓ {updated} precios actualizados en la BD")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("💰 AGREGANDO LISTA DE PRECIOS")
    print("=" * 70)
    
    # 1. Extraer precios del PDF
    if not PDF_FILE.exists():
        print(f"❌ PDF no encontrado: {PDF_FILE}")
        exit()
    
    precios = extract_prices_from_pdf(PDF_FILE)
    
    if not precios:
        print("❌ No se encontraron precios en el PDF")
        exit()
    
    # 2. Actualizar maestro
    if not MAESTRO_FILE.exists():
        print(f"❌ Maestro no encontrado: {MAESTRO_FILE}")
        exit()
    
    df = process_maestro_with_prices(MAESTRO_FILE, precios, OUTPUT_FILE)
    
    # 3. Actualizar BD
    print("\n" + "=" * 70)
    response = input("¿Actualizar precios en PostgreSQL? (s/n): ")
    
    if response.lower() == 's':
        update_prices_in_db(df)
    
    print("\n" + "=" * 70)
    print("✅ ¡PROCESO COMPLETADO!")
    print("=" * 70)
    print(f"\nArchivo generado: {OUTPUT_FILE}")
    print("Recarga la app para ver los precios")
