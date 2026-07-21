import pandas as pd
from pathlib import Path

maestro = Path("MAESTRO_CON_URLS_CLOUDINARY.xlsx")

if maestro.exists():
    df = pd.read_excel(maestro)
    
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE COLUMNAS Y URLs")
    print("=" * 70)
    
    # Mostrar todas las columnas
    print(f"\n📋 Columnas del Excel ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. '{col}'")
    
    print(f"\n" + "=" * 70)
    print("🤔 ¿CUÁLES SON LOS NOMBRES QUE ESPERA TU APP?")
    print("=" * 70)
    print("""
Columnas típicas que las apps esperan:
  - Para código: 'Cod Producto', 'codigo', 'cod_producto', 'product_code'
  - Para imagen: 'URL_Imagen', 'url_imagen', 'imagen', 'image_url', 'url'
  - Para colección: 'Colección', 'coleccion', 'collection'
  
¿Las columnas de tu Excel matchean con lo que espera tu app?
    """)
    
    # Contar URLs
    urls_col = None
    for col in df.columns:
        if 'url' in col.lower() or 'imagen' in col.lower():
            urls_col = col
            break
    
    if urls_col:
        urls_validas = df[df[urls_col].notna() & (df[urls_col] != "")].shape[0]
        print(f"\n✓ Columna de URLs encontrada: '{urls_col}'")
        print(f"  Productos con URL: {urls_validas}/{len(df)}")
        
        # Ver ejemplos
        print(f"\n  Ejemplos:")
        for idx, url in enumerate(df[urls_col].head(5).values, 1):
            if url and url != "":
                print(f"    {idx}. {str(url)[:70]}...")
            else:
                print(f"    {idx}. (VACÍO)")
    else:
        print(f"\n❌ NO encontré columna de URLs")
        print(f"   Busca una columna que contenga 'url', 'imagen', 'image', etc.")
    
else:
    print(f"❌ Archivo no encontrado: {maestro}")
