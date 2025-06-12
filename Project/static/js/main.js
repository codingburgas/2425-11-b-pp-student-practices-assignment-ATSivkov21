// Main JavaScript File for Ad Predictor Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components when DOM is fully loaded
    initSmoothScrolling();
    initFormValidations();
    initTooltips();
    initAnimatedElements();
    initPasswordStrengthChecker();
    initDynamicBackground();
    initMobileMenu();
    initFloatingElements();
    initCounters();
    initAdPreviewHover();
    initThemeSwitcher();
});

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Update URL without page jump
                if (history.pushState) {
                    history.pushState(null, null, targetId);
                } else {
                    location.hash = targetId;
                }
            }
        });
    });
}

/**
 * Initialize form validation with custom styles
 */
function initFormValidations() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Add custom invalid styles
                const invalidFields = form.querySelectorAll(':invalid');
                invalidFields.forEach(field => {
                    field.classList.add('is-invalid');
                    
                    // Create or display custom error message
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('invalid-feedback')) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'invalid-feedback';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                    
                    if (field.validity.valueMissing) {
                        errorMessage.textContent = 'This field is required';
                    } else if (field.validity.typeMismatch) {
                        errorMessage.textContent = 'Please enter a valid value';
                    } else if (field.validity.patternMismatch) {
                        errorMessage.textContent = 'Value does not match required pattern';
                    } else if (field.validity.tooShort) {
                        errorMessage.textContent = `Value should be at least ${field.minLength} characters`;
                    } else if (field.validity.tooLong) {
                        errorMessage.textContent = `Value should be no more than ${field.maxLength} characters`;
                    }
                });
            }
            
            form.classList.add('was-validated');
        }, false);
        
        // Remove validation styles when user starts typing
        form.querySelectorAll('input, textarea, select').forEach(input => {
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    this.classList.remove('is-invalid');
                    const errorMessage = this.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('invalid-feedback')) {
                        errorMessage.textContent = '';
                    }
                }
            });
        });
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover focus',
            customClass: 'blue-tooltip'
        });
    });
}

/**
 * Initialize animated elements with Intersection Observer
 */
function initAnimatedElements() {
    const animatedElements = document.querySelectorAll('[data-aos], .animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                
                if (element.dataset.aos) {
                    element.classList.add('aos-animate');
                } else if (element.classList.contains('animate-on-scroll')) {
                    element.classList.add('animate__animated', 'animate__fadeInUp');
                }
                
                // Stop observing after animation triggers
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Initialize password strength checker
 */
function initPasswordStrengthChecker() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        const strengthMeter = document.createElement('div');
        strengthMeter.className = 'password-strength-meter mt-2';
        strengthMeter.innerHTML = `
            <div class="progress" style="height: 5px;">
                <div class="progress-bar" role="progressbar" style="width: 0%"></div>
            </div>
            <small class="text-muted password-strength-text">Password strength: Very weak</small>
        `;
        input.parentNode.insertBefore(strengthMeter, input.nextElementSibling);
        
        input.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            const progressBar = strengthMeter.querySelector('.progress-bar');
            const strengthText = strengthMeter.querySelector('.password-strength-text');
            
            progressBar.style.width = strength.percentage + '%';
            progressBar.className = 'progress-bar ' + strength.class;
            strengthText.textContent = 'Password strength: ' + strength.text;
            strengthText.className = 'text-muted password-strength-text ' + strength.textClass;
        });
    });
    
    function calculatePasswordStrength(password) {
        let strength = 0;
        
        // Length check
        if (password.length > 0) strength += 1;
        if (password.length >= 8) strength += 1;
        if (password.length >= 12) strength += 1;
        
        // Complexity checks
        if (/[A-Z]/.test(password)) strength += 1;
        if (/[0-9]/.test(password)) strength += 1;
        if (/[^A-Za-z0-9]/.test(password)) strength += 1;
        
        // Calculate percentage and return result
        const percentage = Math.min(100, Math.round((strength / 7) * 100));
        
        if (percentage < 30) {
            return {
                percentage: percentage,
                class: 'bg-danger',
                text: 'Very weak',
                textClass: 'text-danger'
            };
        } else if (percentage < 60) {
            return {
                percentage: percentage,
                class: 'bg-warning',
                text: 'Weak',
                textClass: 'text-warning'
            };
        } else if (percentage < 80) {
            return {
                percentage: percentage,
                class: 'bg-info',
                text: 'Moderate',
                textClass: 'text-info'
            };
        } else {
            return {
                percentage: percentage,
                class: 'bg-success',
                text: 'Strong',
                textClass: 'text-success'
            };
        }
    }
}

/**
 * Initialize dynamic background effects
 */
function initDynamicBackground() {
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple-effect';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 1000);
        });
    });
    
    // Add parallax effect to elements with data-parallax attribute
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    window.addEventListener('scroll', function() {
        const scrollPosition = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = parseFloat(element.dataset.parallax) || 0.5;
            const offset = scrollPosition * speed;
            element.style.transform = `translateY(${offset}px)`;
        });
    });
}

/**
 * Initialize mobile menu functionality
 */
function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
            
            // Animate the hamburger icon
            this.classList.toggle('active');
        });
        
        // Close menu when clicking on a nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                    navbarToggler.classList.remove('active');
                }
            });
        });
    }
}

/**
 * Initialize floating elements animation
 */
function initFloatingElements() {
    const floatingElements = document.querySelectorAll('.floating-element');
    
    floatingElements.forEach((element, index) => {
        // Set different animation delays for each element
        element.style.animationDelay = `${index * 0.2}s`;
        
        // Add hover effect
        element.addEventListener('mouseenter', function() {
            this.style.animationPlayState = 'paused';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.animationPlayState = 'running';
        });
    });
}

/**
 * Initialize counter animations
 */
function initCounters() {
    const counterElements = document.querySelectorAll('.counter');
    
    if (counterElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = +counter.dataset.target;
                    const duration = +counter.dataset.duration || 2000;
                    const increment = target / (duration / 16);
                    let current = 0;
                    
                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            counter.textContent = Math.floor(current);
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.textContent = target;
                        }
                    };
                    
                    updateCounter();
                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });
        
        counterElements.forEach(counter => {
            observer.observe(counter);
        });
    }
}

/**
 * Initialize ad preview hover effects
 */
function initAdPreviewHover() {
    const adPreviews = document.querySelectorAll('.ad-preview');
    
    adPreviews.forEach(ad => {
        ad.addEventListener('mouseenter', function() {
            const overlay = this.querySelector('.ad-overlay');
            if (overlay) {
                overlay.style.opacity = '1';
            }
        });
        
        ad.addEventListener('mouseleave', function() {
            const overlay = this.querySelector('.ad-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
            }
        });
    });
}

/**
 * Initialize theme switcher functionality
 */
function initThemeSwitcher() {
    const themeSwitcher = document.getElementById('themeSwitcher');
    
    if (themeSwitcher) {
        // Check for saved theme preference or use preferred color scheme
        const savedTheme = localStorage.getItem('theme') || 
                          (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        
        // Apply the saved theme
        document.documentElement.setAttribute('data-theme', savedTheme);
        themeSwitcher.checked = savedTheme === 'dark';
        
        // Listen for theme switcher changes
        themeSwitcher.addEventListener('change', function() {
            const newTheme = this.checked ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait = 100) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(this, args);
        }, wait);
    };
}

// Add global error handler
window.addEventListener('error', function(e) {
    console.error('Unhandled error:', e.error);
    // You could add error reporting here
});

// Add global unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // You could add error reporting here
});

// Export functions for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initSmoothScrolling,
        initFormValidations,
        initTooltips,
        initAnimatedElements,
        initPasswordStrengthChecker,
        initDynamicBackground,
        initMobileMenu,
        initFloatingElements,
        initCounters,
        initAdPreviewHover,
        initThemeSwitcher
    };
}