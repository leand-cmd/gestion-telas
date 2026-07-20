import os
import sys
import json
from pathlib import Path

# Agregar la carpeta backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Product, ProductImage
from app.utils.upload import save_upload_file

def assign_images_automatically():
    """Asignar imágenes automáticamente basado en código de producto"""
    
    app = create_app()
    with app.app_context():
        images_dir = Path('./extracted_images')
        
        if not images_dir.exists():
            print("❌ Carpeta extracted_images no encontrada")
            return
        
        # Leer cada carpeta de colección
        for collection_dir in sorted(images_dir.iterdir()):
            if not collection_dir.is_dir():
                continue
            
            collection_name = collection_dir.name
            print(f"📁 Procesando: {collection_name}")
            
            # Obtener imágenes
            images = sorted(collection_dir.glob('*.jpg'))
            
            if not images:
                print(f"   ⚠️  Sin imágenes encontradas")
                continue
            
            # Obtener productos de esta colección
            products = Product.query.filter(
                Product.collection_id.in_(
                    db.session.query(db.func.max(Product.collection_id)).filter(
                        Product.code.like(f"{collection_name[:3]}%")
                    )
                )
            ).all()
            
            # Si no encuentra por código, buscar por nombre de colección
            if not products:
                from app.models import Collection
                collection = Collection.query.filter(
                    Collection.name.ilike(f"%{collection_name}%")
                ).first()
                if collection:
                    products = collection.products
            
            if not products:
                print(f"   ⚠️  Sin productos encontrados para {collection_name}")
                continue
            
            # Asignar imágenes
            img_idx = 0
            for product in products:
                # Asignar 1-2 imágenes por producto
                for _ in range(2):
                    if img_idx >= len(images):
                        break
                    
                    image_path = images[img_idx]
                    
                    try:
                        with open(image_path, 'rb') as f:
                            from werkzeug.datastructures import FileStorage
                            file = FileStorage(
                                stream=f,
                                filename=image_path.name,
                                content_type='image/jpeg'
                            )
                            file_url = save_upload_file(file, folder=f'products/{product.id}')
                        
                        product_image = ProductImage(
                            product_id=product.id,
                            image_url=file_url,
                            alt_text=image_path.stem,
                            order=len(product.images) if product.images else 0
                        )
                        
                        db.session.add(product_image)
                        print(f"   ✓ {product.code} ← {image_path.name}")
                        img_idx += 1
                    
                    except Exception as e:
                        print(f"   ✗ Error con {product.code}: {e}")
            
            db.session.commit()
        
        print("\n✅ Asignación completada!")

if __name__ == '__main__':
    assign_images_automatically()