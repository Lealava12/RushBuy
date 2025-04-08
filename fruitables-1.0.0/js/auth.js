document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login-form");
    const registerForm = document.querySelector("#register-form");
    const API_URL = "http://127.0.0.1:1000";
    let isCheckingLoginStatus = false;

    async function checkLoginStatus() {
        if (isCheckingLoginStatus) return;
        isCheckingLoginStatus = true;
        
        try {
            const response = await fetch(`${API_URL}/user/status`, {
                method: "GET",
                credentials: "include"
            });

            if (response.status === 401) {
                updateLoginUI(null);
                return;
            }
            
            if (!response.ok) throw new Error("Failed to fetch login status");
            const result = await response.json();

            if (result.user_id) {
                sessionStorage.setItem("userName", result.user_name);
                sessionStorage.setItem("userId", result.user_id);
                updateLoginUI(result.user_name);
            } else {
                updateLoginUI(null);
            }
        } catch (error) {
            console.error("Error checking login status:", error);
            // updateLoginUI(null);
        } finally {
            isCheckingLoginStatus = false;
        }
    }
    // Run only once
    document.addEventListener("DOMContentLoaded", checkLoginStatus);

    function updateLoginUI(userName) {
        const loginContainer = document.getElementById("login-button-container");
        if (!loginContainer) return;

        loginContainer.innerHTML = userName ?
            `<span>Hi, ${userName}</span>
             <button class="btn btn-danger" onclick="logout()">Logout</button>` :
            `<a href="Login.html" id="login-button">
                 <button class="btn btn-primary">Log In</button>
             </a>`;
    }

    async function loginUser(email, password) {
        try {
            const response = await fetch(`${API_URL}/user/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
                credentials: "include"
            });

            const result = await response.json();
            if (response.ok && result.user_name) {
                sessionStorage.setItem("userName", result.user_name);
                sessionStorage.setItem("userId", result.user_id);
                updateLoginUI(result.user_name);
                alert(`Welcome back, ${result.user_name}!`);
                setTimeout(() => window.location.href = "index.html", 500);
            } else {
                alert(result.error || "Login failed. Please try again.");
            }
        } catch (error) {
            console.error("Login error:", error);
            alert("An error occurred during login.");
        }
    }

    async function registerUser(name, email, mobile_no, password, confirmPassword) {
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }
        try {
            const response = await fetch(`${API_URL}/user/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, mobile_no, password, confirm_password: confirmPassword })
            });
            const result = await response.json();
            if (response.ok) {
                alert("Registration successful! Please log in.");
                showLoginForm();
            } else {
                alert(result.error || "Registration failed.");
            }
        } catch (error) {
            console.error("Registration error:", error);
            alert("An error occurred during registration.");
        }
    }

    async function addToCart(productId, quantity = 1) {
        const userId = sessionStorage.getItem("userId");
        if (!userId) {
            alert("Please log in to add products to the cart.");
            sessionStorage.setItem("redirectAfterLogin", "cart.html");
            window.location.href = "Login.html";
            return;
        }

        try {
            const response = await fetch(`${API_URL}/add-to-cart`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ product_id: productId, quantity }),
                credentials: "include"
            });
            
            const result = await response.json();
            if (response.ok) {
                alert(result.message || "Product added to cart!");
                window.location.href = "cart.html";
            } else {
                alert(result.error || "Failed to add product to cart. Please try again.");
            }
        } catch (error) {
            console.error("Error adding product to cart:", error);
            alert("An error occurred while adding the product to the cart. Please try again.");
        }
    }

    function logout() {
        fetch(`${API_URL}/user/logout`, { method: "POST", credentials: "include" })
            .then(() => {
                sessionStorage.clear();
                updateLoginUI(null);
                window.location.href = "index.html";
            })
            .catch(error => console.error("Logout error:", error));
    }

    checkLoginStatus();

    loginForm?.addEventListener("submit", event => {
        event.preventDefault();
        loginUser(document.querySelector("#login-email").value, document.querySelector("#login-password").value);
    });

    registerForm?.addEventListener("submit", event => {
        event.preventDefault();
        registerUser(
            document.querySelector("#register-name").value,
            document.querySelector("#register-email").value,
            document.querySelector("#register-mobile").value,
            document.querySelector("#register-password").value,
            document.querySelector("#register-confirm-password").value
        );
    });
});
// document.addEventListener("DOMContentLoaded", () => {
//     const loginForm = document.querySelector("#login-form");
//     const registerForm = document.querySelector("#register-form");
//     const API_URL = "http://127.0.0.1:1000"; // Updated API URL

//     function getAuthToken() {
//         return localStorage.getItem("authToken");
//     }

//     function updateLoginUI(userName) {
//         const loginContainer = document.getElementById("login-button-container");
//         if (!loginContainer) return;

//         loginContainer.innerHTML = userName ? `
//             <span>Hi, ${userName}</span>
//             <button class="btn btn-danger" onclick="logout()">Logout</button>
//         ` : `
//             <a href="Login.html" id="login-button">
//                 <button class="btn btn-primary">Log In</button>
//             </a>
//         `;
//     }

//     async function loginUser(email, password) {
//         try {
//             const response = await fetch(`${API_URL}/user/login`, {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ email, password })
//             });

//             const result = await response.json();
//             console.log("Login Response:", result); // Debugging log

//             if (response.ok && result.token) {
//                 localStorage.setItem("authToken", result.token);
//                 localStorage.setItem("userId", result.user_id);
//                 localStorage.setItem("name", result.message.split(", ")[1]); // Extracting name from message

//                 updateLoginUI(localStorage.getItem("name"));
//                 alert(`Welcome back, ${localStorage.getItem("name")}!`);
//                 setTimeout(() => window.location.href = "index.html", 500);
//             } else {
//                 alert(result.error || "Invalid email or password. Please try again.");
//             }
//         } catch (error) {
//             console.error("Login error:", error);
//             alert("An error occurred during login. Please check your internet connection.");
//         }
//     }

//     async function registerUser(name, email, mobile_no, password, confirmPassword) {
//         if (password !== confirmPassword) {
//             alert("Passwords do not match.");
//             return;
//         }
//         try {
//             const response = await fetch(`${API_URL}/user/register`, {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ name, email, mobile_no, password, confirm_password: confirmPassword })
//             });

//             const result = await response.json();
//             console.log("Register Response:", result); // Debugging log

//             if (response.ok) {
//                 alert("Registration successful! Please log in.");
//                 showLoginForm();
//             } else {
//                 alert(result.error || "Registration failed.");
//             }
//         } catch (error) {
//             console.error("Registration error:", error);
//             alert("An error occurred during registration.");
//         }
//     }

//     async function checkLoginStatus() {
//         const token = getAuthToken();
//         if (!token) {
//             updateLoginUI(null);
//             return;
//         }

//         try {
//             const response = await fetch(`${API_URL}/user/info`, {
//                 method: "GET",
//                 headers: { "Authorization": `Bearer ${token}` }
//             });

//             const result = await response.json();
//             console.log("User Info Response:", result); // Debugging log

//             if (response.ok && result.email) {
//                 localStorage.setItem("name", result.name);
//                 updateLoginUI(result.name);
//             } else {
//                 localStorage.clear();
//                 updateLoginUI(null);
//             }
//         } catch (error) {
//             console.error("Error checking login status:", error);
//         }
//     }

//     function logout() {
//         localStorage.clear();
//         updateLoginUI(null);
//         window.location.href = "index.html";
//     }

//     loginForm?.addEventListener("submit", event => {
//         event.preventDefault();
//         loginUser(
//             document.querySelector("#login-email").value,
//             document.querySelector("#login-password").value
//         );
//     });

//     registerForm?.addEventListener("submit", event => {
//         event.preventDefault();
//         registerUser(
//             document.querySelector("#register-name").value,
//             document.querySelector("#register-email").value,
//             document.querySelector("#register-mobile").value,
//             document.querySelector("#register-password").value,
//             document.querySelector("#register-confirm-password").value
//         );
//     });

//     checkLoginStatus();
// });
