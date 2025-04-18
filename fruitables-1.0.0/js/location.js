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

                // Handle specific error cases
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        console.log("Location access denied by the user.");
                        showManualLocationInput();
                        break;
                    case error.POSITION_UNAVAILABLE:
                        console.log("Location information is unavailable.");
                        showManualLocationInput();
                        break;
                    case error.TIMEOUT:
                        console.log("The request to get the user's location timed out.");
                        showManualLocationInput();
                        break;
                    default:
                        console.log("An unknown error occurred while accessing the location.");
                        showManualLocationInput();
                        break;
                }
            }
        );
    } else {
        console.log("Geolocation is not supported by this browser.");
        showManualLocationInput();
    }
}

// Function to update location display
function updateLocationDisplay(latitude, longitude) {
    const userLocationElements = document.querySelectorAll('.user-location');
    userLocationElements.forEach(element => {
        element.textContent = `Lat: ${latitude}, Lon: ${longitude}`;
    });

    // Optionally, update the delivery location input field
    const deliveryLocationInput = document.getElementById('delivery-location-input');
    if (deliveryLocationInput) {
        deliveryLocationInput.value = `Lat: ${latitude}, Lon: ${longitude}`;
    }
}

// Function to show manual location input
function showManualLocationInput() {
    const manualLocationContainer = document.getElementById('manual-location-container');
    if (manualLocationContainer) {
        manualLocationContainer.style.display = 'block'; // Show the manual input container
    }
}

// Function to handle manual location input
function handleManualLocationInput() {
    const manualLocationInput = document.getElementById('manual-location-input');
    if (manualLocationInput) {
        const location = manualLocationInput.value.trim();
        if (location) {
            // Save the manually entered location in localStorage
            localStorage.setItem('userLocation', JSON.stringify({ manualLocation: location }));

            // Update the location display
            const userLocationElements = document.querySelectorAll('.user-location');
            userLocationElements.forEach(element => {
                element.textContent = location;
            });
        }
    }
}

// Trigger location request when "Detect my location" button is clicked
document.getElementById('detect-location-button').addEventListener('click', () => {
    requestLocation();
});

// Trigger manual location input handling when the user submits the input
document.getElementById('manual-location-submit').addEventListener('click', () => {
    handleManualLocationInput();
});
