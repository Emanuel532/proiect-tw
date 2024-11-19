document.addEventListener("DOMContentLoaded", function () {
    const currentURL = window.location.pathname; // Get only the pathname (e.g., "/messages")

    // Select all relevant links (including navbar-brand and icons)
    const allLinks = document.querySelectorAll('.navbar-brand, .icons .icon');

    allLinks.forEach(link => {
        const linkHref = link.getAttribute('href'); // Get the href value

        // Check for exact matches
        if (currentURL === linkHref) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});
