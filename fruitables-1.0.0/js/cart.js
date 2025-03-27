// Initialize cart data
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Function to add product to cart
function addToCart(product) {
    const existingProduct = cart.find(item => item.id === product.id);
    if (existingProduct) {
        existingProduct.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`${product.name} added to cart!`);
    // Redirect to cart page
    window.location.href = 'cart.html';
}

// Function to remove product from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    renderCart(); // Re-render the cart
}

// Function to render cart items on the cart page
function renderCart() {
    const cartTableBody = document.querySelector('#cart-table-body');
    const cartTotal = document.querySelector('#cart-total');
    if (!cartTableBody || !cartTotal) return;

    cartTableBody.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        cartTableBody.innerHTML += `
            <tr>
                <td><img src="${item.image}" class="img-fluid rounded-circle" style="width: 80px; height: 80px;" alt=""></td>
                <td>${item.name}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td>${item.quantity}</td>
                <td>$${itemTotal.toFixed(2)}</td>
                <td><button class="btn btn-danger btn-sm remove-from-cart" data-id="${item.id}">Remove</button></td>
            </tr>
        `;
    });

    cartTotal.textContent = `$${total.toFixed(2)}`;
}

// Event listener for "Add to Cart" buttons
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('add-to-cart')) {
        const productElement = e.target.closest('.product-item');
        const product = {
            id: productElement.dataset.id,
            name: productElement.dataset.name,
            price: parseFloat(productElement.dataset.price),
            image: productElement.dataset.image
        };
        addToCart(product);
    }
});

// Event listener for "Remove" buttons
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('remove-from-cart')) {
        const productId = e.target.dataset.id;
        removeFromCart(productId);
    }
});

// Render cart on cart page load
if (window.location.pathname.includes('cart.html')) {
    renderCart();
}
