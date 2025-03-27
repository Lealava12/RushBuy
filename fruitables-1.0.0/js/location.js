// Function to request location permission
function requestLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Save location in localStorage
                localStorage.setItem('userLocation', JSON.stringify({ latitude, longitude }));

                // Update location display
                updateLocationDisplay(latitude, longitude);
            },
            (error) => {
                console.error("Error getting location:", error.message);
                alert("Location access denied. Please enable location services.");
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Function to update location display
function updateLocationDisplay(latitude, longitude) {
    const userLocationElements = document.querySelectorAll('.user-location');
    userLocationElements.forEach(element => {
        element.textContent = `Lat: ${latitude}, Lon: ${longitude}`;
    });
}

// Function to load location from localStorage if available
function loadSavedLocation() {
    const savedLocation = localStorage.getItem('userLocation');
    if (savedLocation) {
        const { latitude, longitude } = JSON.parse(savedLocation);
        updateLocationDisplay(latitude, longitude);
    }
}

// Trigger location request on index.html page load
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('index.html')) {
        requestLocation();
    }
    loadSavedLocation();
});
