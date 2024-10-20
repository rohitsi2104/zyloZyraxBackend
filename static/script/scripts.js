document.addEventListener("DOMContentLoaded", function() {
    // Get cookie banner and buttons
    const cookieBanner = document.querySelector('.cookie-banner');
    const acceptButton = document.getElementById('accept-button');
    const declineButton = document.getElementById('decline-button');

    // Accept button event listener
    acceptButton.addEventListener('click', function() {
        cookieBanner.style.display = 'none'; // Hide cookie banner
        // Logic for accepting cookies
        console.log("Cookies accepted");
    });

    // Decline button event listener
    declineButton.addEventListener('click', function() {
        cookieBanner.style.display = 'none'; // Hide cookie banner
        // Logic for declining cookies
        console.log("Cookies declined");
    });
});
