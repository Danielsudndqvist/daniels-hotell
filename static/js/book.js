document.addEventListener('DOMContentLoaded', function() {
    // Get all form elements
    const bookingForm = document.getElementById('bookingForm');
    const nextButtons = document.querySelectorAll('.next-step');
    const prevButtons = document.querySelectorAll('.prev-step');
    const progressBar = document.querySelector('.progress-bar');
    const bookingSteps = document.querySelectorAll('.booking-step');
    
    // Initialize current step
    let currentStep = 1;
    const totalSteps = bookingSteps.length;
    
    // Get form input fields
    const checkInDate = document.getElementById('id_check_in_date');
    const checkOutDate = document.getElementById('id_check_out_date');
    const guestName = document.getElementById('id_guest_name');
    const email = document.getElementById('id_email');
    const phone = document.getElementById('id_phone');
    const termsCheck = document.getElementById('termsCheck');
    const specialRequests = document.getElementById('id_special_requests');
    
    // Get summary elements
    const summaryDates = document.getElementById('summary-dates');
    const summaryGuest = document.getElementById('summary-guest');
    const summaryNights = document.getElementById('summary-nights');
    const summaryTotal = document.getElementById('summary-total');
    
    // Add the badge number to the first step (was missing in the template)
    const firstStepBadge = document.querySelector('.booking-step[data-step="1"] .badge');
    if (firstStepBadge) {
        firstStepBadge.textContent = '1';
    }
    
    // Get the room price from the page
    const priceText = document.querySelector('.lead').textContent;
    const roomPrice = parseFloat(priceText.match(/\d+(\.\d+)?/)[0]);
    
    /**
     * Validates the first step (date selection)
     * @returns {boolean} - Whether the step is valid
     */
    function validateStep1() {
        let isValid = true;
        
        // Check if check-in date is selected
        if (!checkInDate.value) {
            checkInDate.classList.add('is-invalid');
            document.getElementById('check_in_date_feedback').textContent = 'Please select a check-in date';
            isValid = false;
        } else {
            checkInDate.classList.remove('is-invalid');
            checkInDate.classList.add('is-valid');
        }
        
        // Check if check-out date is selected
        if (!checkOutDate.value) {
            checkOutDate.classList.add('is-invalid');
            document.getElementById('check_out_date_feedback').textContent = 'Please select a check-out date';
            isValid = false;
        } else {
            checkOutDate.classList.remove('is-invalid');
            checkOutDate.classList.add('is-valid');
        }
        
        // Check if check-out date is after check-in date
        if (checkInDate.value && checkOutDate.value) {
            const checkIn = new Date(checkInDate.value);
            const checkOut = new Date(checkOutDate.value);
            
            if (checkOut <= checkIn) {
                checkOutDate.classList.add('is-invalid');
                document.getElementById('check_out_date_feedback').textContent = 'Check-out date must be after check-in date';
                isValid = false;
            }
        }
        
        return isValid;
    }
    
    /**
     * Validates a phone number format
     * @param {string} phoneNumber - The phone number to validate
     * @returns {boolean} - Whether the phone number is valid
     */
    function validatePhoneNumber(phoneNumber) {
        // Remove all non-digit characters
        const digits = phoneNumber.replace(/\D/g, '');
        
        // Check if the phone has at least 10 digits (can be customized based on your needs)
        if (digits.length < 10) {
            return false;
        }
        
        // International format validation (optional)
        // This is a basic validation that allows for most international formats
        const phoneRegex = /^(\+|00)?[1-9]\d{1,14}$/;
        return phoneRegex.test(digits) || digits.length >= 10;
    }
    
    /**
     * Validates the second step (guest information)
     * @returns {boolean} - Whether the step is valid
     */
    function validateStep2() {
        let isValid = true;
        
        // Validate guest name
        if (!guestName.value.trim()) {
            guestName.classList.add('is-invalid');
            document.getElementById('guest_name_feedback').textContent = 'Please enter your full name';
            isValid = false;
        } else {
            guestName.classList.remove('is-invalid');
            guestName.classList.add('is-valid');
        }
        
        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.value.trim()) {
            email.classList.add('is-invalid');
            document.getElementById('email_feedback').textContent = 'Please enter your email address';
            isValid = false;
        } else if (!emailRegex.test(email.value.trim())) {
            email.classList.add('is-invalid');
            document.getElementById('email_feedback').textContent = 'Please enter a valid email address';
            isValid = false;
        } else {
            email.classList.remove('is-invalid');
            email.classList.add('is-valid');
        }
        
        // Validate phone
        if (!phone.value.trim()) {
            phone.classList.add('is-invalid');
            document.getElementById('phone_feedback').textContent = 'Please enter your phone number';
            isValid = false;
        } else if (!validatePhoneNumber(phone.value.trim())) {
            phone.classList.add('is-invalid');
            document.getElementById('phone_feedback').textContent = 'Please enter a valid phone number (at least 10 digits)';
            isValid = false;
        } else {
            phone.classList.remove('is-invalid');
            phone.classList.add('is-valid');
        }
        
        return isValid;
    }
    
    /**
     * Format a phone number as user types
     * @param {Event} e - Input event
     */
    function formatPhoneNumber(e) {
        // Get input value
        let input = e.target.value.replace(/\D/g, '');
        
        // Auto-format as user types
        let formattedInput = '';
        
        if (input.length > 0) {
            // Format based on length
            if (input.length <= 3) {
                formattedInput = input;
            } else if (input.length <= 6) {
                formattedInput = `(${input.substring(0, 3)}) ${input.substring(3)}`;
            } else {
                formattedInput = `(${input.substring(0, 3)}) ${input.substring(3, 6)}-${input.substring(6, 10)}`;
            }
            
            // Set the value
            e.target.value = formattedInput;
        }
    }
    
    /**
     * Updates the booking summary in step 3
     */
    function updateSummary() {
        // Format dates for summary
        if (checkInDate.value && checkOutDate.value) {
            const checkIn = new Date(checkInDate.value);
            const checkOut = new Date(checkOutDate.value);
            
            const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
            const formattedCheckIn = checkIn.toLocaleDateString('en-US', options);
            const formattedCheckOut = checkOut.toLocaleDateString('en-US', options);
            
            summaryDates.textContent = `${formattedCheckIn} to ${formattedCheckOut}`;
            
            // Calculate number of nights
            const timeDiff = checkOut.getTime() - checkIn.getTime();
            const nights = Math.ceil(timeDiff / (1000 * 3600 * 24));
            summaryNights.textContent = nights.toString();
            
            // Calculate total price
            const total = (nights * roomPrice).toFixed(2);
            summaryTotal.textContent = `$${total}`;
        }
        
        // Update guest info
        if (guestName.value) {
            summaryGuest.textContent = guestName.value;
        }
    }
    
    /**
     * Navigates to a specific step in the booking form
     * @param {number} stepNumber - The step number to navigate to
     */
    function goToStep(stepNumber) {
        // Hide all steps
        bookingSteps.forEach(step => {
            step.classList.add('d-none');
        });
        
        // Show the target step
        const targetStep = document.querySelector(`.booking-step[data-step="${stepNumber}"]`);
        if (targetStep) {
            targetStep.classList.remove('d-none');
        }
        
        // Update progress bar
        const progress = ((stepNumber - 1) / (totalSteps - 1)) * 100;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        
        // Set current step
        currentStep = stepNumber;
        
        // Scroll to top of form
        document.getElementById('bookingCard').scrollIntoView({ behavior: 'smooth' });
    }
    
    // Event listeners for next buttons
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const nextStep = parseInt(this.getAttribute('data-next'));
            
            if (currentStep === 1) {
                if (validateStep1()) {
                    goToStep(nextStep);
                }
            } else if (currentStep === 2) {
                if (validateStep2()) {
                    updateSummary();
                    goToStep(nextStep);
                }
            }
        });
    });
    
    // Event listeners for previous buttons
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const prevStep = parseInt(this.getAttribute('data-prev'));
            goToStep(prevStep);
        });
    });
    
    // Event listeners for date inputs
    checkInDate.addEventListener('change', function() {
        // Set minimum check-out date to the day after check-in
        if (this.value) {
            const checkIn = new Date(this.value);
            checkIn.setDate(checkIn.getDate() + 1);
            
            const yyyy = checkIn.getFullYear();
            const mm = String(checkIn.getMonth() + 1).padStart(2, '0');
            const dd = String(checkIn.getDate()).padStart(2, '0');
            
            checkOutDate.min = `${yyyy}-${mm}-${dd}`;
            
            // If check-out date is before new min date, update it
            if (checkOutDate.value && new Date(checkOutDate.value) < checkIn) {
                checkOutDate.value = `${yyyy}-${mm}-${dd}`;
            }
        }
    });
    
    // Add phone number formatting
    if (phone) {
        phone.addEventListener('input', formatPhoneNumber);
    }
    
    // Form submission validation
    bookingForm.addEventListener('submit', function(event) {
        // Prevent form submission
        event.preventDefault();
        
        // Validate terms and conditions
        if (!termsCheck.checked) {
            termsCheck.classList.add('is-invalid');
            return;
        } else {
            termsCheck.classList.remove('is-invalid');
        }
        
        // Final validation of all steps
        if (!validateStep1() || !validateStep2()) {
            // If validation fails, go back to the appropriate step
            if (!validateStep1()) {
                goToStep(1);
            } else if (!validateStep2()) {
                goToStep(2);
            }
            return;
        }
        
        // Show loading state on submit button
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
        submitBtn.disabled = true;
        
        // If all validations pass, submit the form
        setTimeout(() => {
            this.submit();
        }, 500); // Small delay to show loading state
    });
    
    /**
     * Initializes min dates for the date inputs
     */
    function initializeDateInputs() {
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        const formatDate = (date) => {
            const yyyy = date.getFullYear();
            const mm = String(date.getMonth() + 1).padStart(2, '0');
            const dd = String(date.getDate()).padStart(2, '0');
            return `${yyyy}-${mm}-${dd}`;
        };
        
        checkInDate.min = formatDate(today);
        checkOutDate.min = formatDate(tomorrow);
    }
    
    // Handle click on terms and conditions link in form
    document.querySelector('label[for="termsCheck"] a').addEventListener('click', function(e) {
        e.preventDefault();
        const termsModal = new bootstrap.Modal(document.getElementById('termsModal'));
        termsModal.show();
    });
    
    // Handle "I Understand" button in terms modal
    document.querySelector('#termsModal .btn-primary').addEventListener('click', function() {
        termsCheck.checked = true;
        termsCheck.classList.remove('is-invalid');
    });
    
    // Initialize the form
    initializeDateInputs();
    
    // Add form-control class to all form inputs if missing
    if (checkInDate && !checkInDate.classList.contains('form-control')) {
        checkInDate.classList.add('form-control');
    }
    
    if (checkOutDate && !checkOutDate.classList.contains('form-control')) {
        checkOutDate.classList.add('form-control');
    }
    
    if (guestName && !guestName.classList.contains('form-control')) {
        guestName.classList.add('form-control');
    }
    
    if (email && !email.classList.contains('form-control')) {
        email.classList.add('form-control');
    }
    
    if (phone && !phone.classList.contains('form-control')) {
        phone.classList.add('form-control');
    }
    
    if (specialRequests && !specialRequests.classList.contains('form-control')) {
        specialRequests.classList.add('form-control');
    }
});
