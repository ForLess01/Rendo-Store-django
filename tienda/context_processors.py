from .models import CarritoItem

def carrito_count(request):
    """
    Context processor that adds the cart item count to all templates.
    """
    if not request.session.session_key:
        return {'cart_count': 0}
    
    session_key = request.session.session_key
    if request.user.is_authenticated:
        count = CarritoItem.objects.filter(usuario=request.user).count()
    else:
        count = CarritoItem.objects.filter(session_key=session_key).count()
    
    return {'cart_count': count}
