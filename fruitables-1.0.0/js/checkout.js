const API_BASE_URL = 'http://127.0.0.1:1000';
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname.includes("chackout.html")) {
        loadCheckoutItems();
    }
});

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
            window.location.href = "checkout.html";
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
        removeFromCheckout(productId);
    }
});

function removeFromCheckout(productId) {
    let cartItems = JSON.parse(sessionStorage.getItem("checkoutItems")) || [];
    cartItems = cartItems.filter(item => item.product_id != productId);
    sessionStorage.setItem("checkoutItems", JSON.stringify(cartItems));
    loadCheckoutItems();
}
// function placeOrder() {

//     const userId = sessionStorage.getItem("user_id"); 
//     if (!userId) {
//         alert("User not authenticated. Please log in first.");
//         return;
//     }
//     // Get all required form fields
//     const firstName = document.querySelector('input[placeholder="First Name"]')?.value.trim();
//     const lastName = document.querySelector('input[placeholder="Last Name"]')?.value.trim();
//     // const companyName = document.querySelector('input[placeholder="Company Name"]')?.value.trim();
//     const address = document.querySelector('input[placeholder="House Number Street Name"]')?.value.trim();
//     const city = document.querySelector('input[placeholder="Town/City"]')?.value.trim();
//     const country = document.querySelector('input[placeholder="Country"]')?.value.trim();
//     const postcode = document.querySelector('input[placeholder="Postcode/Zip"]')?.value.trim();
//     const mobile = document.querySelector('input[type="tel"]')?.value.trim();
//     const email = document.querySelector('input[type="email"]')?.value.trim();
//     const orderNotes = document.querySelector('textarea[name="text"]')?.value.trim();

//     // Validate that all required fields are filled
//     if (!firstName || !lastName || !address || !city || !country || !postcode || !mobile || !email) {
//         alert("Please fill in all required fields before placing your order.");
//         return;
//     }

//     // Get all payment method checkboxes
//     const paymentMethods = document.querySelectorAll('input[name="Transfer"], input[name="Payments"], input[name="Delivery"], input[name="Paypal"]');

//     let selectedMethod = null;

//     // Check if at least one payment method is selected
//     paymentMethods.forEach(method => {
//         if (method.checked) {
//             selectedMethod = method.value;
//         }
//     });

// //     if (!selectedMethod) {
// //         alert("Please select a payment method before placing the order.");
// //         return;
// //     }

// //     // Get the order button
// //     const placeOrderButton = document.querySelector("button[onclick='placeOrder()']");

// //     if (selectedMethod === "Delivery") { // Cash on Delivery
// //         placeOrderButton.disabled = false;

// //         // Get total amount
// //         const totalAmount = document.getElementById("checkout-total").textContent;

// //         // Simulating order placement (Replace with actual backend logic)
// //         alert(`Order placed successfully!\nPayment Method: ${selectedMethod}\nTotal Amount: ₹${totalAmount}`);

// //         // Clear checkout session
// //         sessionStorage.removeItem("checkoutItems");

// //         // Redirect to homepage or order confirmation page
// //         window.location.href = "index.html"; // Change to an order confirmation page if needed
// //     } else {
// //         placeOrderButton.disabled = true;
// //         alert(`The selected payment method (${selectedMethod}) is not available at the moment.`);
// //     }
// // }
// if (!selectedMethod) {
//     alert("Please select a payment method before placing the order.");
//     return;
// }

// // Get the order button
// const placeOrderButton = document.querySelector("button[onclick='placeOrder()']");

// if (selectedMethod === "Delivery") { // Cash on Delivery
//     placeOrderButton.disabled = false;

//     // Get total amount
//     const totalAmount = document.getElementById("checkout-total").textContent;

//     // Prepare data for backend
//     const billingData = {
//         user_id: userId,// Change this to the actual user ID from session or authentication
//         first_name: firstName,
//         last_name: lastName,
//         address: address,
//         city: city,
//         country: country,
//         postcode: postcode,
//         mobile: mobile,
//         email: email,
//         order_notes: orderNotes
//     };

//     // Send data to backend
//     try {
//         const response = await fetch('/billing', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(billingData)
//       });
//     // .then(response => response.json())
//     // .then(data => {
//         const result = await response.json();
//         if (data.message) {
//             alert(`Order placed successfully!\nPayment Method: ${selectedMethod}\nTotal Amount: ₹${totalAmount}`);
//             sessionStorage.removeItem("checkoutItems");
//             window.location.href = "index.html"; // Change to order confirmation page if needed
//         } else {
//             alert("Error placing order: " + data.error);
//         }
//     }
//     catch (error) {
//         alert("Failed to place order. Please try again.");
//         console.error(error);
//     }

// } else {
//     placeOrderButton.disabled = true;
//     alert(`The selected payment method (${selectedMethod}) is not available at the moment.`);
// }
// }

async function placeOrder() {
    // Get user ID from session storage (change this to match your auth mechanism)
    const userId = sessionStorage.getItem("user_id"); 
    if (!userId) {
        alert("User not authenticated. Please log in first.");
        return;
    }

    // Get all required form fields
    const firstName = document.querySelector('input[placeholder="First Name"]')?.value.trim();
    const lastName = document.querySelector('input[placeholder="Last Name"]')?.value.trim();
    const address = document.querySelector('input[placeholder="House Number Street Name"]')?.value.trim();
    const city = document.querySelector('input[placeholder="Town/City"]')?.value.trim();
    const country = document.querySelector('input[placeholder="Country"]')?.value.trim();
    const postcode = document.querySelector('input[placeholder="Postcode/Zip"]')?.value.trim();
    const mobile = document.querySelector('input[type="tel"]')?.value.trim();
    const email = document.querySelector('input[type="email"]')?.value.trim();
    const orderNotes = document.querySelector('textarea[name="text"]')?.value.trim();

    // Validate that all required fields are filled
    if (!firstName || !lastName || !address || !city || !country || !postcode || !mobile || !email) {
        alert("Please fill in all required fields before placing your order.");
        return;
    }

    // Get all payment method checkboxes
    const paymentMethods = document.querySelectorAll('input[name="Transfer"], input[name="Payments"], input[name="Delivery"], input[name="Paypal"]');

    let selectedMethod = null;

    // Check if at least one payment method is selected
    paymentMethods.forEach(method => {
        if (method.checked) {
            selectedMethod = method.value;
        }
    });

    if (!selectedMethod) {
        alert("Please select a payment method before placing the order.");
        return;
    }

    // Get the order button
    const placeOrderButton = document.querySelector("button[onclick='placeOrder()']");

    if (selectedMethod === "Delivery") { // Cash on Delivery
        placeOrderButton.disabled = false;

        // Get total amount
        const totalAmount = document.getElementById("checkout-total").textContent;

        // Prepare data for backend
        const billingData = {
            user_id: userId, 
            first_name: firstName,
            last_name: lastName,
            address: address,
            city: city,
            country: country,
            postcode: postcode,
            mobile: mobile,
            email: email,
            order_notes: orderNotes
        };

        try {
            const response = await fetch('/billing', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(billingData)
            });

            const result = await response.json();

            if (response.ok) {
                alert(`Order placed successfully!\nPayment Method: ${selectedMethod}\nTotal Amount: ₹${totalAmount}`);
                sessionStorage.removeItem("checkoutItems"); // Clear checkout session
                window.location.href = "index.html"; // Redirect to confirmation page
            } else {
                alert(`Error placing order: ${result.error}`);
            }
        } catch (error) {
            alert("Failed to place order. Please try again.");
            console.error(error);
        }
    } else {
        placeOrderButton.disabled = true;
        alert(`The selected payment method (${selectedMethod}) is not available at the moment.`);
    }
}
