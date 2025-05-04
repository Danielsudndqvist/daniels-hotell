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
    const phone = document.getElementById('id_phone_number');
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
        
        // Check if dates are valid
        if (checkInDate.value && checkOutDate.value) {
            const checkIn = new Date(checkInDate.value);
            const checkOut = new Date(checkOutDate.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            // Check if check-in date is in the past
            if (checkIn < today) {
                checkInDate.classList.add('is-invalid');
                document.getElementById('check_in_date_feedback').textContent = 'Check-in date cannot be in the past';
                isValid = false;
            }
            
            // Check if check-out date is after check-in date
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
        // First check if the phone number contains any letters
        if (/[a-zA-Z]/.test(phoneNumber)) {
            return false;
        }
        
        // Check if the phone number contains only allowed characters
        if (!/^[0-9+\-\s()]+$/.test(phoneNumber)) {
            return false;
        }
        
        // Remove all non-digit characters
        const digits = phoneNumber.replace(/\D/g, '');
        
        // Check if the phone has at least 10 digits and no more than 15
        return digits.length >= 10 && digits.length <= 15;
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
            document.getElementById('phone_number_feedback').textContent = 'Please enter your phone number';
            isValid = false;
        } else if (!validatePhoneNumber(phone.value.trim())) {
            phone.classList.add('is-invalid');
            document.getElementById('phone_number_feedback').textContent = 'Please enter a valid phone number (10-15 digits, no letters)';
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
        // Get input value and remove any letters
        const input = e.target.value.replace(/[a-zA-Z]/g, '');
        
        // If the value changed after removing letters, update the input
        if (input !== e.target.value) {
            e.target.value = input;
            return;
        }
        
        // Get just the digits for validation
        const digits = input.replace(/\D/g, '');
        
        // Make sure we have at least the minimum required digits
        if (digits.length < 10) {
            // Just keep the input as-is, but add validation feedback
            if (digits.length > 0) {
                phone.classList.add('is-invalid');
                document.getElementById('phone_number_feedback').textContent = 'Phone number must have at least 10 digits';
            }
        } else {
            // Valid length, remove any error class
            phone.classList.remove('is-invalid');
            phone.classList.add('is-valid');
            
            // Format the phone number
            let formattedInput = '';
            
            // Format based on length
            if (digits.length <= 3) {
                formattedInput = digits;
            } else if (digits.length <= 6) {
                formattedInput = `(${digits.substring(0, 3)}) ${digits.substring(3)}`;
            } else {
                formattedInput = `(${digits.substring(0, 3)}) ${digits.substring(3, 6)}-${digits.substring(6, Math.min(digits.length, 15))}`;
            }
            
            // Set the formatted value only if it's different (to avoid cursor jumping)
            if (formattedInput !== e.target.value) {
                e.target.value = formattedInput;
            }
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
        button.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent any default button behavior
            
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
        button.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent any default button behavior
            
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
    
    // Add phone number formatting and validation
    if (phone) {
        phone.addEventListener('input', formatPhoneNumber);
        
        // Add HTML5 validation pattern attribute
        phone.setAttribute('pattern', '[0-9+\\-\\s()]+');
        phone.setAttribute('title', 'Phone number must contain 10-15 digits (no letters)');
        
        // Make sure phone has the correct name attribute
        phone.name = 'phone_number';
        
        // Add an invisible feedback element if it doesn't exist
        if (!document.getElementById('phone_number_feedback')) {
            const feedbackDiv = document.createElement('div');
            feedbackDiv.id = 'phone_number_feedback';
            feedbackDiv.className = 'invalid-feedback';
            feedbackDiv.textContent = 'Please enter a valid phone number';
            
            if (phone.parentNode) {
                phone.parentNode.appendChild(feedbackDiv);
            }
        }
    }
    
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
        
        // Set default values to today and tomorrow if no values are set
        if (!checkInDate.value) {
            checkInDate.value = formatDate(today);
        }
        
        if (!checkOutDate.value) {
            checkOutDate.value = formatDate(tomorrow);
        }
    }
    
    // Handle click on terms and conditions link in form
    const termsLink = document.querySelector('label[for="termsCheck"] a');
    if (termsLink) {
        termsLink.addEventListener('click', function(e) {
            e.preventDefault();
            const termsModal = new bootstrap.Modal(document.getElementById('termsModal'));
            termsModal.show();
        });
    }
    
    // Handle "I Understand" button in terms modal
    const termsModalButton = document.querySelector('#termsModal .btn-primary');
    if (termsModalButton) {
        termsModalButton.addEventListener('click', function() {
            termsCheck.checked = true;
            termsCheck.classList.remove('is-invalid');
        });
    }
    
    // Initialize the form
    initializeDateInputs();
    
    // Add form-control class to all form inputs if missing
    const formInputs = [checkInDate, checkOutDate, guestName, email, phone, specialRequests];
    formInputs.forEach(input => {
        if (input && !input.classList.contains('form-control')) {
            input.classList.add('form-control');
        }
    });
    
    // Initialize first step
    goToStep(1);
    
    // ENHANCED FORM SUBMISSION HANDLER
    if (bookingForm) {
        // Replace the default submit event handler
        bookingForm.addEventListener('submit', function(e) {
            // Prevent the default form submission
            e.preventDefault();
            
            console.log('Form submission started...');
            
            // Validate terms and conditions
            if (!termsCheck.checked) {
                termsCheck.classList.add('is-invalid');
                console.log('Terms not checked');
                return false;
            } else {
                termsCheck.classList.remove('is-invalid');
            }
            
            // Final validation check
            if (!validateStep1() || !validateStep2()) {
                console.log('Form validation failed');
                return false;
            }
            
            // Show loading indicator on the submit button
            const submitBtn = document.querySelector('#bookingForm button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
                submitBtn.disabled = true;
            }
            
            console.log('Form is valid, submitting directly...');
            
            // Make sure all hidden fields have correct values
            // This is crucial for multi-step forms
            
            // Submit the form directly - this bypasses any issues with the multi-step setup
            bookingForm.submit();
            return true;
        });
    }
});
