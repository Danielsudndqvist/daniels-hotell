document.addEventListener('DOMContentLoaded', function() {
    // Initialize all accessibility enhancements
    initAccessibilityFeatures();
    
    // Mobile-specific enhancements
    initMobileEnhancements();
    
    // Improved form validation with meaningful errors
    initAccessibleFormValidation();
    
    // Add skip to content functionality
    addSkipToContentLink();
    
    // Detect if mobile bottom navigation should be shown
    detectMobileNavigation();
    
    // Handle responsive tables
    makeTablesResponsive();
    
    // Add ARIA attributes to interactive elements
    enhanceAriaSupport();
    
    // Add mobile card headers toggle functionality
    setupMobileCardHeaders();
    
    // Detect and apply dark mode if supported and preferred
    setupDarkModeSupport();
});

/**
 * Initialize core accessibility features
 */
function initAccessibilityFeatures() {
    // Add 'lang' attribute to HTML if missing
    if (!document.documentElement.hasAttribute('lang')) {
        document.documentElement.setAttribute('lang', 'en');
    }
    
    // Ensure all images have alt text
    document.querySelectorAll('img:not([alt])').forEach(img => {
        console.warn('Image missing alt attribute:', img);
        img.setAttribute('alt', ''); // Empty alt for decorative images
    });
    
    // Fix heading hierarchy
    checkHeadingHierarchy();
    
    // Add roles to landmarks if missing
    document.querySelectorAll('header:not([role])').forEach(el => el.setAttribute('role', 'banner'));
    document.querySelectorAll('footer:not([role])').forEach(el => el.setAttribute('role', 'contentinfo'));
    document.querySelectorAll('nav:not([role])').forEach(el => el.setAttribute('role', 'navigation'));
    document.querySelectorAll('main:not([role])').forEach(el => el.setAttribute('role', 'main'));
    
    // Ensure interactive elements are keyboard accessible
    document.querySelectorAll('div[onclick], span[onclick]').forEach(el => {
        if (!el.hasAttribute('tabindex')) {
            el.setAttribute('tabindex', '0');
            console.warn('Added missing tabindex to interactive element:', el);
        }
        
        // Also ensure there's a keyboard event handler
        if (!el.hasAttribute('onkeydown')) {
            el.setAttribute('onkeydown', 'if(event.key==="Enter"||event.key===" "){this.click();event.preventDefault();}');
        }
    });
}

/**
 * Check and warn about improper heading hierarchy
 */
function checkHeadingHierarchy() {
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    let lastLevel = 0;
    
    headings.forEach(heading => {
        const currentLevel = parseInt(heading.tagName.substring(1));
        
        if (currentLevel - lastLevel > 1) {
            console.warn('Heading hierarchy skipped a level:', heading);
        }
        
        lastLevel = currentLevel;
    });
}

/**
 * Add skip to content link for keyboard users
 */
function addSkipToContentLink() {
    // Check if it already exists
    if (document.querySelector('.skip-to-content')) {
        return;
    }
    
    // Find the main content landmark
    const mainContent = document.querySelector('main, [role="main"], #main, #content');
    
    if (mainContent) {
        // Ensure it has an id for the skip link target
        if (!mainContent.id) {
            mainContent.id = 'main-content';
        }
        
        // Create and add the skip link
        const skipLink = document.createElement('a');
        skipLink.href = `#${mainContent.id}`;
        skipLink.className = 'skip-to-content';
        skipLink.textContent = 'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }
}

/**
 * Add mobile-specific enhancements
 */
function initMobileEnhancements() {
    // Check if it's a mobile device
    const isMobile = window.matchMedia('(max-width: 768px)').matches;
    
    if (isMobile) {
        // Add mobile class to body
        document.body.classList.add('is-mobile');
        
        // Handle fixed bottom booking bar if needed
        const bookingForms = document.querySelectorAll('.booking-form-container');
        if (bookingForms.length > 0) {
            createFixedBookingBar();
        }
        
        // Add touch-friendly classes
        document.querySelectorAll('.btn').forEach(btn => {
            if (!btn.classList.contains('btn-sm') && !btn.classList.contains('btn-lg')) {
                btn.classList.add('touch-friendly');
            }
        });
        
        // Convert multi-step forms to accordions on mobile
        document.querySelectorAll('.booking-steps').forEach(stepsContainer => {
            convertToMobileAccordion(stepsContainer);
        });
    }
}

/**
 * Create a fixed booking bar at the bottom for mobile
 */
function createFixedBookingBar() {
    // Only needed on detail or booking pages
    if (!document.querySelector('.room-card, .booking-form-container')) {
        return;
    }
    
    // Check price element
    const priceElement = document.querySelector('.price, .room-price, [data-price]');
    if (!priceElement) {
        return;
    }
    
    // Get price value
    let priceText = '$0';
    if (priceElement.dataset.price) {
        priceText = `$${priceElement.dataset.price}`;
    } else if (priceElement.textContent.includes('$')) {
        priceText = priceElement.textContent.trim();
    }
    
    // Create the fixed bar
    const fixedBar = document.createElement('div');
    fixedBar.className = 'fixed-booking-bar';
    fixedBar.innerHTML = `
        <div class="price">${priceText} <small class="text-muted">/night</small></div>
        <button class="btn btn-primary" id="mobileBookBtn">Book Now</button>
    `;
    
    // Add to body
    document.body.appendChild(fixedBar);
    document.body.classList.add('has-fixed-booking-bar');
    
    // Handle button click - scroll to form or trigger booking
    document.getElementById('mobileBookBtn').addEventListener('click', function() {
        const bookingForm = document.querySelector('.booking-form-container form');
        if (bookingForm) {
            bookingForm.scrollIntoView({ behavior: 'smooth' });
        } else {
            // Find the first book now button and click it
            const bookBtn = document.querySelector('a[href*="book"], .btn:contains("Book")');
            if (bookBtn) {
                bookBtn.click();
            }
        }
    });
}

/**
 * Convert multi-step forms to accordions on mobile
 */
function convertToMobileAccordion(stepsContainer) {
    // Only on mobile
    if (!window.matchMedia('(max-width: 768px)').matches) {
        return;
    }
    
    const steps = stepsContainer.querySelectorAll('.booking-step');
    
    steps.forEach((step, index) => {
        // Get the step number and title
        const stepNum = step.dataset.step;
        const stepTitle = step.querySelector('h5') || step.querySelector('.step-title');
        
        if (stepTitle) {
            // Create accordion header
            const accordionHeader = document.createElement('div');
            accordionHeader.className = 'mobile-step-header';
            accordionHeader.setAttribute('aria-expanded', index === 0 ? 'true' : 'false');
            accordionHeader.innerHTML = stepTitle.innerHTML;
            
            // Replace title with accordion header
            stepTitle.parentNode.replaceChild(accordionHeader, stepTitle);
            
            // Create content wrapper
            const contentWrapper = document.createElement('div');
            contentWrapper.className = 'mobile-step-content';
            if (index !== 0) {
                contentWrapper.style.display = 'none';
            }
            
            // Move all remaining content to wrapper
            while (step.firstChild) {
                contentWrapper.appendChild(step.firstChild);
            }
            
            // Add header and content to step
            step.appendChild(accordionHeader);
            step.appendChild(contentWrapper);
            
            // Show all steps but hide content
            step.classList.remove('d-none');
            
            // Add click handler
            accordionHeader.addEventListener('click', function() {
                const isExpanded = this.getAttribute('aria-expanded') === 'true';
                
                // Close all steps
                steps.forEach(s => {
                    const header = s.querySelector('.mobile-step-header');
                    const content = s.querySelector('.mobile-step-content');
                    
                    if (header && content) {
                        header.setAttribute('aria-expanded', 'false');
                        content.style.display = 'none';
                    }
                });
                
                // Open this step if it was closed
                if (!isExpanded) {
                    this.setAttribute('aria-expanded', 'true');
                    contentWrapper.style.display = 'block';
                }
            });
        }
    });
}

/**
 * Enhance form validation with better accessibility
 */
function initAccessibleFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        // Add novalidate to handle validation with JS
        form.setAttribute('novalidate', '');
        
        // Custom validation on submit
        form.addEventListener('submit', function(event) {
            if (!this.checkValidity()) {
                event.preventDefault();
                
                // Find all invalid fields
                const invalidFields = Array.from(form.elements).filter(el => !el.checkValidity());
                
                // Display custom error messages
                invalidFields.forEach(field => {
                    markFieldAsInvalid(field);
                });
                
                // Focus the first invalid field
                if (invalidFields.length > 0) {
                    invalidFields[0].focus();
                    
                    // Announce error to screen readers
                    announceToScreenReader(`${invalidFields.length} form fields have errors. Starting with: ${getErrorMessage(invalidFields[0])}`);
                }
            }
        });
        
        // Live validation on blur
        Array.from(form.elements).forEach(field => {
            if (field.nodeName !== 'BUTTON' && field.nodeName !== 'FIELDSET') {
                field.addEventListener('blur', function() {
                    // Only validate if field has been interacted with
                    if (field.value !== '') {
                        if (!field.checkValidity()) {
                            markFieldAsInvalid(field);
                        } else {
                            markFieldAsValid(field);
                        }
                    }
                });
                
                // Clear validation styling on input
                field.addEventListener('input', function() {
                    field.classList.remove('is-invalid', 'is-valid');
                    
                    // Find and hide any associated error message
                    const errorId = field.id + '-error';
                    const errorElement = document.getElementById(errorId);
                    if (errorElement) {
                        errorElement.style.display = 'none';
                    }
                });
            }
        });
    });
}

/**
 * Mark a form field as invalid with appropriate ARIA attributes
 */
function markFieldAsInvalid(field) {
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
    
    // Get the error message
    const errorMessage = getErrorMessage(field);
    
    // Find or create error message element
    let errorElement = document.getElementById(field.id + '-error');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.id = field.id + '-error';
        errorElement.className = 'invalid-feedback';
        field.parentNode.appendChild(errorElement);
    }
    
    // Update error message
    errorElement.textContent = errorMessage;
    errorElement.style.display = 'block';
    
    // Set ARIA attributes
    field.setAttribute('aria-invalid', 'true');
    field.setAttribute('aria-describedby', errorElement.id);
}

/**
 * Mark a form field as valid
 */
function markFieldAsValid(field) {
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
    field.setAttribute('aria-invalid', 'false');
    
    // Find and hide any error message
    const errorId = field.id + '-error';
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

/**
 * Get appropriate error message for a field
 */
function getErrorMessage(field) {
    // Check for custom error message
    if (field.dataset.errorMessage) {
        return field.dataset.errorMessage;
    }
    
    // Use validation message or generate based on validation state
    if (field.validity.valueMissing) {
        return `${getFieldLabel(field)} is required.`;
    } else if (field.validity.typeMismatch) {
        return `Please enter a valid ${field.type} in ${getFieldLabel(field)}.`;
    } else if (field.validity.tooShort) {
        return `${getFieldLabel(field)} should be at least ${field.minLength} characters.`;
    } else if (field.validity.tooLong) {
        return `${getFieldLabel(field)} should be at most ${field.maxLength} characters.`;
    } else if (field.validity.rangeUnderflow) {
        return `${getFieldLabel(field)} should be at least ${field.min}.`;
    } else if (field.validity.rangeOverflow) {
        return `${getFieldLabel(field)} should be at most ${field.max}.`;
    } else if (field.validity.patternMismatch) {
        return `${getFieldLabel(field)} should match the required format.`;
    }
    
    return field.validationMessage || `${getFieldLabel(field)} is invalid.`;
}

/**
 * Get the visible label text for a form field
 */
function getFieldLabel(field) {
    // Check for associated label
    const labelElement = document.querySelector(`label[for="${field.id}"]`);
    if (labelElement) {
        // Remove any required indicator (*)
        return labelElement.textContent.replace('*', '').trim();
    }
    
    // Use placeholder, name, or ID as fallback
    return field.placeholder || field.name || field.id || 'This field';
}

/**
 * Announce a message to screen readers using an ARIA live region
 */
function announceToScreenReader(message) {
    // Find or create the live region
    let announcer = document.getElementById('a11y-announcer');
    if (!announcer) {
        announcer = document.createElement('div');
        announcer.id = 'a11y-announcer';
        announcer.className = 'sr-only';
        announcer.setAttribute('aria-live', 'assertive');
        announcer.setAttribute('aria-atomic', 'true');
        document.body.appendChild(announcer);
    }
    
    // Set the message and clear after a short delay
    announcer.textContent = message;
    setTimeout(() => {
        announcer.textContent = '';
    }, 3000);
}

/**
 * Detect and setup mobile navigation
 */
function detectMobileNavigation() {
    // Only if on mobile
    if (!window.matchMedia('(max-width: 768px)').matches) {
        return;
    }
    
    // Check for main navigation
    const mainNav = document.querySelector('nav.navbar, .main-nav');
    if (!mainNav) {
        return;
    }
    
    // Check for common page types
    const isHomePage = document.body.classList.contains('home') || window.location.pathname === '/' || window.location.pathname === '/index.html';
    const isRoomListingPage = document.body.classList.contains('room-listing') || window.location.pathname.includes('/rooms');
    const isBookingPage = document.body.classList.contains('booking') || window.location.pathname.includes('/book');
    const isAccountPage = document.body.classList.contains('account') || window.location.pathname.includes('/account');
    
    // Create bottom navigation if not on a specialized page
    if (!isBookingPage) {
        createMobileBottomNav(isHomePage, isRoomListingPage, isAccountPage);
    }
}

/**
 * Create a mobile bottom navigation bar
 */
function createMobileBottomNav(isHomePage, isRoomListingPage, isAccountPage) {
    // Check if it already exists
    if (document.querySelector('.mobile-nav')) {
        return;
    }
    
    // Create navigation
    const mobileNav = document.createElement('nav');
    mobileNav.className = 'mobile-nav';
    mobileNav.setAttribute('aria-label', 'Mobile navigation');
    
    // Create navigation items
    mobileNav.innerHTML = `
        <a href="/" class="mobile-nav-item ${isHomePage ? 'active' : ''}">
            <i class="fas fa-home mobile-nav-icon"></i>
            <span class="mobile-nav-text">Home</span>
        </a>
        <a href="/rooms/" class="mobile-nav-item ${isRoomListingPage ? 'active' : ''}">
            <i class="fas fa-bed mobile-nav-icon"></i>
            <span class="mobile-nav-text">Rooms</span>
        </a>
        <a href="#" class="mobile-nav-item" id="mobileSearchBtn">
            <i class="fas fa-search mobile-nav-icon"></i>
            <span class="mobile-nav-text">Search</span>
        </a>
        <a href="/bookings/" class="mobile-nav-item">
            <i class="fas fa-calendar-alt mobile-nav-icon"></i>
            <span class="mobile-nav-text">Bookings</span>
        </a>
        <a href="/account/" class="mobile-nav-item ${isAccountPage ? 'active' : ''}">
            <i class="fas fa-user mobile-nav-icon"></i>
            <span class="mobile-nav-text">Account</span>
        </a>
    `;
    
    // Add to body
    document.body.appendChild(mobileNav);
    document.body.classList.add('has-mobile-nav');
    
    // Add padding to body to prevent content from being hidden
    document.body.style.paddingBottom = '60px';
    
    // Handle search button click
    document.getElementById('mobileSearchBtn').addEventListener('click', function(e) {
        e.preventDefault();
        
        // Check for search form
        const searchForm = document.querySelector('.search-card, form[role="search"]');
        if (searchForm) {
            searchForm.scrollIntoView({ behavior: 'smooth' });
        } else {
            // Redirect to search page
            window.location.href = '/rooms/';
        }
    });
}

/**
 * Make tables responsive on mobile
 */
function makeTablesResponsive() {
    document.querySelectorAll('table:not(.table-responsive-card)').forEach(table => {
        // Only process tables not in .table-responsive
        if (!table.closest('.table-responsive')) {
            // Add responsive class
            table.classList.add('table-responsive-card');
            
            // Get header cells
            const headerCells = table.querySelectorAll('thead th');
            const headerTexts = Array.from(headerCells).map(th => th.textContent.trim());
            
            // Add data attributes to each cell
            table.querySelectorAll('tbody tr').forEach(row => {
                row.querySelectorAll('td').forEach((cell, index) => {
                    if (index < headerTexts.length) {
                        cell.setAttribute('data-label', headerTexts[index]);
                    }
                });
            });
        }
    });
}

/**
 * Add ARIA support to interactive elements
 */
function enhanceAriaSupport() {
    // Add aria-current="page" to active navigation items
    document.querySelectorAll('.nav-item.active, .nav-link.active').forEach(item => {
        item.setAttribute('aria-current', 'page');
    });
    
    // Ensure all buttons have accessible names
    document.querySelectorAll('button').forEach(button => {
        if (!button.textContent.trim() && !button.getAttribute('aria-label')) {
            // Try to use icon name or provide generic label
            const icon = button.querySelector('i[class*="fa-"]');
            if (icon) {
                const iconClass = Array.from(icon.classList).find(cls => cls.startsWith('fa-'));
                if (iconClass) {
                    const iconName = iconClass.replace('fa-', '').replace(/-/g, ' ');
                    button.setAttribute('aria-label', iconName + ' button');
                }
            } else {
                console.warn('Button missing accessible name:', button);
                button.setAttribute('aria-label', 'Button');
            }
        }
    });
    
    // Add appropriate roles to custom widgets
    document.querySelectorAll('.accordion, .collapse-group').forEach(accordion => {
        accordion.setAttribute('role', 'region');
        
        const headers = accordion.querySelectorAll('.accordion-header, [data-bs-toggle="collapse"]');
        headers.forEach(header => {
            header.setAttribute('role', 'button');
            
            // Ensure it has aria-expanded
            if (!header.hasAttribute('aria-expanded')) {
                const isExpanded = header.classList.contains('show') || 
                                  header.classList.contains('active') ||
                                  header.getAttribute('aria-selected') === 'true';
                header.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
            }
            
            // Ensure it has aria-controls
            if (!header.hasAttribute('aria-controls')) {
                const target = header.dataset.bsTarget || header.getAttribute('href');
                if (target && target.startsWith('#')) {
                    header.setAttribute('aria-controls', target.substring(1));
                }
            }
        });
    });
    
    // Add roles to form components
    document.querySelectorAll('form').forEach(form => {
        // Add role="search" to search forms
        if (form.querySelector('input[type="search"]') || 
            form.classList.contains('search-form') ||
            form.getAttribute('action')?.includes('search')) {
            form.setAttribute('role', 'search');
        }
        
        // Add aria-required to required fields
        form.querySelectorAll('[required]').forEach(field => {
            field.setAttribute('aria-required', 'true');
            
            // Find the label and add required class
            const labelElement = document.querySelector(`label[for="${field.id}"]`);
            if (labelElement) {
                labelElement.classList.add('required');
            }
        });
    });
}

/**
 * Setup mobile card headers to be collapsible
 */
function setupMobileCardHeaders() {
    // Only on mobile
    if (!window.matchMedia('(max-width: 768px)').matches) {
        return;
    }
    
    document.querySelectorAll('.card-header-collapsible').forEach(header => {
        const card = header.closest('.card');
        if (!card) return;
        
        const cardBody = card.querySelector('.card-body');
        if (!cardBody) return;
        
        // Set initial state
        const initiallyExpanded = !header.classList.contains('collapsed');
        header.setAttribute('aria-expanded', initiallyExpanded ? 'true' : 'false');
        
        if (!initiallyExpanded) {
            cardBody.style.display = 'none';
        }
        
        // Add click handler
        header.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            this.setAttribute('aria-expanded', !isExpanded ? 'true' : 'false');
            cardBody.style.display = !isExpanded ? 'block' : 'none';
            
            // Add/remove collapsed class
            if (isExpanded) {
                this.classList.add('collapsed');
            } else {
                this.classList.remove('collapsed');
            }
        });
    });
}

/**
 * Setup dark mode support if browser supports it
 */
function setupDarkModeSupport() {
    // Check if dark mode is preferred
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (prefersDarkMode) {
        document.documentElement.classList.add('dark-mode-supported');
    }
    
    // Add listener for changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (event.matches) {
            document.documentElement.classList.add('dark-mode-supported');
        } else {
            document.documentElement.classList.remove('dark-mode-supported');
        }
    });
}
