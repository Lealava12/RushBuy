// Initialize cart data
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Function to render cart items on the checkout page
function renderCheckout() {
    const checkoutTableBody = document.querySelector('#checkout-table-body');
    const checkoutTotal = document.querySelector('#checkout-total');
    if (!checkoutTableBody || !checkoutTotal) return;

    checkoutTableBody.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        checkoutTableBody.innerHTML += `
            <tr>
                <td><img src="${item.image}" class="img-fluid rounded-circle" style="width: 90px; height: 90px;" alt=""></td>
                <td>${item.name}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td>${item.quantity}</td>
                <td>$${itemTotal.toFixed(2)}</td>
                <td><button class="btn btn-danger btn-sm remove-from-cart" data-id="${item.id}">Remove</button></td>
            </tr>
        `;
    });

    checkoutTotal.textContent = `$${total.toFixed(2)}`;
}

// Function to remove product from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    renderCheckout(); // Re-render the checkout
    renderCart(); // Update cart page if needed
}

// Event listener for "Remove" buttons
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('remove-from-cart')) {
        const productId = e.target.dataset.id;
        removeFromCart(productId);
    }
});

// Redirect to checkout page when "Proceed Checkout" is clicked
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('proceed-checkout')) {
        // Redirect to checkout page
        window.location.href = 'chackout.html';
    }
});

// Render checkout items on page load
if (window.location.pathname.includes('chackout.html')) {
    renderCheckout();
}
