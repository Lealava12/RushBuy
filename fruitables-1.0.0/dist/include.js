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

    const sidebar = document.querySelector(".sidebar");
    const toggleButton = document.getElementById("toggle-sidebar");
    const closeButton = document.querySelector(".close-aside");

    // Function to check screen size and adjust sidebar visibility
    const adjustSidebarVisibility = () => {
        if (window.innerWidth <= 768) {
            // Hide sidebar by default on mobile
            sidebar.classList.remove("open");
            toggleButton.style.display = "block"; // Show toggle button
        } else {
            // Show sidebar by default on larger screens
            sidebar.classList.add("open");
            toggleButton.style.display = "none"; // Hide toggle button
        }
    };

    // Add event listener for window resize to adjust sidebar visibility
    window.addEventListener("resize", adjustSidebarVisibility);

    // Initial check for sidebar visibility
    adjustSidebarVisibility();

    // Open sidebar when toggle button is clicked
    if (toggleButton) {
        toggleButton.addEventListener("click", () => {
            sidebar.classList.add("open");
        });
    }

    // Close sidebar when close button is clicked
    if (closeButton) {
        closeButton.addEventListener("click", () => {
            sidebar.classList.remove("open");
        });
    }
});

// const API_BASE_URL = 'http://lealavaecommerce.com/api';
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

            showAlert(data.message); // Show logout success message
            sessionStorage.clear(); // Clear session storage
            localStorage.clear(); // Clear local storage if used
            window.location.href = data.redirect; // Redirect to login page
        } catch (error) {
            console.error("Error during logout:", error);
            showAlert("An error occurred while logging out. Please try again.");
        }
    });
}

function showAlert(message) {
    const alertOverlay = document.createElement("div");
    const alertBox = document.createElement("div");
    const alertMessage = document.createElement("p");
    const closeButton = document.createElement("button");

    // Overlay styles
    alertOverlay.style.position = "fixed";
    alertOverlay.style.top = 0;
    alertOverlay.style.left = 0;
    alertOverlay.style.width = "100%";
    alertOverlay.style.height = "100%";
    alertOverlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    alertOverlay.style.display = "flex";
    alertOverlay.style.alignItems = "center";
    alertOverlay.style.justifyContent = "center";
    alertOverlay.style.zIndex = 1000;

    // Alert box styles
    alertBox.style.backgroundColor = "#fff";
    alertBox.style.padding = "20px";
    alertBox.style.borderRadius = "8px";
    alertBox.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
    alertBox.style.textAlign = "center";
    alertBox.style.width = "400px"; // Default width for larger screens
    alertBox.style.maxWidth = "90%"; // Ensure it fits smaller screens

    // Alert message styles
    alertMessage.textContent = message;
    alertMessage.style.marginBottom = "20px";
    alertMessage.style.fontSize = "1rem"; // Default font size

    // Close button styles
    closeButton.textContent = "OK";
    closeButton.style.padding = "10px 20px";
    closeButton.style.backgroundColor = "#007bff";
    closeButton.style.color = "#fff";
    closeButton.style.border = "none";
    closeButton.style.borderRadius = "5px";
    closeButton.style.cursor = "pointer";
    closeButton.style.fontSize = "1rem";

    // Adjust styles for smaller screens
    if (window.innerWidth <= 576) {
        alertBox.style.padding = "15px";
        alertMessage.style.fontSize = "0.9rem";
        closeButton.style.padding = "8px 16px";
        closeButton.style.fontSize = "0.9rem";
    }

    closeButton.addEventListener("click", () => {
        document.body.removeChild(alertOverlay);
    });

    alertBox.appendChild(alertMessage);
    alertBox.appendChild(closeButton);
    alertOverlay.appendChild(alertBox);

    document.body.appendChild(alertOverlay);
}

function showConfirm(message, onConfirm) {
    const confirmOverlay = document.createElement("div");
    const confirmBox = document.createElement("div");
    const confirmMessage = document.createElement("p");
    const confirmButtons = document.createElement("div");
    const confirmButton = document.createElement("button");
    const cancelButton = document.createElement("button");

    // Overlay styles
    confirmOverlay.style.position = "fixed";
    confirmOverlay.style.top = 0;
    confirmOverlay.style.left = 0;
    confirmOverlay.style.width = "100%";
    confirmOverlay.style.height = "100%";
    confirmOverlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    confirmOverlay.style.display = "flex";
    confirmOverlay.style.alignItems = "center";
    confirmOverlay.style.justifyContent = "center";
    confirmOverlay.style.zIndex = 1000;

    // Confirm box styles
    confirmBox.style.backgroundColor = "#fff";
    confirmBox.style.padding = "20px";
    confirmBox.style.borderRadius = "8px";
    confirmBox.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
    confirmBox.style.textAlign = "center";
    confirmBox.style.width = "400px"; // Default width for larger screens
    confirmBox.style.maxWidth = "90%"; // Ensure it fits smaller screens

    // Confirm message styles
    confirmMessage.textContent = message;
    confirmMessage.style.marginBottom = "20px";
    confirmMessage.style.fontSize = "1rem";

    // Confirm buttons container styles
    confirmButtons.style.display = "flex";
    confirmButtons.style.justifyContent = "space-between";
    confirmButtons.style.gap = "10px";

    // Confirm button styles
    confirmButton.textContent = "Yes";
    confirmButton.style.padding = "10px 20px";
    confirmButton.style.backgroundColor = "#007bff";
    confirmButton.style.color = "#fff";
    confirmButton.style.border = "none";
    confirmButton.style.borderRadius = "5px";
    confirmButton.style.cursor = "pointer";
    confirmButton.style.fontSize = "1rem";

    // Cancel button styles
    cancelButton.textContent = "No";
    cancelButton.style.padding = "10px 20px";
    cancelButton.style.backgroundColor = "#dc3545";
    cancelButton.style.color = "#fff";
    cancelButton.style.border = "none";
    cancelButton.style.borderRadius = "5px";
    cancelButton.style.cursor = "pointer";
    cancelButton.style.fontSize = "1rem";

    // Adjust styles for smaller screens
    if (window.innerWidth <= 576) {
        confirmBox.style.padding = "15px";
        confirmMessage.style.fontSize = "0.9rem";
        confirmButton.style.padding = "8px 16px";
        confirmButton.style.fontSize = "0.9rem";
        cancelButton.style.padding = "8px 16px";
        cancelButton.style.fontSize = "0.9rem";
    }

    // Event listeners for buttons
    confirmButton.addEventListener("click", () => {
        document.body.removeChild(confirmOverlay);
        if (onConfirm) onConfirm(); // Call the confirmation callback
    });

    cancelButton.addEventListener("click", () => {
        document.body.removeChild(confirmOverlay);
    });

    // Append elements
    confirmButtons.appendChild(confirmButton);
    confirmButtons.appendChild(cancelButton);
    confirmBox.appendChild(confirmMessage);
    confirmBox.appendChild(confirmButtons);
    confirmOverlay.appendChild(confirmBox);

    document.body.appendChild(confirmOverlay);
}
