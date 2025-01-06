// Main Hotel functionality namespace
const Hotel = {
    // Booking related functionality
    booking: {
        init: function() {
            const checkInDate = document.querySelector('input[name="check_in_date"]');
            const checkOutDate = document.querySelector('input[name="check_out_date"]');
            const nightsContainer = document.getElementById('nightsContainer');
            const numberOfNights = document.getElementById('numberOfNights');
            const totalPrice = document.getElementById('totalPrice');
            const basePriceElement = document.getElementById('basePrice');
            
            if (!basePriceElement) return;
            
            const basePrice = parseFloat(basePriceElement.dataset.price);

            function updatePriceBreakdown() {
                if (checkInDate?.value && checkOutDate?.value) {
                    const start = new Date(checkInDate.value);
                    const end = new Date(checkOutDate.value);
                    const nights = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
                    
                    if (nights > 0) {
                        nightsContainer.classList.remove('d-none');
                        nightsContainer.classList.add('d-flex');
                        numberOfNights.textContent = nights;
                        totalPrice.textContent = '$' + (nights * basePrice).toFixed(2);
                    } else {
                        nightsContainer.classList.add('d-none');
                        nightsContainer.classList.remove('d-flex');
                        totalPrice.textContent = '$' + basePrice.toFixed(2);
                    }
                }
            }

            if (checkInDate && checkOutDate) {
                const today = new Date().toISOString().split('T')[0];
                checkInDate.min = today;
                
                checkInDate.addEventListener('change', function() {
                    checkOutDate.min = this.value;
                    if (checkOutDate.value && checkOutDate.value < this.value) {
                        checkOutDate.value = this.value;
                    }
                    updatePriceBreakdown();
                });
                
                checkOutDate.addEventListener('change', updatePriceBreakdown);
            }
        }
    },

    // Room details modal functionality
    roomModal: {
        modal: null,
        init: function() {
            this.modal = new bootstrap.Modal(document.getElementById('roomInfoModal'));
            const moreInfoButtons = document.querySelectorAll('.more-info-button');
            
            moreInfoButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const roomId = button.getAttribute('data-room-id');
                    this.fetchRoomDetails(roomId);
                });
            });
        },

        fetchRoomDetails: function(roomId) {
            fetch(`/room/${roomId}/json/`)
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(data => {
                    this.displayRoomDetails(data);
                    this.modal.show();
                })
                .catch(error => {
                    console.error('Error fetching room details:', error);
                    alert('Failed to fetch room details. Please try again later.');
                });
        },

        displayRoomDetails: function(data) {
            document.getElementById('room-name').innerText = data.name;
            document.getElementById('room-description').innerText = data.description;
            document.getElementById('room-price').innerText = `$${data.price}`;
            document.getElementById('room-capacity').innerText = `${data.capacity} guests`;
        }
    }
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    
    // Initialize room modal functionality
    if (document.getElementById('roomInfoModal')) {
        Hotel.roomModal.init();
    }
    
    // Initialize booking functionality
    if (document.querySelector('input[name="check_in_date"]')) {
        Hotel.booking.init();
    }
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});