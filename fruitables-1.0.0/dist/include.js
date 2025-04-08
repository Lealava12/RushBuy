document.addEventListener("DOMContentLoaded", async function () {
    // Function to load external HTML components
    const loadComponent = async (url, elementId) => {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to load ${url}: ${response.statusText}`);
            
            const element = document.getElementById(elementId);
            if (!element) throw new Error(`Element with ID '${elementId}' not found.`);
            
            element.innerHTML = await response.text();
        } catch (error) {
            console.error(`Error loading ${url}:`, error);
        }
    };

    // Include sidebar, header, footer, and nav
    await loadComponent("sidebar.html", "sidebar-container");
    // await loadComponent("header.html", "header-container");
    // await loadComponent("footer.html", "footer-container");
    // await loadComponent("nav.html", "nav-container");

    // Initialize logout functionality after components are loaded
    initializeLogout();
});

// const API_BASE_URL = 'http://127.0.0.1:1000';
console.log("Logout script loaded");

function initializeLogout() {
    const logoutButton = document.getElementById("logout");

    if (!logoutButton) {
        console.error("Logout button not found.");
        return;
    }

    console.log("Logout button found");

    logoutButton.addEventListener("click", async function (event) {
        event.preventDefault(); // Stop page refresh
        console.log("Logout button clicked"); // Debugging log

        try {
            const response = await fetch(`${API_BASE_URL}/logout`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Logout request failed.");
            }

            const data = await response.json();
            console.log("Server Response:", data); // Log response from backend

            alert(data.message); // Show logout success message
            sessionStorage.clear(); // Clear session storage
            localStorage.clear(); // Clear local storage if used
            window.location.href = data.redirect; // Redirect to login page
        } catch (error) {
            console.error("Error during logout:", error);
            alert("An error occurred while logging out. Please try again.");
        }
    });
}
