import pandas as pd
from pathlib import Path

# Buscar archivos Excel
excel_files = list(Path(".").glob("*.xlsx"))

print("=" * 70)
print("🔍 ARCHIVOS EXCEL ENCONTRADOS:")
print("=" * 70)

for f in excel_files:
    print(f"  • {f.name}")

# Leer el maestro
maestro_files = [f for f in excel_files if "MAESTRO" in f.name.upper()]

if maestro_files:
    maestro = maestro_files[0]
    print(f"\n✓ Usando: {maestro.name}\n")
    
    df = pd.read_excel(maestro)
    
    print("=" * 70)
    print("📋 NOMBRES EXACTOS DE COLUMNAS:")
    print("=" * 70)
    
    for i, col in enumerate(df.columns, 1):
        # Mostrar nombre exacto con comillas
        print(f"  {i}. '{col}'")
    
    # Buscar columna de imagen
    print("\n" + "=" * 70)
    print("🔎 BUSCANDO COLUMNA DE IMAGEN:")
    print("=" * 70)
    
    imagen_cols = [col for col in df.columns if 'imagen' in col.lower() or 'url' in col.lower()]
    
    if imagen_cols:
        for col in imagen_cols:
            print(f"\n✓ Encontrada: '{col}'")
            
            # Contar valores
            con_url = df[df[col].notna() & (df[col] != "")].shape[0]
            sin_url = len(df) - con_url
            
            print(f"  Con valor: {con_url}")
            print(f"  Sin valor: {sin_url}")
            
            # Ver ejemplos
            print(f"  Ejemplos:")
            for idx, (cod, url) in enumerate(df[['Cod Producto', col]].head(3).values, 1):
                if url and url != "":
                    print(f"    {idx}. {cod}: {str(url)[:60]}...")
                else:
                    print(f"    {idx}. {cod}: (VACÍO)")
    else:
        print("❌ NO encontré columna de imagen/url")
        print("   Las columnas disponibles son:")
        for col in df.columns:
            print(f"     - {col}")

else:
    print("❌ No encontré archivos MAESTRO*.xlsx")
