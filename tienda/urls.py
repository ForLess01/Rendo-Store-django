from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.ListaProductosView.as_view(), name='lista_productos'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('producto/<int:pk>/', views.DetalleProductoView.as_view(), name='detalle_producto'),
    path('carrito/', views.CarritoView.as_view(), name='carrito'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
]
