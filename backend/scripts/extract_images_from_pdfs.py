#!/usr/bin/env python3
# backend/scripts/extract_images_from_pdfs.py
"""
Script para extraer imágenes de archivos PDF

Uso:
    python scripts/extract_images_from_pdfs.py --input /ruta/a/pdfs --output /ruta/destino
    
O usar desde la carpeta correcta:
    python extract_images_from_pdfs.py --input ../path/to/pdfs --output ../extracted_images

Requisitos:
    pip install PyPDF2 pdf2image pillow
    En Linux: sudo apt-get install poppler-utils
    En macOS: brew install poppler
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

try:
    import pdf2image
    import PyPDF2
    from PIL import Image
except ImportError:
    print("❌ Dependencias faltantes. Instala con:")
    print("   pip install PyPDF2 pdf2image pillow")
    print("\nEn Linux:")
    print("   sudo apt-get install poppler-utils")
    print("\nEn macOS:")
    print("   brew install poppler")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFImageExtractor:
    """Extrae imágenes de archivos PDF"""
    
    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.stats = {
            'files_processed': 0,
            'images_extracted': 0,
            'errors': 0
        }
    
    def setup(self):
        """Preparar directorios"""
        if not self.input_dir.exists():
            logger.error(f"❌ Carpeta de entrada no existe: {self.input_dir}")
            return False
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Carpeta de salida: {self.output_dir}")
        return True
    
    def extract_images_from_pdf(self, pdf_path):
        """Extraer imágenes de un PDF específico"""
        pdf_name = pdf_path.stem
        images_found = []
        
        try:
            # Crear carpeta para imágenes de este PDF
            pdf_output = self.output_dir / pdf_name
            pdf_output.mkdir(exist_ok=True)
            
            logger.info(f"\n📄 Procesando: {pdf_path.name}")
            
            # Método 1: Convertir PDF a imágenes (screenshots)
            try:
                pages = pdf2image.convert_from_path(
                    str(pdf_path),
                    dpi=150,  # 150 DPI para calidad suficiente
                    fmt='jpeg'
                )
                
                for page_num, page in enumerate(pages, 1):
                    filename = f"{pdf_name}_page_{page_num:03d}.jpg"
                    filepath = pdf_output / filename
                    page.save(str(filepath), 'JPEG', quality=85, optimize=True)
                    images_found.append(str(filepath))
                    logger.info(f"   ✓ Página {page_num} → {filename}")
                
            except Exception as e:
                logger.warning(f"   ⚠️  No se pudieron extraer páginas: {e}")
            
            # Método 2: Extraer imágenes embebidas (si existen)
            try:
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    
                    for page_num, page in enumerate(reader.pages, 1):
                        if '/XObject' in page['/Resources']:
                            xobject = page['/Resources']['/XObject'].get_object()
                            
                            for obj_name in xobject:
                                obj = xobject[obj_name].get_object()
                                
                                if obj['/Subtype'] == '/Image':
                                    try:
                                        if '/ColorSpace' in obj:
                                            data = obj.get_data()
                                            size = (obj['/Width'], obj['/Height'])
                                            
                                            # Crear imagen desde datos crudos
                                            img = Image.frombytes('RGB', size, data)
                                            
                                            filename = f"{pdf_name}_embedded_p{page_num}_{obj_name}.jpg"
                                            filepath = pdf_output / filename
                                            img.save(str(filepath), 'JPEG', quality=90)
                                            images_found.append(str(filepath))
                                            logger.info(f"   ✓ Imagen embebida → {filename}")
                                    except Exception as e:
                                        logger.debug(f"   ⚠️  No se pudo procesar imagen: {e}")
            
            except Exception as e:
                logger.debug(f"   ⚠️  No se extrajeron imágenes embebidas: {e}")
            
            if images_found:
                logger.info(f"   ✅ {len(images_found)} imagen(es) extraída(s)")
                return images_found
            else:
                logger.warning(f"   ⚠️  Sin imágenes encontradas")
                return []
        
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            self.stats['errors'] += 1
            return []
    
    def process_all(self):
        """Procesar todos los PDFs en la carpeta"""
        pdf_files = list(self.input_dir.glob('*.pdf'))
        
        if not pdf_files:
            logger.error("❌ No se encontraron archivos PDF")
            return False
        
        logger.info(f"📁 Encontrados {len(pdf_files)} PDF(s)")
        logger.info(f"📸 Extrayendo imágenes...\n")
        
        for pdf_path in sorted(pdf_files):
            images = self.extract_images_from_pdf(pdf_path)
            self.stats['files_processed'] += 1
            self.stats['images_extracted'] += len(images)
        
        self.print_summary()
        return True
    
    def print_summary(self):
        """Mostrar resumen de extracción"""
        logger.info("\n" + "="*60)
        logger.info("📊 RESUMEN DE EXTRACCIÓN")
        logger.info("="*60)
        logger.info(f"✓ PDFs procesados: {self.stats['files_processed']}")
        logger.info(f"✓ Imágenes extraídas: {self.stats['images_extracted']}")
        logger.info(f"✗ Errores: {self.stats['errors']}")
        logger.info(f"📁 Salida: {self.output_dir.absolute()}")
        logger.info("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description='Extraer imágenes de archivos PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python extract_images_from_pdfs.py --input ./pdfs --output ./images
  python extract_images_from_pdfs.py -i ~/Downloads/catalogos -o ./extracted
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Carpeta con PDFs de entrada'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Carpeta para guardar imágenes extraídas'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=150,
        help='DPI para conversión de PDF a imagen (default: 150)'
    )
    
    args = parser.parse_args()
    
    extractor = PDFImageExtractor(args.input, args.output)
    
    if not extractor.setup():
        sys.exit(1)
    
    if extractor.process_all():
        logger.info("✅ Extracción completada")
        sys.exit(0)
    else:
        logger.error("❌ Error en la extracción")
        sys.exit(1)

if __name__ == '__main__':
    main()
