// document.addEventListener("DOMContentLoaded", () => {
//     const loginForm = document.querySelector(".signinBx form");
//     const registerForm = document.querySelector(".signupBx form");
//     const API_URL = "http://127.0.0.1:1000"; // Ensure this matches your Flask API URL

//     // Check if the user is already logged in
//     async function checkLoginStatus() {
//         try {
//             const response = await fetch(`${API_URL}/user/login`, {
//                 method: "GET",
//                 credentials: "include" // Send cookies with the request
//             });

//             if (!response.ok) throw new Error("Failed to fetch login status");

//             const result = await response.json();
//             if (result.user_id && result.user_name) {
//                 sessionStorage.setItem("userName", result.user_name);
//                 sessionStorage.setItem("userId", result.user_id);
//                 updateSlidebarLoginUI(result.user_name);
//             } else {
//                 updateSlidebarLoginUI(null); // Reset to default login button
//             }
//         } catch (error) {
//             console.error("Error checking login status:", error);
//             updateSlidebarLoginUI(null); // Reset to default login button in case of error
//         }
//     }

//     // Update the login button in slidebar.html
//     function updateSlidebarLoginUI(userName) {
//         const loginButtonContainer = document.getElementById("login-button-container");
//         if (loginButtonContainer) {
//             if (userName) {
//                 loginButtonContainer.innerHTML = `
//                     <span class="text-dark my-auto">Hi, ${userName}</span>
//                     <a href="#" id="logout-button" class="btn btn-danger ms-3">Logout</a>
//                 `;

//                 // Add logout functionality
//                 const logoutButton = document.getElementById("logout-button");
//                 logoutButton.addEventListener("click", async (e) => {
//                     e.preventDefault();
//                     await logoutUser();
//                 });
//             } else {
//                 loginButtonContainer.innerHTML = `
//                     <a href="Login.html" class="my-auto" id="login-button">
//                         <button class="btn btn-primary">Log In</button>
//                     </a>
//                 `;
//             }
//         } else {
//             console.error("Login button container not found.");
//         }
//     }

//     // Logout user
//     async function logoutUser() {
//         try {
//             const response = await fetch(`${API_URL}/logout`, {
//                 method: "POST",
//                 credentials: "include" // Send cookies with the request
//             });

//             if (response.ok) {
//                 sessionStorage.clear(); // Clear session storage
//                 updateSlidebarLoginUI(null); // Reset to default login button
//                 window.location.href = "Login.html"; // Redirect to login page
//             } else {
//                 alert("Failed to log out. Please try again.");
//             }
//         } catch (error) {
//             console.error("Error logging out:", error);
//         }
//     }

//     // User Login Function
//     async function loginUser(email, password) {
//         try {
//             const response = await fetch(`${API_URL}/user/login`, {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ email, password }),
//                 credentials: "include" // Send cookies with the request
//             });

//             const result = await response.json();

//             if (response.ok && result.user_name) {
//                 sessionStorage.setItem("userName", result.user_name);
//                 sessionStorage.setItem("userId", result.user_id);
//                 alert(`Welcome back, ${result.user_name}!`);
//                 updateSlidebarLoginUI(result.user_name);

//                 if (sessionStorage.getItem("redirectAfterLogin")) {
//                     const redirectPage = sessionStorage.getItem("redirectAfterLogin");
//                     sessionStorage.removeItem("redirectAfterLogin");
//                     window.location.href = redirectPage;
//                 } else {
//                     window.location.href = result.redirect || "index.html";
//                 }
//             } else {
//                 alert(result.error || "Failed to log in. Please try again.");
//             }
//         } catch (error) {
//             console.error("Error during login:", error);
//             alert("An error occurred during login. Please try again.");
//         }
//     }

//     // Login form submission handler
//     loginForm.addEventListener("submit", (event) => {
//         event.preventDefault();

//         const email = loginForm.querySelector("input[type='email']").value;
//         const password = loginForm.querySelector("input[type='password']").value;

//         loginUser(email, password);
//     });

//     // Registration form submission handler
//     registerForm.addEventListener("submit", async (event) => {
//         event.preventDefault();

//         const name = registerForm.querySelector("input[placeholder='Full Name']").value;
//         const email = registerForm.querySelector("input[placeholder='Email ']").value;
//         const mobile_no = registerForm.querySelector("input[placeholder='Phone Number']").value;
//         const password = registerForm.querySelector("input[placeholder=' Password']").value;
//         const confirmPassword = registerForm.querySelector("input[placeholder='Confirm Password']").value;

//         if (password !== confirmPassword) {
//             alert("Passwords do not match. Please try again.");
//             return;
//         }

//         try {
//             const response = await fetch(`${API_URL}/user/register`, {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ name, email, mobile_no, password })
//             });

//             const result = await response.json();

//             if (response.ok) {
//                 alert(result.message || "Registration successful");
//                 showLoginForm();
//             } else {
//                 alert(result.error || "Registration failed");
//             }
//         } catch (error) {
//             console.error("Error during registration:", error);
//             alert("An error occurred during registration. Please try again.");
//         }
//     });

//     // Utility function to show the login form
//     function showLoginForm() {
//         const loginForm = document.querySelector('.signinBx');
//         const registerForm = document.querySelector('.signupBx');
//         loginForm.classList.add('active');
//         registerForm.classList.remove('active');
//     }

//     // Utility function to show the register form
//     function showRegisterForm() {
//         const loginForm = document.querySelector('.signinBx');
//         const registerForm = document.querySelector('.signupBx');
//         registerForm.classList.add('active');
//         loginForm.classList.remove('active');
//     }

//     // Attach event listeners for toggling forms
//     document.querySelector(".signinBx .signup a").addEventListener("click", showRegisterForm);
//     document.querySelector(".signupBx .signup a").addEventListener("click", showLoginForm);

//     // Initialize with login form visible and check login status
//     showLoginForm();
//     checkLoginStatus();

//     // Ensure slidebar login button updates if sessionStorage already has userName
//     if (sessionStorage.getItem("userName")) {
//         updateSlidebarLoginUI(sessionStorage.getItem("userName"));
//     }
// });
//     const API_URL = 'http://127.0.0.1:1000';

// document.addEventListener("DOMContentLoaded", async function () {
//     const authContainer = document.querySelector(".d-flex.m-3.me-0");

//     try {
//         const response = await fetch(`${API_URL}/user/profile`, {
//             method: "GET",
//             headers: { "Content-Type": "application/json" },
//             credentials: "include"
//         });

//         const data = await response.json();
//         if (response.ok && data.message) {
//             authContainer.innerHTML = `
//                 <button class="btn btn-primary me-2">Hi, ${data.message.split(", ")[1]}</button>
//                 <button onclick="logout()" class="btn btn-danger">Logout</button>
//             `;
//         } else {
//             authContainer.innerHTML = `
//                 <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#authModal">Log In</button>
//             `;
//         }
//     } catch (error) {
//         console.error("Error fetching user profile:", error);
//     }

//     // Login Form Submission
//     document.querySelector("#login-form").addEventListener("submit", async function (event) {
//         event.preventDefault();
//         const email = document.querySelector("#login-email").value;
//         const password = document.querySelector("#login-password").value;

//         const response = await fetch(`${API_URL}/user/login`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             credentials: "include",
//             body: JSON.stringify({ email, password })
//         });

//         const data = await response.json();
//         if (response.ok) {
//             alert("Login successful");
//             location.reload();
//         } else {
//             alert(data.error);
//         }
//     });

//     // Registration Form Submission
//     document.querySelector("#register-form").addEventListener("submit", async function (event) {
//         event.preventDefault();
//         const name = document.querySelector("#register-name").value;
//         const email = document.querySelector("#register-email").value;
//         const mobile = document.querySelector("#register-mobile").value;
//         const password = document.querySelector("#register-password").value;
//         const confirmPassword = document.querySelector("#register-confirm-password").value;

//         if (password !== confirmPassword) {
//             alert("Passwords do not match!");
//             return;
//         }

//         const response = await fetch(`${API_URL}/user/signup`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ name, email, mobile, password })
//         });

//         const data = await response.json();
//         if (response.ok) {
//             alert("Registration successful");
//             location.reload();
//         } else {
//             alert(data.error);
//         }
//     });
// });

// // Logout Function
// async function logout() {
//     const response = await fetch(`${API_URL}/user/logout`, { method: "POST", credentials: "include" });
//     if (response.ok) {
//         alert("Logged out successfully");
//         location.reload();
//     } else {
//         alert("Logout failed");
//     }
// }

// // Toggle Forms
// function showRegisterForm() {
//     document.querySelector('.signinBx').classList.remove('active');
//     document.querySelector('.signupBx').classList.add('active');
// }

// function showLoginForm() {
//     document.querySelector('.signupBx').classList.remove('active');
//     document.querySelector('.signinBx').classList.add('active');
// }

