document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const form = document.getElementById('bookingForm');
    const checkInDate = document.getElementById('{{ form.check_in_date.id_for_label }}');
    const checkOutDate = document.getElementById('{{ form.check_out_date.id_for_label }}');
    const guestName = document.getElementById('{{ form.guest_name.id_for_label }}');
    const email = document.getElementById('{{ form.email.id_for_label }}');
    const termsCheck = document.getElementById('termsCheck');

    // Summary elements
    const summaryDates = document.getElementById('summary-dates');
    const summaryGuest = document.getElementById('summary-guest');
    const summaryNights = document.getElementById('summary-nights');
    const summaryTotal = document.getElementById('summary-total');

    // Progress bar
    const progressBar = document.querySelector('.progress-bar');

    // Navigation between steps
    const steps = document.querySelectorAll('.booking-step');
    const nextButtons = document.querySelectorAll('.next-step');
    const prevButtons = document.querySelectorAll('.prev-step');

    // Price calculation
    const roomPrice = {{ room.price }};

    // Set today as minimum date for check-in
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    checkInDate.min = formatDate(today);
    checkOutDate.min = formatDate(tomorrow);

    checkInDate.addEventListener('change', function() {
        if (this.value) {
            const nextDay = new Date(this.value);
            nextDay.setDate(nextDay.getDate() + 1);
            checkOutDate.min = formatDate(nextDay);

            if (checkOutDate.value && new Date(checkOutDate.value) <= new Date(this.value)) {
                checkOutDate.value = formatDate(nextDay);
            }

            updatePriceSummary();
        }
    });

    checkOutDate.addEventListener('change', updatePriceSummary);

    function updatePriceSummary() {
        if (checkInDate.value && checkOutDate.value) {
            const start = new Date(checkInDate.value);
            const end = new Date(checkOutDate.value);
            const nights = Math.round((end - start) / (1000 * 60 * 60 * 24));

            summaryDates.textContent = `${checkInDate.value} to ${checkOutDate.value}`;
            summaryNights.textContent = nights;
            summaryTotal.textContent = `$${(roomPrice * nights).toFixed(2)}`;
        }
    }

    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentStep = parseInt(this.closest('.booking-step').dataset.step);
            const nextStep = parseInt(this.dataset.next);

            if (validateStep(currentStep)) {
                progressBar.style.width = `${(nextStep - 1) * 50}%`;
                document.querySelector(`.booking-step[data-step="${currentStep}"]`).classList.add('d-none');
                document.querySelector(`.booking-step[data-step="${nextStep}"]`).classList.remove('d-none');

                if (nextStep === 3) {
                    updatePriceSummary();
                    summaryGuest.textContent = guestName.value;
                }
            }
        });
    });

    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentStep = parseInt(this.closest('.booking-step').dataset.step);
            const prevStep = parseInt(this.dataset.prev);

            progressBar.style.width = `${(prevStep - 1) * 50}%`;
            document.querySelector(`.booking-step[data-step="${currentStep}"]`).classList.add('d-none');
            document.querySelector(`.booking-step[data-step="${prevStep}"]`).classList.remove('d-none');
        });
    });

    function validateStep(step) {
        let isValid = true;

        switch(step) {
            case 1:
                if (!checkInDate.value) {
                    document.getElementById('check_in_date_feedback').textContent = 'Please select a check-in date';
                    checkInDate.classList.add('is-invalid');
                    isValid = false;
                } else {
                    checkInDate.classList.remove('is-invalid');
                }

                if (!checkOutDate.value) {
                    document.getElementById('check_out_date_feedback').textContent = 'Please select a check-out date';
                    checkOutDate.classList.add('is-invalid');
                    isValid = false;
                } else {
                    checkOutDate.classList.remove('is-invalid');
                }
                break;

            case 2:
                if (!guestName.value) {
                    document.getElementById('guest_name_feedback').textContent = 'Please enter your name';
                    guestName.classList.add('is-invalid');
                    isValid = false;
                } else {
                    guestName.classList.remove('is-invalid');
                }

                if (!email.value) {
                    document.getElementById('email_feedback').textContent = 'Please enter your email';
                    email.classList.add('is-invalid');
                    isValid = false;
                } else if (!/\S+@\S+\.\S+/.test(email.value)) {
                    document.getElementById('email_feedback').textContent = 'Please enter a valid email';
                    email.classList.add('is-invalid');
                    isValid = false;
                } else {
                    email.classList.remove('is-invalid');
                }
                break;
        }

        return isValid;
    }

    form.addEventListener('submit', function(event) {
        if (!termsCheck.checked) {
            termsCheck.classList.add('is-invalid');
            event.preventDefault();
            return false;
        } else {
            termsCheck.classList.remove('is-invalid');
        }

        const requiredFields = form.querySelectorAll('[required]');
        let formValid = true;

        requiredFields.forEach(field => {
            if (!field.value) {
                field.classList.add('is-invalid');
                formValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });

        if (!formValid) {
            event.preventDefault();
            return false;
        }
    });
});
