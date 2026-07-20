#!/usr/bin/env python3
# backend/scripts/upload_images_to_cloudinary.py
"""
Script para subir masivamente imágenes a Cloudinary y asignarlas a productos

Uso:
    python scripts/upload_images_to_cloudinary.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import logging

# Cargar variables de entorno
load_dotenv()

# Agregar la carpeta backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Product, ProductImage, Collection

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

class CloudinaryImageUploader:
    """Sube imágenes a Cloudinary y las asocia a productos"""
    
    def __init__(self):
        self.stats = {
            'uploaded': 0,
            'errors': 0,
            'skipped': 0
        }
    
    def get_or_create_folder_mapping(self):
        """Crear mapeo entre carpetas de imágenes y colecciones"""
        mapping = {}
        
        app = create_app()
        with app.app_context():
            collections = Collection.query.all()
            
            for collection in collections:
                # Mapear nombre de carpeta a colección
                # Ej: "ORGANIC_GARDEN" → Collection("Organic Garden")
                folder_name = collection.name.upper().replace(' ', '_').replace('-', '_')
                mapping[folder_name] = collection.id
                logger.info(f"Mapeado: {folder_name} → {collection.name}")
        
        return mapping
    
    def upload_images(self):
        """Subir todas las imágenes a Cloudinary"""
        
        images_dir = Path('./extracted_images')
        
        if not images_dir.exists():
            logger.error("❌ Carpeta 'extracted_images' no encontrada")
            return False
        
        # Obtener mapeo de carpetas
        folder_mapping = self.get_or_create_folder_mapping()
        
        app = create_app()
        with app.app_context():
            # Procesar cada carpeta de colección
            for collection_folder in sorted(images_dir.iterdir()):
                if not collection_folder.is_dir():
                    continue
                
                folder_name = collection_folder.name.upper().replace(' ', '_').replace('-', '_')
                
                logger.info(f"\n📁 Procesando carpeta: {collection_folder.name}")
                
                # Obtener colección
                collection_id = folder_mapping.get(folder_name)
                if not collection_id:
                    logger.warning(f"   ⚠️  No se encontró colección para {folder_name}")
                    continue
                
                collection = Collection.query.get(collection_id)
                products = collection.products if collection else []
                
                if not products:
                    logger.warning(f"   ⚠️  Sin productos en colección {collection.name}")
                    continue
                
                logger.info(f"   📦 Encontrados {len(products)} producto(s)")
                
                # Obtener imágenes
                images = sorted(collection_folder.glob('*.jpg'))
                
                if not images:
                    logger.warning(f"   ⚠️  Sin imágenes en carpeta")
                    continue
                
                logger.info(f"   🖼️  {len(images)} imagen(es) para subir")
                
                # Asignar imágenes a productos
                img_idx = 0
                for product in products:
                    # Cada producto obtiene 1-2 imágenes
                    for _ in range(2):
                        if img_idx >= len(images):
                            break
                        
                        image_path = images[img_idx]
                        
                        try:
                            # Subir a Cloudinary
                            logger.info(f"   ⏳ Subiendo {image_path.name}...")
                            
                            result = cloudinary.uploader.upload(
                                str(image_path),
                                folder=f'gestion-telas/products/{product.id}',
                                resource_type='auto',
                                use_filename=True,
                                unique_filename=True
                            )
                            
                            image_url = result['secure_url']
                            
                            # Guardar en BD
                            product_image = ProductImage(
                                product_id=product.id,
                                image_url=image_url,
                                alt_text=image_path.stem,
                                order=len(product.images) if product.images else 0
                            )
                            
                            db.session.add(product_image)
                            self.stats['uploaded'] += 1
                            
                            logger.info(f"   ✓ {product.code} ← {image_path.name}")
                            img_idx += 1
                        
                        except Exception as e:
                            logger.error(f"   ✗ Error con {product.code}: {e}")
                            self.stats['errors'] += 1
                    
                    db.session.commit()
            
            self.print_summary()
            return True
    
    def print_summary(self):
        """Mostrar resumen"""
        logger.info("\n" + "="*60)
        logger.info("📊 RESUMEN DE CARGA")
        logger.info("="*60)
        logger.info(f"✓ Imágenes subidas: {self.stats['uploaded']}")
        logger.info(f"✗ Errores: {self.stats['errors']}")
        logger.info(f"⊘ Omitidas: {self.stats['skipped']}")
        logger.info("="*60 + "\n")

def main():
    logger.info("🚀 Iniciando carga a Cloudinary...\n")
    
    # Verificar credenciales de Cloudinary
    if not all([
        os.getenv('CLOUDINARY_CLOUD_NAME'),
        os.getenv('CLOUDINARY_API_KEY'),
        os.getenv('CLOUDINARY_API_SECRET')
    ]):
        logger.error("❌ Faltan credenciales de Cloudinary en .env")
        logger.error("   Agrega: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET")
        sys.exit(1)
    
    uploader = CloudinaryImageUploader()
    
    if uploader.upload_images():
        logger.info("✅ Carga completada exitosamente")
        sys.exit(0)
    else:
        logger.error("❌ Error en la carga")
        sys.exit(1)

if __name__ == '__main__':
    main()
