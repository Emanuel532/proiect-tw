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

    const searchInput = document.querySelector('.search-input');
    const searchWrapper = document.querySelector('.search-wrapper');
    const searchIcon = document.querySelector('.search-icon');

    searchInput.addEventListener('focus', () => {
        searchWrapper.style.border = '2px solid #007bff';
        searchInput.placeholder = ''
        searchIcon.style.color = '#007bff';
    });

    searchInput.addEventListener('blur', () => {
        searchWrapper.style.border = '';
        searchIcon.style.color = '';
        searchInput.placeholder = 'Search'
    });
});
