// document.addEventListener("DOMContentLoaded", async () => {
//     const API_BASE_URL = "http://192.168.29.252:1000";
//     const userId = sessionStorage.getItem("userId");

//     if (!userId) {
//         alert("Please log in to view your cart.");
//         sessionStorage.setItem("redirectAfterLogin", "cart.html");
//         window.location.href = "Login.html";
//         return;
//     }

//     try {
//         const response = await fetch(`${API_BASE_URL}/get-cart?user_id=${userId}`);
//         const result = await response.json();

//         if (response.ok) {
//             const cartItems = result.cartItems || [];
//             const cartContainer = document.querySelector(".cart-items-container");

//             if (!cartContainer) {
//                 console.error("Cart container not found in the DOM.");
//                 return;
//             }

//             cartContainer.innerHTML = ""; // Clear previous items

//             if (cartItems.length === 0) {
//                 cartContainer.innerHTML = "<p>Your cart is empty.</p>";
//                 return;
//             }

//             cartItems.forEach(item => {
//                 cartContainer.innerHTML += `
//                     <div class="cart-item">
//                         <img src="${item.image_url || 'img/default.jpg'}" alt="${item.name}">
//                         <div>
//                             <h4>${item.name}</h4>
//                             <p>Price: ₹${item.price}</p>
//                             <p>Quantity: ${item.quantity}</p>
//                         </div>
//                     </div>
//                 `;
//             });
//         } else {
//             console.error("Failed to fetch cart items:", result.error || "Unknown error");
//             alert(result.error || "Failed to load cart items. Please try again.");
//         }
//     } catch (error) {
//         console.error("Error fetching cart items:", error);
//         alert("An error occurred while loading the cart. Please try again.");
//     }
// });

