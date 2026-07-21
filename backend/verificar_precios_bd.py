import psycopg2

DATABASE_URL = "postgresql://postgres:SjUafZYzpKWrXzOpSDgNQISoUGTNTMYw@tokaido.proxy.rlwy.net:44666/railway"

print("=" * 70)
print("🔍 VERIFICANDO PRECIOS EN POSTGRESQL")
print("=" * 70)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Ver primeros 10 productos con precios
    cursor.execute("""
        SELECT cod_producto, precio_rollo, precio_corte 
        FROM productos 
        LIMIT 10
    """)
    
    resultados = cursor.fetchall()
    
    print(f"\nPrimeros 10 productos:\n")
    for cod, precio_rollo, precio_corte in resultados:
        print(f"  {cod}: Rollo=${precio_rollo} | Corte=${precio_corte}")
    
    # Contar cuántos tienen precios
    cursor.execute("""
        SELECT COUNT(*) as con_precio, 
               COUNT(CASE WHEN precio_rollo > 0 THEN 1 END) as con_precio_rollo,
               COUNT(CASE WHEN precio_corte > 0 THEN 1 END) as con_precio_corte
        FROM productos
    """)
    
    con_precio, con_rollo, con_corte = cursor.fetchone()
    
    print(f"\n" + "=" * 70)
    print(f"📊 RESUMEN:")
    print("=" * 70)
    print(f"Total productos: {con_precio}")
    print(f"Con precio_rollo > 0: {con_rollo}")
    print(f"Con precio_corte > 0: {con_corte}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
