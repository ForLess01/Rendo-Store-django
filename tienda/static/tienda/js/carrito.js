// Función para actualizar el contador del carrito
function actualizarContadorCarrito() {
    // Si el usuario está autenticado, obtenemos los items del carrito del usuario
    // Si no, usamos la sesión actual
    const url = '{% if user.is_authenticated %}{% url "tienda:carrito_json" %}{% else %}{% url "tienda:carrito_session_json" %}{% endif %}';
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const totalItems = data.items.reduce((total, item) => total + item.cantidad, 0);
            document.getElementById('cart-count').textContent = totalItems;
        })
        .catch(error => console.error('Error al actualizar el contador del carrito:', error));
}

// Función para agregar un producto al carrito
function agregarAlCarrito(productoId, cantidad = 1) {
    const url = `{% url 'tienda:agregar_al_carrito' 0 %}`.replace('0', productoId);
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `cantidad=${cantidad}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            actualizarContadorCarrito();
            mostrarNotificacion('Producto agregado al carrito', 'success');
        } else {
            mostrarNotificacion(data.message || 'Error al agregar al carrito', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error en la conexión', 'error');
    });
}

// Función para actualizar la cantidad de un producto en el carrito
function actualizarCantidad(itemId, accion) {
    const cantidadElement = document.getElementById(`cantidad-${itemId}`);
    const subtotalElement = document.getElementById(`subtotal-${itemId}`);
    const totalElement = document.getElementById('total-carrito');
    
    // Mostrar indicador de carga
    const originalHTML = cantidadElement.innerHTML;
    cantidadElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    const url = `{% url 'tienda:actualizar_carrito' 0 %}`.replace('0', itemId);
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `accion=${accion}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            mostrarNotificacion(data.error, 'error');
            cantidadElement.innerHTML = originalHTML;
            return;
        }
        
        // Actualizar la interfaz
        cantidadElement.textContent = data.cantidad;
        subtotalElement.textContent = data.subtotal.toFixed(2);
        totalElement.textContent = data.total.toFixed(2);
        
        // Actualizar contador del carrito
        actualizarContadorCarrito();
        
        // Si la cantidad es 0, eliminar la fila
        if (data.cantidad === 0) {
            document.querySelector(`[data-item-id="${itemId}"]`).remove();
            
            // Si no hay más items, recargar la página
            if (document.querySelectorAll('[data-item-id]').length === 0) {
                window.location.reload();
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al actualizar el carrito', 'error');
        cantidadElement.innerHTML = originalHTML;
    });
}

// Función para eliminar un producto del carrito
function eliminarDelCarrito(itemId) {
    if (!confirm('¿Estás seguro de que deseas eliminar este producto del carrito?')) {
        return;
    }
    
    const url = `{% url 'tienda:eliminar_del_carrito' 0 %}`.replace('0', itemId);
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Eliminar la fila de la tabla
            document.querySelector(`[data-item-id="${itemId}"]`).remove();
            
            // Actualizar total
            document.getElementById('total-carrito').textContent = data.total.toFixed(2);
            
            // Actualizar contador del carrito
            actualizarContadorCarrito();
            
            // Mostrar notificación
            mostrarNotificacion('Producto eliminado del carrito', 'success');
            
            // Si no hay más items, recargar la página
            if (document.querySelectorAll('[data-item-id]').length === 0) {
                window.location.reload();
            }
        } else {
            mostrarNotificacion(data.message || 'Error al eliminar el producto', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error en la conexión', 'error');
    });
}

// Función auxiliar para obtener el valor de una cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Verificar si ya existe un contenedor de notificaciones
    let container = document.getElementById('notificaciones');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notificaciones';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '1000';
        document.body.appendChild(container);
    }
    
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `p-4 mb-2 rounded-md shadow-lg ${
        tipo === 'success' ? 'bg-green-100 text-green-800 border border-green-200' :
        tipo === 'error' ? 'bg-red-100 text-red-800 border border-red-200' :
        'bg-blue-100 text-blue-800 border border-blue-200'
    }`;
    notificacion.textContent = mensaje;
    
    // Agregar la notificación al contenedor
    container.appendChild(notificacion);
    
    // Eliminar la notificación después de 5 segundos
    setTimeout(() => {
        notificacion.style.opacity = '0';
        notificacion.style.transition = 'opacity 0.5s';
        setTimeout(() => {
            notificacion.remove();
            // Si no hay más notificaciones, eliminar el contenedor
            if (container.children.length === 0) {
                container.remove();
            }
        }, 500);
    }, 5000);
}

// Inicializar el contador del carrito cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    actualizarContadorCarrito();
});
