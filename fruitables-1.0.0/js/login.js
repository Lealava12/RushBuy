document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".signinBx form");
    const registerForm = document.querySelector(".signupBx form");
    const API_URL = "http://127.0.0.1:1000"; // Ensure this matches your Flask API URL

    // Check if the user is already logged in
    function checkLoginStatus() {
        const userName = sessionStorage.getItem("userName");
        console.log("Checking login status. UserName:", userName); // Debugging
        if (userName) {
            showGreeting(userName);
        }
    }

    // Show greeting message
    function showGreeting(userName) {
        const loginButton = document.querySelector("a[href='Login.html']");
        if (loginButton) {
            loginButton.outerHTML = `<span class="text-white">Hi, ${userName}</span>`;
            console.log("Login button replaced with greeting."); // Debugging
        } else {
            console.log("Login button not found."); // Debugging
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
                const userName = result.message.split(",")[1].trim();
                sessionStorage.setItem("userName", userName); // Save user name in session storage
                sessionStorage.setItem("userId", result.user_id); // Save user ID in session storage
                console.log("User logged in. UserName saved:", userName); // Debugging
                showGreeting(userName); // Replace login button with greeting
                window.location.href = result.redirect || "index.html"; // Redirect to index
            } else {
                alert(result.error || "Login failed");
                console.error("Login failed:", result.error); // Debugging
            }
        } catch (error) {
            alert("An error occurred: " + error.message);
            console.error("Error during login:", error); // Debugging
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
            const result = await response.json();

            if (response.ok) {
                alert(result.message || "Registration successful");
                showLoginForm(); // Show login form after successful registration
            } else {
                alert(result.error || "Registration failed");
                console.error("Registration failed:", result.error); // Debugging
            }
        } catch (error) {
            alert("An error occurred: " + error.message);
            console.error("Error during registration:", error); // Debugging
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

    // Initialize with login form visible and check login status
    showLoginForm();
    checkLoginStatus();
});