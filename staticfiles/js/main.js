document.addEventListener('DOMContentLoaded', function() {
    // Initialize all Bootstrap tooltips
    initTooltips();
    
    // Initialize date input constraints
    setupDateConstraints();
    
    // Initialize price range slider
    setupPriceRangeSlider();

    // Handle booking date calculations
    setupBookingCalculations();
    
    // Setup booking form validation
    setupFormValidation();
    
    // Initialize countdown timers
    updateBookingCountdowns();
    
    // Setup modal data loading
    setupModalDataLoading();
    
    // Setup tab persistence
    setupTabPersistence();
    
    // Setup filter collapsible state persistence
    setupFilterPersistence();
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Setup date input constraints (today as minimum for check-in, etc.)
 */
function setupDateConstraints() {
    const checkInDate = document.getElementById('check_in');
    const checkOutDate = document.getElementById('check_out');
    
    if (checkInDate && checkOutDate) {
        // Set today as minimum date for check-in
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        // Format dates as YYYY-MM-DD
        checkInDate.min = formatDate(today);
        checkOutDate.min = formatDate(tomorrow);
        
        // When check-in date changes, update the minimum check-out date
        checkInDate.addEventListener('change', function() {
            if (this.value) {
                const nextDay = new Date(this.value);
                nextDay.setDate(nextDay.getDate() + 1);
                
                checkOutDate.min = formatDate(nextDay);
                
                // If current check-out date is now invalid, update it
                if (checkOutDate.value && new Date(checkOutDate.value) <= new Date(this.value)) {
                    checkOutDate.value = formatDate(nextDay);
                }
                
                // If we have price calculation elements, update them
                updatePriceCalculation();
            }
        });
        
        // When check-out date changes, update price calculation if present
        checkOutDate.addEventListener('change', updatePriceCalculation);
    }
}

/**
 * Format a date object as YYYY-MM-DD
 */
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * Setup price range slider and display
 */
function setupPriceRangeSlider() {
    const priceRange = document.getElementById('price_range');
    const priceDisplay = document.getElementById('price_display');
    
    if (priceRange && priceDisplay) {
        // Update price display when slider moves
        priceRange.addEventListener('input', function() {
            priceDisplay.textContent = this.value;
        });
        
        // Set initial value
        priceDisplay.textContent = priceRange.value;
    }
}

/**
 * Setup booking date and price calculations
 */
function setupBookingCalculations() {
    // Add event listeners to update price calculation when either date changes
    const checkInDate = document.querySelector('input[name="check_in_date"]');
    const checkOutDate = document.querySelector('input[name="check_out_date"]');
    
    if (checkInDate && checkOutDate) {
        checkInDate.addEventListener('change', updatePriceCalculation);
        checkOutDate.addEventListener('change', updatePriceCalculation);
        
        // Initial calculation
        updatePriceCalculation();
    }
}

/**
 * Update price calculation based on selected dates
 */
function updatePriceCalculation() {
    const checkInDate = document.querySelector('input[name="check_in_date"]');
    const checkOutDate = document.querySelector('input[name="check_out_date"]');
    const basePrice = document.getElementById('basePrice');
    const numberOfNights = document.getElementById('numberOfNights');
    const totalPrice = document.getElementById('totalPrice');
    const nightsContainer = document.getElementById('nightsContainer');
    
    if (checkInDate && checkOutDate && basePrice && numberOfNights && totalPrice) {
        if (checkInDate.value && checkOutDate.value) {
            const start = new Date(checkInDate.value);
            const end = new Date(checkOutDate.value);
            
            // Calculate number of nights
            const timeDiff = end.getTime() - start.getTime();
            const nights = Math.round(timeDiff / (1000 * 60 * 60 * 24));
            
            if (nights > 0) {
                // Get price per night from data attribute
                const pricePerNight = parseFloat(basePrice.dataset.price);
                const total = pricePerNight * nights;
                
                // Update display
                numberOfNights.textContent = nights;
                totalPrice.textContent = `$${total.toFixed(2)}`;
                nightsContainer.classList.remove('d-none');
                nightsContainer.classList.add('d-flex');
                
                // Update any summary elements on the page
                updateBookingSummary(start, end, nights, total);
            }
        }
    }
}

/**
 * Update booking summary in multi-step forms
 */
function updateBookingSummary(checkIn, checkOut, nights, total) {
    const summaryDates = document.getElementById('summary-dates');
    const summaryNights = document.getElementById('summary-nights');
    const summaryTotal = document.getElementById('summary-total');
    
    if (summaryDates) {
        const checkInFormatted = checkIn.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        const checkOutFormatted = checkOut.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        summaryDates.textContent = `${checkInFormatted} to ${checkOutFormatted}`;
    }
    
    if (summaryNights) {
        summaryNights.textContent = nights;
    }
    
    if (summaryTotal) {
        summaryTotal.textContent = `$${total.toFixed(2)}`;
    }
}

/**
 * Setup form validation for booking forms
 */
function setupFormValidation() {
    const form = document.querySelector('form.needs-validation');
    
    if (form) {
        // NextStep and PrevStep buttons for multi-step forms
        setupMultiStepForm();
        
        // Validate on submit
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Find first invalid field and focus it
                const invalidField = form.querySelector(':invalid');
                if (invalidField) {
                    invalidField.focus();
                    
                    // If it's in a hidden step, show that step
                    const step = invalidField.closest('.booking-step');
                    if (step && step.classList.contains('d-none')) {
                        showBookingStep(parseInt(step.dataset.step));
                    }
                }
            }
            
            form.classList.add('was-validated');
        });
    }
}

/**
 * Setup multi-step form navigation
 */
function setupMultiStepForm() {
    const nextButtons = document.querySelectorAll('.next-step');
    const prevButtons = document.querySelectorAll('.prev-step');
    const progressBar = document.querySelector('.progress-bar');
    
    // Next buttons
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentStep = parseInt(this.closest('.booking-step').dataset.step);
            const nextStep = parseInt(this.dataset.next);
            
            // Validate current step fields
            if (validateStep(currentStep)) {
                showBookingStep(nextStep);
            }
        });
    });
    
    // Previous buttons
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const prevStep = parseInt(this.dataset.prev);
            showBookingStep(prevStep);
        });
    });
    
    // Helper function to show a specific step
    function showBookingStep(stepNumber) {
        // Hide all steps
        document.querySelectorAll('.booking-step').forEach(step => {
            step.classList.add('d-none');
        });
        
        // Show the target step
        const targetStep = document.querySelector(`.booking-step[data-step="${stepNumber}"]`);
        if (targetStep) {
            targetStep.classList.remove('d-none');
            
            // Update progress bar if present
            if (progressBar) {
                progressBar.style.width = `${(stepNumber - 1) * 50}%`;
            }
            
            // If it's the last step (review), update the summary
            if (stepNumber === 3) {
                updateGuestSummary();
            }
        }
    }
    
    // Validate fields in the current step
    function validateStep(step) {
        let isValid = true;
        const form = document.getElementById('bookingForm');
        
        // Get all required fields in the current step
        const currentStepEl = document.querySelector(`.booking-step[data-step="${step}"]`);
        const requiredFields = currentStepEl.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value) {
                field.classList.add('is-invalid');
                
                // Find the feedback element
                const feedbackEl = document.getElementById(`${field.id}_feedback`);
                if (feedbackEl) {
                    feedbackEl.textContent = 'This field is required';
                }
                
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }
    
    // Update guest information in the summary
    function updateGuestSummary() {
        const guestName = document.querySelector('input[name="guest_name"]');
        const summaryGuest = document.getElementById('summary-guest');
        
        if (guestName && summaryGuest) {
            summaryGuest.textContent = guestName.value;
        }
    }
}

/**
 * Update countdown timers for upcoming bookings
 */
function updateBookingCountdowns() {
    const countdownBadges = document.querySelectorAll('.countdown-badge');
    
    if (countdownBadges.length > 0) {
        function updateCountdowns() {
            const now = new Date();
            
            countdownBadges.forEach(badge => {
                const targetDate = new Date(badge.dataset.date);
                
                // Calculate difference in days
                const timeDiff = targetDate.getTime() - now.getTime();
                const diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
                
                updateCountdownDisplay(badge, diffDays);
            });
        }
        
        // Initial update
        updateCountdowns();
        
        // Update every hour
        setInterval(updateCountdowns, 3600000);
    }
}

/**
 * Update the display of a countdown badge
 */
function updateCountdownDisplay(badge, days) {
    // Remove all existing color classes
    badge.classList.remove('bg-primary', 'bg-warning', 'bg-success', 'bg-danger', 'text-dark');
    
    if (days > 1) {
        badge.textContent = `${days} days`;
        badge.classList.add('bg-primary');
    } else if (days === 1) {
        badge.textContent = 'Tomorrow';
        badge.classList.add('bg-warning', 'text-dark');
    } else if (days === 0) {
        badge.textContent = 'Today';
        badge.classList.add('bg-success');
    } else {
        badge.textContent = 'Past due';
        badge.classList.add('bg-danger');
    }
}

/**
 * Setup modal data loading
 */
function setupModalDataLoading() {
    // Handle dynamically loaded modals
    document.querySelectorAll('[data-bs-remote]').forEach(item => {
        item.addEventListener('click', function (event) {
            event.preventDefault();
            
            const modal = document.getElementById(this.dataset.bsTarget.replace('#', ''));
            const url = this.dataset.bsRemote;
            
            if (modal && url) {
                const modalBody = modal.querySelector('.modal-body');
                const spinner = modal.querySelector('.spinner-border')?.parentElement;
                
                if (modalBody) {
                    // Show loading spinner if present
                    if (spinner) {
                        spinner.classList.remove('d-none');
                    }
                    
                    // Hide existing content
                    modalBody.innerHTML = '';
                    
                    // Fetch content
                    fetch(url)
                        .then(response => response.text())
                        .then(html => {
                            modalBody.innerHTML = html;
                            
                            // Hide spinner
                            if (spinner) {
                                spinner.classList.add('d-none');
                            }
                        })
                        .catch(error => {
                            console.error('Error loading modal content:', error);
                            modalBody.innerHTML = `
                                <div class="alert alert-danger">
                                    Error loading content. Please try again.
                                </div>
                            `;
                            
                            // Hide spinner
                            if (spinner) {
                                spinner.classList.add('d-none');
                            }
                        });
                }
                
                // Show the modal
                const modalInstance = new bootstrap.Modal(modal);
                modalInstance.show();
            }
        });
    });
}

/**
 * Setup tab persistence using localStorage
 */
function setupTabPersistence() {
    const tabElements = document.querySelectorAll('a[data-bs-toggle="tab"], a[data-bs-toggle="list"]');
    
    if (tabElements.length > 0) {
        // Get the active tab from localStorage
        const activeTab = localStorage.getItem('activeTab');
        
        if (activeTab) {
            // Find the tab element
            const tab = document.querySelector(`a[href="${activeTab}"]`);
            if (tab) {
                // Activate the tab
                const tabInstance = new bootstrap.Tab(tab);
                tabInstance.show();
            }
        }
        
        // Save active tab when changed
        tabElements.forEach(tab => {
            tab.addEventListener('shown.bs.tab', function (event) {
                localStorage.setItem('activeTab', event.target.getAttribute('href'));
            });
        });
    }
}

/**
 * Setup filter collapsible state persistence
 */
function setupFilterPersistence() {
    const filterCollapse = document.getElementById('filterCollapse');
    
    if (filterCollapse) {
        // Get filter state from localStorage
        const isCollapsed = localStorage.getItem('filterCollapsed') === 'true';
        
        if (isCollapsed) {
            filterCollapse.classList.remove('show');
        } else {
            filterCollapse.classList.add('show');
        }
        
        // Save state when changed
        filterCollapse.addEventListener('hidden.bs.collapse', function () {
            localStorage.setItem('filterCollapsed', 'true');
        });
        
        filterCollapse.addEventListener('shown.bs.collapse', function () {
            localStorage.setItem('filterCollapsed', 'false');
        });
    }
}
