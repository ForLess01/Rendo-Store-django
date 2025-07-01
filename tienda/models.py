from django.conf import settings
from django.db import models
from django.urls import reverse

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    image_url = models.URLField('URL de la imagen', blank=True, null=True, help_text='URL de la imagen del producto (opcional si se sube una imagen)')
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tienda:detalle_producto', args=[str(self.id)])

    def get_image_url(self):
        """Return the image URL, either from the uploaded file or the URL field."""
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        elif self.image_url:
            return self.image_url
        return ''  # or a default image URL if you have one

class CarritoItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio