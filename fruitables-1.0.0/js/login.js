document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".signinBx form");
    const registerForm = document.querySelector(".signupBx form");
    const API_URL = "http://127.0.0.1:1000"; // Ensure this matches your Flask API URL

    // Check if the backend server is reachable
    async function checkServerStatus() {
        try {
            const response = await fetch(`${API_URL}/`, { method: "GET" });
            if (!response.ok) {
                throw new Error("Server is not reachable");
            }
        } catch (error) {
            alert("Unable to connect to the server. Please ensure the backend is running.");
            console.error("Server connection error:", error.message);
        }
    }

    // Check if the user is already logged in
    function checkLoginStatus() {
        const userEmail = sessionStorage.getItem("userEmail");
        if (userEmail) {
            showGreeting(userEmail);
        }
    }

    // Show greeting message
    function showGreeting(email) {
        const loginButton = document.querySelector("a[href='Login.html']");
        if (loginButton) {
            loginButton.outerHTML = `<span class="text-white">Hi, ${email.split('@')[0]}</span>`;
        }
    }

    // Login form submission handler
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = loginForm.querySelector("input[type='email']").value;
        const password = loginForm.querySelector("input[type='password']").value;

        try {
            const response = await fetch(`${API_URL}/user/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
            const result = await response.json();

            if (response.ok) {
                alert(result.message || "Login successful");
                sessionStorage.setItem("userEmail", email); // Save user email in session storage
                showGreeting(email); // Replace login button with greeting
                window.location.href = result.redirect || "dashboard.html"; // Redirect to dashboard
            } else {
                alert(result.error || "Login failed");
            }
        } catch (error) {
            alert("An error occurred: " + error.message);
        }
    });

    // Registration form submission handler
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = registerForm.querySelector("input[placeholder='Full Name']").value;
        const email = registerForm.querySelector("input[placeholder='Email ']").value;
        const mobile_no = registerForm.querySelector("input[placeholder='Phone Number']").value;
        const password = registerForm.querySelector("input[placeholder=' Password']").value;
        const confirmPassword = registerForm.querySelector("input[placeholder='Confirm Password']").value;

        try {
            const response = await fetch(`${API_URL}/user/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, mobile_no, password, confirm_password: confirmPassword })
            });

            if (!response.ok) {
                const errorResult = await response.json();
                throw new Error(errorResult.error || "Registration failed");
            }

            const result = await response.json();
            alert(result.message || "Registration successful");
            showLoginForm(); // Show login form after successful registration
        } catch (error) {
            alert("An error occurred: " + error.message);
        }
    });

    // Utility function to show the login form
    function showLoginForm() {
        const loginForm = document.querySelector('.signinBx');
        const registerForm = document.querySelector('.signupBx');
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
    }

    // Utility function to show the register form
    function showRegisterForm() {
        const loginForm = document.querySelector('.signinBx');
        const registerForm = document.querySelector('.signupBx');
        registerForm.classList.add('active');
        loginForm.classList.remove('active');
    }

    // Attach event listeners for toggling forms
    document.querySelector(".signinBx .signup a").addEventListener("click", showRegisterForm);
    document.querySelector(".signupBx .signup a").addEventListener("click", showLoginForm);

    // Initialize with login form visible, check server status, and check login status
    showLoginForm();
    checkServerStatus();
    checkLoginStatus();
});