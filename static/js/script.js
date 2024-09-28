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

    // Initialize slides if present
    showSlides(slideIndex);

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
        fetch(`/room/${roomId}/details/`)
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
            roomCarouselInner.innerHTML = data.images.map((imgUrl, index) => `
                <div class="carousel-item ${index === 0 ? 'active' : ''}">
                    <img src="${imgUrl}" class="d-block w-100" alt="${data.name} - Image ${index + 1}">
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
            <p><strong>Price:</strong> $${data.price.toFixed(2)}/night</p>
            <p><strong>Max Occupancy:</strong> ${data.max_occupancy} people</p>
            <p><strong>Size:</strong> ${data.size} sq ft</p>
            <p><strong>Amenities:</strong> ${data.amenities.join(', ') || 'Not specified'}</p>
        `;

        // Update the "Book Now" button
        const bookNowBtn = document.getElementById('bookNowBtn');
        if (bookNowBtn) {
            bookNowBtn.href = `/book/${data.id}/`;
        }

        // Update modal title
        const modalTitle = document.getElementById('roomInfoModalLabel');
        if (modalTitle) {
            modalTitle.textContent = data.name;
        }
    }

    // Form validation
    var forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })

    // Add Bootstrap classes to form fields
    var formFields = document.querySelectorAll('form input, form select, form textarea');
    formFields.forEach(function(field) {
        field.classList.add('form-control');
    });

    // Add date validation
    var checkInDate = document.getElementById('id_check_in_date');
    var checkOutDate = document.getElementById('id_check_out_date');

    if (checkInDate && checkOutDate) {
        checkInDate.addEventListener('change', validateDates);
        checkOutDate.addEventListener('change', validateDates);
    }

    function validateDates() {
        if (checkInDate.value && checkOutDate.value) {
            if (new Date(checkOutDate.value) <= new Date(checkInDate.value)) {
                checkOutDate.setCustomValidity('Check-out date must be after check-in date');
            } else {
                checkOutDate.setCustomValidity('');
            }
        }
    }
});