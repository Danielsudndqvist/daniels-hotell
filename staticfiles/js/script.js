document.addEventListener('DOMContentLoaded', function() {
    // Carousel functionality
    let slideIndex = 1;
    const heroCarousel = document.getElementById('heroCarousel');
    if (heroCarousel) {
        new bootstrap.Carousel(heroCarousel, {
            interval: 5000,
            wrap: true 
        });
    }

    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    function currentSlide(n) {
        showSlides(slideIndex = n);
    }

    function showSlides(n) {
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("dot");

        if (n > slides.length) { slideIndex = 1 }
        if (n < 1) { slideIndex = slides.length }

        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }

        for (let i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }

        if (slides[slideIndex - 1]) {
            slides[slideIndex - 1].style.display = "block";
            dots[slideIndex - 1].className += " active";
        }
    }

    // Room details modal functionality
    const moreInfoButtons = document.querySelectorAll('.more-info-btn');
    const roomInfoModal = new bootstrap.Modal(document.getElementById('roomInfoModal'));
    const roomInfoContent = document.getElementById('roomInfoContent');
    const roomCarouselInner = document.getElementById('roomCarouselInner');

    moreInfoButtons.forEach(button => {
        button.addEventListener('click', function() {
            const roomId = this.getAttribute('data-room-id');
            fetchRoomDetails(roomId);
        });
    });

    function fetchRoomDetails(roomId) {
        fetch(`/room/${roomId}/json/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                displayRoomDetails(data);
                roomInfoModal.show();
            })
            .catch(error => {
                console.error('Error fetching room details:', error);
                alert('Failed to fetch room details. Please try again later.');
            });
    }

    function displayRoomDetails(data) {
        // Populate carousel with images
        if (data.images && data.images.length > 0) {
            roomCarouselInner.innerHTML = data.images.map((img, index) => `
                <div class="carousel-item ${index === 0 ? 'active' : ''}">
                    <img src="${img}" class="d-block w-100" alt="${data.name} - Image ${index + 1}">
                </div>
            `).join('');
            // Reinitialize the carousel
            new bootstrap.Carousel(document.getElementById('roomCarousel'));
        } else {
            roomCarouselInner.innerHTML = '<div class="carousel-item active"><img src="/static/images/placeholder.jpg" class="d-block w-100" alt="No image available"></div>';
        }

        // Populate room details
        roomInfoContent.innerHTML = `
            <h2>${data.name}</h2>
            <p>${data.description}</p>
            <p><strong>Type:</strong> ${data.room_type}</p>
            <p><strong>Price:</strong> $${data.price}/night</p>
            <p><strong>Amenities:</strong> ${data.amenities ? data.amenities.join(', ') : 'Not specified'}</p>
            <p><strong>Max Occupancy:</strong> ${data.max_occupancy} people</p>
            <p><strong>Size:</strong> ${data.size} sq ft</p>
        `;

        // Update the "Book Now" button
        const bookNowBtn = document.getElementById('bookNowBtn');
        if (bookNowBtn) {
            bookNowBtn.href = `/book/${data.id}/`;
        }
    }

    // Form validation
    const form = document.querySelector('form');
    if (form) {
        const fields = form.querySelectorAll('input, select, textarea');
        
        fields.forEach(function(field) {
            field.classList.add('form-control');
        });

        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    }

    // Initialize slides if present
    showSlides(slideIndex);
});