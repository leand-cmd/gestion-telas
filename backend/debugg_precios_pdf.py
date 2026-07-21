import pdfplumber
import re
from pathlib import Path
import pandas as pd

PDF_FILE = Path("Lista de precios - 14-07-26.pdf")
MAESTRO_FILE = Path("MAESTRO_CON_URLS_CLOUDINARY.xlsx")

print("=" * 70)
print("🔍 ANALIZANDO EXTRACCIÓN DE PRECIOS DEL PDF")
print("=" * 70)

# 1. Extraer códigos del PDF
print("\n1️⃣  Leyendo PDF...")
precios_pdf = {}

try:
    with pdfplumber.open(PDF_FILE) as pdf:
        for page_num, page in enumerate(pdf.pages[:2], 1):  # Primeras 2 páginas
            print(f"  Página {page_num}:")
            
            tables = page.extract_tables()
            if not tables:
                print("    (sin tablas)")
                continue
            
            for table in tables:
                for row_num, row in enumerate(table):
                    if not row:
                        continue
                    
                    # Mostrar primeras 3 filas
                    if row_num < 3:
                        print(f"    Row {row_num}: {row}")
                    
                    codigo_str = str(row[0]).strip() if row[0] else ""
                    codigo_match = re.search(r'(\d+)-(\d+)(?:-(\d+))?', codigo_str)
                    
                    if codigo_match:
                        codigo = codigo_match.group(0)
                        
                        # Extraer precios
                        precios_en_fila = []
                        for cell in row[1:]:
                            if cell:
                                try:
                                    valor = str(cell).replace('.', '').replace(',', '.')
                                    precio = float(valor)
                                    precios_en_fila.append(precio)
                                except:
                                    pass
                        
                        if precios_en_fila:
                            precios_pdf[codigo] = precios_en_fila
                            print(f"    ✓ {codigo}: {precios_en_fila}")

except Exception as e:
    print(f"  ❌ Error: {e}")

print(f"\n  Total códigos extraídos del PDF: {len(precios_pdf)}")

# 2. Códigos del maestro
print("\n2️⃣  Leyendo maestro Excel...")
df = pd.read_excel(MAESTRO_FILE)
codigos_maestro = set(df['Cod Producto'].astype(str).str.strip().values)

print(f"  Total códigos en maestro: {len(codigos_maestro)}")

# 3. Comparar
print("\n3️⃣  COMPARANDO:")
print("=" * 70)

coincidentes = set(precios_pdf.keys()) & codigos_maestro
no_coincidentes_pdf = set(precios_pdf.keys()) - codigos_maestro
no_coincidentes_maestro = codigos_maestro - set(precios_pdf.keys())

print(f"\n✓ Códigos que coinciden: {len(coincidentes)}")
print(f"  Ejemplos:")
for codigo in list(coincidentes)[:5]:
    print(f"    - {codigo}: {precios_pdf[codigo]}")

print(f"\n❌ Códigos en PDF pero NO en maestro: {len(no_coincidentes_pdf)}")
if no_coincidentes_pdf:
    print(f"  Ejemplos:")
    for codigo in list(no_coincidentes_pdf)[:5]:
        print(f"    - {codigo}")

print(f"\n❌ Códigos en maestro pero NO en PDF: {len(no_coincidentes_maestro)}")
if no_coincidentes_maestro:
    print(f"  Ejemplos:")
    for codigo in list(no_coincidentes_maestro)[:5]:
        print(f"    - {codigo}")

print("\n" + "=" * 70)
