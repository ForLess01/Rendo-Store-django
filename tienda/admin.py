from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Producto, CarritoItem

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')
        image_url = cleaned_data.get('image_url')
        
        # Ensure at least one of imagen or image_url is provided
        if not imagen and not image_url:
            raise forms.ValidationError({
                'imagen': 'Debe proporcionar una imagen o una URL de imagen.',
                'image_url': 'Debe proporcionar una imagen o una URL de imagen.'
            })
        return cleaned_data

class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm
    list_display = ('nombre', 'precio', 'stock', 'disponible', 'fecha_creacion')
    list_filter = ('disponible', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'image_preview')
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'precio', 'stock', 'disponible')
        }),
        ('Imágenes', {
            'fields': ('imagen', 'image_url', 'image_preview'),
            'description': 'Puede subir una imagen o proporcionar una URL de imagen.'
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.imagen.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.image_url)
        return "No hay imagen disponible."
    image_preview.short_description = 'Vista previa'
    
    def save_model(self, request, obj, form, change):
        # Ensure that if an image is uploaded, it takes precedence over the URL
        if 'imagen' in form.changed_data and form.cleaned_data['imagen']:
            obj.image_url = ''
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Producto, ProductoAdmin)
admin.site.register(CarritoItem)
