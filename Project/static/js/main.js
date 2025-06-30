// Main JavaScript File for Ad Predictor Website

// Global variables
let currentTheme = 'light';
let isAnimating = false;

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
    initializeApp();
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

// Initialize Application
function initializeApp() {
    initializeAnimations();
    initializeFormValidation();
    initializeTooltips();
    initializeCharts();
    initializeNotifications();
    initializeThemeToggle();
    initializeSmoothScrolling();
    initializeLazyLoading();
    initializeSearchFunctionality();
    initializeMobileMenu();
}

// ===== ANIMATIONS =====
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.animate-on-scroll, .fade-in-up, .fade-in-left, .fade-in-right').forEach(el => {
        observer.observe(el);
    });

    // Parallax effect for background elements
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// ===== FORM VALIDATION =====
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                showFormErrors(form);
            }
            form.classList.add('was-validated');
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => validateField(input));
            input.addEventListener('input', () => clearFieldError(input));
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';

    // Custom validation rules
    switch(fieldName) {
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
            break;
        case 'password':
            if (value.length < 8) {
                isValid = false;
                errorMessage = 'Password must be at least 8 characters long';
            }
            break;
        case 'username':
            if (value.length < 3) {
                isValid = false;
                errorMessage = 'Username must be at least 3 characters long';
            }
            break;
    }

    if (!isValid) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }

    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function showFormErrors(form) {
    const invalidFields = form.querySelectorAll('.is-invalid');
    if (invalidFields.length > 0) {
        showNotification('Please correct the errors in the form', 'error');
        invalidFields[0].focus();
    }
}

// ===== TOOLTIPS =====
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            placement: 'top',
            trigger: 'hover'
        });
    });
}

// ===== CHARTS =====
function initializeCharts() {
    // Initialize Chart.js if available
    if (typeof Chart !== 'undefined') {
        setupCharts();
    }
}

function setupCharts() {
    const chartElements = document.querySelectorAll('.chart-container');
    
    chartElements.forEach(container => {
        const canvas = container.querySelector('canvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            const chartType = container.dataset.chartType || 'line';
            const chartData = JSON.parse(container.dataset.chartData || '{}');
            
            new Chart(ctx, {
                type: chartType,
                data: chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: container.dataset.chartTitle || 'Chart'
                        }
                    }
                }
            });
        }
    });
}

// ===== NOTIFICATIONS =====
function initializeNotifications() {
    // Create notification container
    const notificationContainer = document.createElement('div');
    notificationContainer.id = 'notification-container';
    notificationContainer.className = 'notification-container';
    document.body.appendChild(notificationContainer);
}

function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icon = getNotificationIcon(type);
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="${icon}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, duration);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return 'fas fa-check-circle';
        case 'error': return 'fas fa-exclamation-circle';
        case 'warning': return 'fas fa-exclamation-triangle';
        case 'info': 
        default: return 'fas fa-info-circle';
    }
}

// ===== THEME TOGGLE =====
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    }
}

function toggleTheme() {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

function setTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Update theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

// ===== SMOOTH SCROLLING =====
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===== LAZY LOADING =====
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// ===== SEARCH FUNCTIONALITY =====
function initializeSearchFunctionality() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
}

function handleSearch(event) {
    const query = event.target.value.toLowerCase();
    const searchableElements = document.querySelectorAll('[data-searchable]');
    
    searchableElements.forEach(element => {
        const text = element.textContent.toLowerCase();
        const isVisible = text.includes(query);
        element.style.display = isVisible ? '' : 'none';
    });
}

// ===== MOBILE MENU =====
function initializeMobileMenu() {
    const mobileMenuToggle = document.querySelector('.navbar-toggler');
    const mobileMenu = document.querySelector('.navbar-collapse');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('show');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                mobileMenu.classList.remove('show');
            }
        });
    }
}

// ===== UTILITY FUNCTIONS =====

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Format numbers
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Format currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Format date
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    return new Intl.DateTimeFormat('en-US', { ...defaultOptions, ...options }).format(date);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy to clipboard', 'error');
    });
}

// Download file
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ===== API HELPERS =====

// Make API request
async function makeApiRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        console.error('API request failed:', error);
        return { success: false, error: error.message };
    }
}

// ===== FORM HELPERS =====

// Submit form via AJAX
async function submitFormAjax(form, successCallback = null, errorCallback = null) {
    const formData = new FormData(form);
    const url = form.action;
    const method = form.method || 'POST';
    
    try {
        const response = await fetch(url, {
            method: method,
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            if (successCallback) successCallback(result);
            showNotification('Form submitted successfully!', 'success');
        } else {
            if (errorCallback) errorCallback(result);
            showNotification(result.message || 'Form submission failed', 'error');
        }
    } catch (error) {
        console.error('Form submission error:', error);
        if (errorCallback) errorCallback(error);
        showNotification('An error occurred while submitting the form', 'error');
    }
}

// ===== CHART HELPERS =====

// Create chart data
function createChartData(labels, datasets) {
    return {
        labels: labels,
        datasets: datasets.map(dataset => ({
            label: dataset.label,
            data: dataset.data,
            backgroundColor: dataset.backgroundColor || 'rgba(37, 99, 235, 0.2)',
            borderColor: dataset.borderColor || 'rgba(37, 99, 235, 1)',
            borderWidth: dataset.borderWidth || 2,
            fill: dataset.fill !== undefined ? dataset.fill : false
        }))
    };
}

// ===== ANIMATION HELPERS =====

// Animate element
function animateElement(element, animation, duration = 1000) {
    element.style.animation = `${animation} ${duration}ms ease-in-out`;
    
    setTimeout(() => {
        element.style.animation = '';
    }, duration);
}

// Fade in element
function fadeIn(element, duration = 500) {
    element.style.opacity = '0';
    element.style.display = 'block';
    
    let start = null;
    function animate(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const opacity = Math.min(progress / duration, 1);
        
        element.style.opacity = opacity;
        
        if (progress < duration) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

// Fade out element
function fadeOut(element, duration = 500) {
    let start = null;
    function animate(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const opacity = Math.max(1 - progress / duration, 0);
        
        element.style.opacity = opacity;
        
        if (progress < duration) {
            requestAnimationFrame(animate);
        } else {
            element.style.display = 'none';
        }
    }
    
    requestAnimationFrame(animate);
}

// ===== EXPORT FUNCTIONS =====
window.AdPredictor = {
    showNotification,
    copyToClipboard,
    downloadFile,
    makeApiRequest,
    submitFormAjax,
    createChartData,
    animateElement,
    fadeIn,
    fadeOut,
    formatNumber,
    formatCurrency,
    formatDate
};