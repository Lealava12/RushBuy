const API_BASE_URL = 'http://127.0.0.1:1000';
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname.includes("chackout.html")) {
        loadCheckoutItems();
    }
});

async function getUserId() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/status`, {
            method: "GET",
            credentials: "include"
        });
        
        const data = await response.json();
        
        if (data.username) { // Updated to match backend response
            sessionStorage.setItem("user_id", data.username);
            return data.username;
        } else {
            alert("Session expired. Please log in again.");
            return null;
        }
    } catch (error) {
        console.error("Error fetching user status:", error);
        alert("Failed to check user authentication. Please try again.");
        return null;
    }
}

function proceedToCheckout() {
    fetch(`${API_BASE_URL}/get-cart`, {
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data.error && data.cartItems.length > 0) {
            sessionStorage.setItem("checkoutItems", JSON.stringify(data.cartItems));
            window.location.href = "chackout.html";
        } else {
            alert("Your cart is empty.");
        }
    })
    .catch(error => {
        console.error("Error fetching cart:", error);
    });
}

function loadCheckoutItems() {
    const cartItems = JSON.parse(sessionStorage.getItem("checkoutItems")) || [];
    const checkoutTableBody = document.getElementById("checkout-table-body");
    const totalElement = document.getElementById("checkout-total");
    checkoutTableBody.innerHTML = "";
    let total = 0;

    if (cartItems.length === 0) {
        checkoutTableBody.innerHTML = "<tr><td colspan='6' class='text-center text-muted'>No items in checkout.</td></tr>";
        totalElement.textContent = "0.00";
        return;
    }

    cartItems.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        checkoutTableBody.innerHTML += `
            <tr>
                <td><img src="${item.image_url || 'default-image.jpg'}" alt="${item.name}" width="50"></td>
                <td>${item.name}</td>
                <td>₹${item.price}</td>
                <td>${item.quantity}</td>
                <td>₹${itemTotal}</td>
                <td>
                    <button class="btn btn-sm btn-danger remove-from-cart" data-id="${item.product_id}">X</button>
                </td>
            </tr>
        `;
    });

    totalElement.textContent = total.toFixed(2);
}

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove-from-cart")) {
        const productId = e.target.dataset.id;

        console.log("Sending request to remove product:", productId); // Debug log

        fetch(`${API_BASE_URL}/remove-from-cart`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => {
            console.log("Response status:", response.status); // Debug log
            return response.json();
        })
        .then(data => {
            if (response.ok) {
                console.log(data.message || "Product removed from cart."); // Debug log
                let cartItems = JSON.parse(sessionStorage.getItem("checkoutItems")) || [];
                cartItems = cartItems.filter(item => item.product_id != productId);
                sessionStorage.setItem("checkoutItems", JSON.stringify(cartItems));
                loadCheckoutItems();
            } else {
                console.error("Error removing product from cart:", data.error);
                alert(data.error || "Failed to remove product from cart. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error removing product from cart:", error);
            alert("An error occurred while removing the product. Please try again.");
        });
    }
});

function removeFromCheckout(productId) {
    let cartItems = JSON.parse(sessionStorage.getItem("checkoutItems")) || [];
    cartItems = cartItems.filter(item => item.product_id != productId);
    sessionStorage.setItem("checkoutItems", JSON.stringify(cartItems));
    loadCheckoutItems();
}

async function placeOrder() {
    try {
        const userId = await getUserId();
        if (!userId) return;

        // Use correct name selectors instead of placeholders (more reliable)
        const inputs = {
            first_name: document.querySelector('input[name="first_name"]'),
            last_name: document.querySelector('input[name="last_name"]'),
            address: document.querySelector('input[name="address"]'),
            city: document.querySelector('input[name="city"]'),
            country: document.querySelector('input[name="country"]'),
            postcode: document.querySelector('input[name="postcode"]'),
            mobile: document.querySelector('input[name="mobile"]'),
            email: document.querySelector('input[name="email"]'),
            order_notes: document.querySelector('textarea[name="order_notes"]')
        };

        // Check for missing required fields
        for (const key in inputs) {
            if (key !== "order_notes" && (!inputs[key] || !inputs[key].value.trim())) {
                alert(`Please fill in the ${key.replace("_", " ")} field.`);
                return;
            }
        }

        const paymentMethodInput = document.querySelector('input[name="payment_method"]:checked');
        const paymentMethod = paymentMethodInput ? paymentMethodInput.value : null;

        if (!paymentMethod) {
            alert("Please select a payment method before placing the order.");
            return;
        }

        const placeOrderButton = document.querySelector("button[onclick='placeOrder()']");
        placeOrderButton.disabled = true;

        const totalAmount = parseFloat(document.getElementById("checkout-total").textContent.replace(/[^\d.]/g, ''));
        const cartItems = JSON.parse(sessionStorage.getItem("checkoutItems") || "[]");

        if (cartItems.length === 0) {
            alert("Your cart is empty. Please add items before placing an order.");
            placeOrderButton.disabled = false;
            return;
        }

        const orderData = {
            user_id: userId,
            total_amount: totalAmount,
            delivery_time_preference: "No preference",
            cart_items: cartItems,
            payment_method: paymentMethod,
            first_name: inputs.first_name.value.trim(),
            last_name: inputs.last_name.value.trim(),
            address: inputs.address.value.trim(),
            city: inputs.city.value.trim(),
            country: inputs.country.value.trim(),
            postcode: inputs.postcode.value.trim(),
            mobile: inputs.mobile.value.trim(),
            email: inputs.email.value.trim(),
            order_notes: inputs.order_notes ? inputs.order_notes.value.trim() : ""
        };

        console.log("Sending order data:", orderData); // Debug log

        const response = await fetch(`${API_BASE_URL}/users/checkout`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(orderData)
        });

        const result = await response.json();

        if (response.ok) {
            alert(`Order placed successfully!\nOrder ID: ${String(result.order_id).padStart(5, '0')}\nPayment Method: ${paymentMethod}\nTotal Amount: ₹${totalAmount}`);
            sessionStorage.removeItem("checkoutItems");
            window.location.href = "index.html";
        } else {
            console.error("Server returned error:", result); // Debug
            alert(`Error placing order: ${result.error || "Unknown error"}`);
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
        console.error(error);
    } finally {
        const placeOrderButton = document.querySelector("button[onclick='placeOrder()']");
        if (placeOrderButton) placeOrderButton.disabled = false;
    }
}
