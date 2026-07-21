import requests
from pathlib import Path

BASE_URL = "https://gestion-telas-production.up.railway.app"
EMAIL = "aracellipaciellobaez@gmail.com"
PASSWORD = "123456789"

# Login
print("Iniciando login...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"email": EMAIL, "password": PASSWORD},
    verify=False
)

if response.status_code != 200:
    print(f"ERROR: {response.status_code}")
    exit()

token = response.json()["token"]
print("OK: Login exitoso\n")

headers = {"Authorization": f"Bearer {token}"}

# Procesar cada carpeta como colección
images_base = Path("extracted_images")

print("Creando productos y subiendo imágenes...\n")
created_products = 0
uploaded_images = 0
errors = 0

for folder_path in sorted(images_base.iterdir()):
    if not folder_path.is_dir():
        continue
    
    collection_name = folder_path.name
    images = sorted(folder_path.glob("*.jpg"))
    
    if not images:
        print(f"SKIP: {collection_name} (sin imagenes)")
        continue
    
    print(f"PROC: {collection_name}")
    
    # Determinar cuántos productos crear basado en cantidad de imágenes
    # Máximo 2-3 imágenes por producto
    num_products = max(1, len(images) // 2)
    if num_products > 5:
        num_products = 5  # Máximo 5 productos por colección
    
    print(f"  → Creando {num_products} producto(s)...")
    
    created_product_ids = []
    
    for i in range(num_products):
        # Generar código del producto
        code = f"{collection_name[:3].upper()}-{str(i+1).zfill(3)}"
        
        # Crear producto
        try:
            prod_data = {
                "codigo": code,
                "nombre": f"{collection_name} #{i+1}",
                "descripcion": f"Producto de {collection_name}",
                "precio": 0,  # Será actualizado después
                "stock": 0
            }
            
            prod_response = requests.post(
                f"{BASE_URL}/api/productos",
                json=prod_data,
                headers=headers,
                verify=False
            )
            
            if prod_response.status_code in [200, 201]:
                product = prod_response.json()
                product_id = product.get("id")
                created_product_ids.append(product_id)
                print(f"    ✓ Producto {code} (ID: {product_id})")
                created_products += 1
            else:
                print(f"    ✗ Error creando {code}: {prod_response.status_code}")
                errors += 1
        
        except Exception as e:
            print(f"    ✗ Error: {str(e)[:50]}")
            errors += 1
    
    # Subir imágenes a los productos creados
    if created_product_ids:
        print(f"  → Subiendo {len(images)} imagen(es)...")
        
        img_idx = 0
        for product_id in created_product_ids:
            # Máximo 2-3 imágenes por producto
            for _ in range(3):
                if img_idx >= len(images):
                    break
                
                image = images[img_idx]
                
                try:
                    with open(image, "rb") as f:
                        files = {"file": f}
                        data = {"alt_text": image.stem}
                        
                        upload_response = requests.post(
                            f"{BASE_URL}/api/uploads/product/{product_id}",
                            files=files,
                            data=data,
                            headers=headers,
                            verify=False
                        )
                    
                    if upload_response.status_code in [200, 201]:
                        print(f"    ✓ {image.name}")
                        uploaded_images += 1
                    else:
                        print(f"    ✗ {image.name} ({upload_response.status_code})")
                        errors += 1
                    
                    img_idx += 1
                
                except Exception as e:
                    print(f"    ✗ Error: {str(e)[:50]}")
                    errors += 1
    
    print()

print("="*60)
print(f"RESUMEN FINAL")
print("="*60)
print(f"Productos creados: {created_products}")
print(f"Imagenes subidas: {uploaded_images}")
print(f"Errores: {errors}")
print("="*60)
print(f"\n✅ Proceso completado!")
