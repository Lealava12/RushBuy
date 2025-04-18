document.addEventListener("DOMContentLoaded", async function () {
    // Function to load external HTML components
    const loadComponent = async (url, elementId) => {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to load ${url}`);
            document.getElementById(elementId).innerHTML = await response.text();
        } catch (error) {
            console.error(`Error loading ${url}:`, error);
        }
    };

    // Include sidebar, header, footer, and nav
    // await loadComponent("slidebar.html", "sidebar-container");
    // await loadComponent("header.html", "header-container");
    await loadComponent("footer.html", "footer-container");
    // await loadComponent("nav.html", "nav-container");
    
});
