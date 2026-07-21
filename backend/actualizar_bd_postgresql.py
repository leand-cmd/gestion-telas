#!/usr/bin/env python3
"""
Script para actualizar imagen_url directamente en PostgreSQL
"""

import psycopg2
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURACIÓN
# ============================================================

DATABASE_URL = "postgresql://postgres:SjUafZYzpKWrXzOpSDgNQISoUGTNTMYw@tokaido.proxy.rlwy.net:44666/railway"
MAESTRO_FILE = Path("MAESTRO_CON_URLS_CLOUDINARY.xlsx")

# ============================================================
# SCRIPT
# ============================================================

print("=" * 70)
print("🚀 ACTUALIZANDO IMAGEN_URL EN POSTGRESQL")
print("=" * 70)

# 1. Conectar a PostgreSQL
print("\n1️⃣  Conectando a PostgreSQL...")
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("   ✓ Conectado a Railway PostgreSQL")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit()

# 2. Leer Excel
print("\n2️⃣  Leyendo Excel...")
if not MAESTRO_FILE.exists():
    print(f"   ❌ Archivo no encontrado: {MAESTRO_FILE}")
    exit()

df = pd.read_excel(MAESTRO_FILE)
print(f"   ✓ Maestro cargado: {len(df)} productos")

# 3. Actualizar en BD
print("\n3️⃣  Actualizando imagen_url en BD...")
print("-" * 70)

updated = 0
errors = 0
skipped = 0

for idx, row in df.iterrows():
    try:
        cod_producto = str(row['Cod Producto']).strip()
        imagen_url = row.get('imagen_url', '') or ''
        
        print(f"[{idx+1}/{len(df)}] {cod_producto}...", end=" ")
        
        if not imagen_url or imagen_url == "":
            print("(sin URL)")
            skipped += 1
            continue
        
        # Actualizar en tabla productos
        cursor.execute("""
            UPDATE productos 
            SET imagen_url = %s
            WHERE cod_producto = %s
        """, (imagen_url, cod_producto))
        
        conn.commit()
        print("✓")
        updated += 1
        
    except Exception as e:
        conn.rollback()
        print(f"✗ {str(e)[:40]}")
        errors += 1

# 4. Cerrar conexión
cursor.close()
conn.close()

# 5. Resumen
print("\n" + "=" * 70)
print("📊 RESUMEN FINAL")
print("=" * 70)
print(f"Productos actualizados: {updated}")
print(f"Sin URL (omitidos): {skipped}")
print(f"Errores: {errors}")
print("=" * 70)

if updated > 0:
    print(f"\n✅ ¡ÉXITO! {updated} imágenes actualizadas en la BD")
    print(f"   Recarga tu app (Ctrl + F5) para ver los cambios")
else:
    print(f"\n❌ No se actualizó nada")
