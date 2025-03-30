// Initialize Vanta.js birds effect for background
document.addEventListener('DOMContentLoaded', () => {
    // Configure and start Vanta.js birds effect with enhanced 3D flying effect
    VANTA.BIRDS({
        el: "#vanta-background",
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.20,                // Increased scale for more pronounced 3D effect
        scaleMobile: 1.10,          // Increased scale on mobile too
        backgroundColor: 0x07192f,  // Deep blue background color
        color1: 0xff3f81,           // Pink color
        color2: 0x42e2f4,           // Light blue color
        colorMode: "variance",
        birdSize: 1.00,             // Slightly smaller birds
        wingSpan: 30.00,            // Increased wing span for better wing visibility
        separation: 25.00,          // Decreased separation for more clustered flying patterns
        alignment: 35.00,           // Decreased alignment to create more varied flight paths
        cohesion: 30.00,            // Increased cohesion for better flocking behavior
        quantity: 6.00,             // More birds for richer visual effect
        speedLimit: 6.00,           // Increased speed for more dynamic movement
        backgroundAlpha: 0.92,      // Slight transparency in background
        forceAnimate: true,         // Force animation even when not in view
        mouseEase: false,           // Birds will move away from cursor more abruptly
        scaleMouse: 3.50,           // Significantly increased mouse influence
        neighborRadius: 180.00,     // Increased neighbor radius for better group dynamics
        antialias: true,            // Added antialiasing for smoother rendering
        showDots: false             // No dots, just birds for cleaner look
    });

    // Handle responsive adjustments with improved 3D settings
    window.addEventListener('resize', () => {
        if (window.innerWidth < 768) {
            // Adjust bird quantity and 3D settings for smaller screens
            if (window.VANTA && window.VANTA.current) {
                window.VANTA.current.setOptions({
                    quantity: 4.00,
                    birdSize: 0.85,
                    speedLimit: 5.00,
                    scaleMouse: 2.50,
                    wingSpan: 25.00,
                    separation: 20.00,
                    scale: 1.10
                });
            }
        } else {
            // Reset to enhanced 3D settings for larger screens
            if (window.VANTA && window.VANTA.current) {
                window.VANTA.current.setOptions({
                    quantity: 6.00,
                    birdSize: 1.00,
                    speedLimit: 6.00,
                    scaleMouse: 3.50,
                    wingSpan: 30.00,
                    separation: 25.00,
                    scale: 1.20
                });
            }
        }
    });
});

// Error handling toast functionality
function showError(message) {
    const errorToast = document.getElementById('error-toast');
    const errorMessage = document.getElementById('error-message');
    
    // Set error message
    errorMessage.textContent = message || 'Something went wrong. Please try again.';
    
    // Initialize Bootstrap toast
    const toast = new bootstrap.Toast(errorToast);
    toast.show();
}
