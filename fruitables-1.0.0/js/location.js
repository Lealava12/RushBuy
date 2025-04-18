// Function to request location permission
function requestLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const latitude = position.coords.ltitude;
                const longitude = position.coords.longitude;

                // Save location in localStorage
                localStorage.setItem('userLocation', JSON.stringify({ latitude, longitude }));

                // Update location display
                updateLocationDisplay(latitude, longitude);
            },
            (error) => {
                console.error("Error getting location:", error.message);

                // Handle specific error cases
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        alert("Location access denied. Please enable location services in your browser settings.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Location information is unavailable. Please try again later.");
                        break;
                    case error.TIMEOUT:
                        alert("The request to get your location timed out. Please try again.");
                        break;
                    default:
                        alert("An unknown error occurred while accessing your location.");
                        break;
                }

                // Fallback: Load saved location if available
                loadSavedLocation();
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
    } else {
        alert("No saved location found. Please enable location services to get your current location.");
    }
}

// Trigger location request on index.html page load
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('index.html')) {
        requestLocation();
    }
    loadSavedLocation();
});
