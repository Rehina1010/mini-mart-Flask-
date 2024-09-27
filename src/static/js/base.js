 document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            const flashMessages = document.querySelectorAll('.flash-messages .alert');
            flashMessages.forEach(function(message) {
                message.style.display = 'none';
            });
        }, 5000);
    });

    document.addEventListener('DOMContentLoaded', function() {
    const carouselElement = document.getElementById('productCarousel');
    const carousel = new bootstrap.Carousel(carouselElement, {
        interval: 5000,
        ride: 'carousel'
    });
});
    document.addEventListener('DOMContentLoaded', function() {
        const thumbnails = document.querySelectorAll('.thumb');

        thumbnails.forEach(function(thumb) {
            thumb.addEventListener('click', function() {
                const index = this.getAttribute('data-bs-slide-to');
                const carousel = new bootstrap.Carousel(document.querySelector('#productCarousel'));
                carousel.to(index);
            });
        });
    });