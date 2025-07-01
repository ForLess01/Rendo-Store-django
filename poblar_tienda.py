import os
import django
from django.core.files import File
from django.core.files.images import ImageFile

def poblar_tienda():
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()
    
    from tienda.models import Producto
    
    # Crear directorio de imágenes si no existe
    os.makedirs('media/productos', exist_ok=True)
    
    # Lista de productos de ejemplo
    productos = [
        {
            'nombre': 'Laptop HP Pavilion',
            'descripcion': 'Laptop HP Pavilion 15.6" Intel Core i5 12GB RAM 1TB HDD',
            'precio': 2499.99,
            'imagen': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'stock': 10
        },
        {
            'nombre': 'Smartphone Samsung Galaxy S21',
            'descripcion': 'Smartphone Samsung Galaxy S21 5G 128GB 8GB RAM',
            'precio': 3299.99,
            'imagen': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e9c0?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'stock': 15
        },
        {
            'nombre': 'Auriculares Sony WH-1000XM4',
            'descripcion': 'Auriculares inalámbricos con cancelación de ruido',
            'precio': 1299.99,
            'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'stock': 20
        },
        {
            'nombre': 'Smart TV 55" 4K UHD',
            'descripcion': 'Smart TV LG 55" 4K UHD con HDR y WebOS',
            'precio': 2899.99,
            'imagen': 'https://images.unsplash.com/photo-1522869632220-1a335355c1f6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'stock': 8
        },
        {
            'nombre': 'Tablet Samsung Galaxy Tab S7',
            'descripcion': 'Tablet Samsung Galaxy Tab S7 11" 128GB 6GB RAM',
            'precio': 2199.99,
            'imagen': 'https://images.unsplash.com/photo-1542751110-9e68f84f0ce6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'stock': 12
        }
    ]
    
    # Descargar imágenes y crear productos
    import requests
    from io import BytesIO
    
    for producto_data in productos:
        # Verificar si el producto ya existe
        if not Producto.objects.filter(nombre=producto_data['nombre']).exists():
            print(f"Creando producto: {producto_data['nombre']}")
            
            # Descargar la imagen
            response = requests.get(producto_data['imagen'])
            if response.status_code == 200:
                # Crear el objeto de imagen
                img_name = f"{producto_data['nombre'].lower().replace(' ', '_')}.jpg"
                img_path = f"productos/{img_name}"
                
                # Guardar la imagen en el sistema de archivos
                with open(f"media/{img_path}", 'wb') as f:
                    f.write(response.content)
                
                # Crear el producto
                producto = Producto(
                    nombre=producto_data['nombre'],
                    descripcion=producto_data['descripcion'],
                    precio=producto_data['precio'],
                    stock=producto_data['stock'],
                    disponible=True
                )
                
                # Asignar la imagen al producto
                with open(f"media/{img_path}", 'rb') as f:
                    producto.imagen.save(img_name, File(f), save=True)
                
                producto.save()
                print(f"Producto creado: {producto.nombre}")
            else:
                print(f"Error al descargar la imagen para {producto_data['nombre']}")
        else:
            print(f"El producto {producto_data['nombre']} ya existe")

if __name__ == '__main__':
    poblar_tienda()
