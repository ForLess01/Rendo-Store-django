document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-to-cart-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            const messageDiv = document.getElementById('add-to-cart-message');
            
            // Disable the submit button to prevent multiple submissions
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Añadiendo...';
            
            // Clear any previous messages
            if (messageDiv) {
                messageDiv.textContent = '';
                messageDiv.classList.add('hidden');
            }
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the cart count
                    if (typeof updateCartCount === 'function') {
                        updateCartCount(data.cart_count);
                    }
                    
                    // Show success message
                    if (messageDiv) {
                        messageDiv.textContent = data.message;
                        messageDiv.classList.remove('hidden');
                        messageDiv.classList.remove('text-red-600');
                        messageDiv.classList.add('text-green-600');
                    }
                    
                    // Reset the form after a short delay
                    setTimeout(() => {
                        form.reset();
                    }, 1000);
                } else {
                    throw new Error(data.message || 'Error al agregar al carrito');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (messageDiv) {
                    messageDiv.textContent = error.message || 'Error al agregar al carrito';
                    messageDiv.classList.remove('hidden');
                    messageDiv.classList.remove('text-green-600');
                    messageDiv.classList.add('text-red-600');
                }
            })
            .finally(() => {
                // Re-enable the submit button
                submitButton.disabled = false;
                submitButton.innerHTML = '<i class="fas fa-cart-plus mr-2"></i> Añadir al carrito';
                
                // Hide the message after 3 seconds
                if (messageDiv) {
                    setTimeout(() => {
                        messageDiv.classList.add('hidden');
                    }, 3000);
                }
            });
        });
    }
});
