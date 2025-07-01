from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.conf import settings
import json

from .models import Producto, CarritoItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ListaProductosView(ListView):
    model = Producto
    template_name = 'tienda/lista_productos.html'
    context_object_name = 'productos'
    paginate_by = 9

    def get_queryset(self):
        queryset = Producto.objects.filter(disponible=True)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query)
            )
        return queryset

class DetalleProductoView(DetailView):
    model = Producto
    template_name = 'tienda/detalle_producto.html'
    context_object_name = 'producto'

class CarritoView(View):
    template_name = 'tienda/carrito.html'

    def get(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.create()
            session_key = request.session.session_key
            items = CarritoItem.objects.none()
        else:
            session_key = request.session.session_key
            if request.user.is_authenticated:
                items = CarritoItem.objects.filter(usuario=request.user)
            else:
                items = CarritoItem.objects.filter(session_key=session_key)
        
        total = sum(item.subtotal for item in items)
        
        return render(request, self.template_name, {
            'items': items,
            'total': total,
            'cart_count': items.count()
        })

@require_http_methods(["POST"])
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # For authenticated users, check if they have the same product in their cart
    if request.user.is_authenticated:
        item, created = CarritoItem.objects.get_or_create(
            producto=producto,
            usuario=request.user,
            defaults={'cantidad': cantidad, 'session_key': session_key}
        )
        if not created:
            item.cantidad += cantidad
            item.save()
        # Get the updated cart count for the user
        cart_count = CarritoItem.objects.filter(usuario=request.user).count()
    else:
        # For anonymous users, use session key
        item, created = CarritoItem.objects.get_or_create(
            producto=producto,
            session_key=session_key,
            defaults={'cantidad': cantidad}
        )
        if not created:
            item.cantidad += cantidad
            item.save()
        # Get the updated cart count for the session
        cart_count = CarritoItem.objects.filter(session_key=session_key).count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'¡{producto.nombre} ha sido agregado al carrito!',
            'cart_count': cart_count
        })
    
    messages.success(request, f'¡{producto.nombre} ha sido agregado al carrito!')
    return redirect('tienda:carrito')

@require_http_methods(["POST"])
def actualizar_carrito(request, item_id):
    try:
        if request.user.is_authenticated:
            item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
        else:
            if not request.session.session_key:
                return JsonResponse({'success': False, 'error': 'Sesión no válida'}, status=400)
            item = get_object_or_404(CarritoItem, id=item_id, session_key=request.session.session_key)
        
        accion = request.POST.get('accion')
        
        if accion == 'aumentar':
            # Check stock before increasing quantity
            if item.cantidad >= item.producto.stock:
                return JsonResponse({
                    'success': False, 
                    'error': f'No hay suficiente stock disponible. Solo quedan {item.producto.stock} unidades.'
                }, status=400)
            item.cantidad += 1
            item.save()
                
        elif accion == 'disminuir':
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
            else:
                # If quantity would be 0, delete the item
                item.delete()
                return JsonResponse({
                    'success': True,
                    'message': 'Producto eliminado del carrito',
                    'item_deleted': True,
                    'cart_count': CarritoItem.objects.filter(
                        usuario=request.user if request.user.is_authenticated else None,
                        session_key=None if request.user.is_authenticated else request.session.session_key
                    ).count()
                })
        else:
            return JsonResponse({'success': False, 'error': 'Acción no válida'}, status=400)
        
        # Ensure subtotal is a number, not a Decimal
        subtotal = float(item.subtotal)
        
        # Get updated cart items
        if request.user.is_authenticated:
            items = CarritoItem.objects.filter(usuario=request.user)
        else:
            items = CarritoItem.objects.filter(session_key=request.session.session_key)
        
        # Calculate cart totals
        total = float(sum(i.subtotal for i in items))
        item_count = items.count()
        
        return JsonResponse({
            'success': True,
            'cantidad': item.cantidad,
            'subtotal': subtotal,
            'total': total,
            'item_count': item_count,
            'cart_count': item_count,  # For consistency with other responses
            'stock_disponible': item.producto.stock  # Add available stock to response
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["POST"])
def eliminar_del_carrito(request, item_id):
    try:
        if request.user.is_authenticated:
            item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
        else:
            if not request.session.session_key:
                return JsonResponse({'success': False, 'error': 'Sesión no válida'}, status=400)
            item = get_object_or_404(CarritoItem, id=item_id, session_key=request.session.session_key)
        
        item.delete()
        
        # Get updated cart items
        if request.user.is_authenticated:
            items = CarritoItem.objects.filter(usuario=request.user)
        else:
            items = CarritoItem.objects.filter(session_key=request.session.session_key)
        
        total = sum(item.subtotal for item in items)
        
        return JsonResponse({
            'success': True,
            'total': float(total) if total else 0,
            'item_count': items.count()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def buscar_productos(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'productos': []})
        return render(request, 'tienda/buscar_productos.html', {'productos': [], 'query': query})
    
    # Search in both name and description
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query),
        disponible=True
    ).order_by('nombre')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests (search dropdown)
        results = []
        for producto in productos[:5]:  # Limit to 5 results for dropdown
            results.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'imagen': producto.get_image_url(),
                'url': producto.get_absolute_url()
            })
        return JsonResponse({'productos': results})
    
    # For regular search page
    context = {
        'productos': productos,
        'query': query,
        'resultados_encontrados': productos.exists()
    }
    
    return render(request, 'tienda/buscar_productos.html', context)


class CheckoutView(View):
    template_name = 'tienda/checkout.html'
    
    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            items = CarritoItem.objects.filter(usuario=request.user)
        else:
            session_key = request.session.session_key
            items = CarritoItem.objects.filter(session_key=session_key)
        
        if not items.exists():
            messages.warning(request, 'Tu carrito está vacío')
            return redirect('tienda:carrito')
        
        total = sum(item.subtotal for item in items)
        
        context = {
            'items': items,
            'total': total,
            'cart_count': items.count()
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            items = CarritoItem.objects.filter(usuario=request.user)
        else:
            session_key = request.session.session_key
            items = CarritoItem.objects.filter(session_key=session_key)
        
        # In a real implementation, you would process payment here
        # For now, we'll just clear the cart
        items.delete()
        
        messages.success(request, '¡Gracias por tu compra! Tu pedido ha sido procesado con éxito.')
        return redirect('tienda:lista_productos')
