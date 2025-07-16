// Global variables
let isLoading = false;
// const API_BASE_URL = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '';
const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8000'
  : 'https://spam-detector-y2sw.onrender.com';


// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize Application
function initializeApp() {
    setupNavigation();
    setupAnimations();
    setupStatsCounter();
    setupDemoForm();
    setupContactForm();
    setupScrollEffects();
    
    // Page-specific initializations
    const currentPage = getCurrentPage();
    switch(currentPage) {
        case 'demo':
            initializeDemoPage();
            break;
        case 'project':
            initializeProjectPage();
            break;
        case 'about':
            initializeAboutPage();
            break;
        default:
            initializeHomePage();
    }
}

// Get current page name
function getCurrentPage() {
    const path = window.location.pathname;
    const page = path.split('/').pop().replace('.html', '');
    return page || 'index';
}

// Navigation Setup
function setupNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// Animation Setup
function setupAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            }
        });
    }, observerOptions);
    
    // Observe all elements with animation classes
    document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .scale-in').forEach(el => {
        observer.observe(el);
    });
}

// Stats Counter Animation
function setupStatsCounter() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const animateCounter = (element, target, duration = 2000) => {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format the number based on the target
            let displayValue = Math.floor(current);
            if (target < 1) {
                displayValue = (current).toFixed(2);
            } else if (target >= 1000) {
                displayValue = Math.floor(current).toLocaleString();
            }
            
            element.textContent = displayValue + (target < 1 ? '%' : target >= 1000 ? '+' : '%');
        }, 16);
    };
    
    // Observe stats section
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                statNumbers.forEach(stat => {
                    const target = parseFloat(stat.dataset.target);
                    animateCounter(stat, target);
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
}

// Demo Form Setup
function setupDemoForm() {
    const demoForm = document.getElementById('demo-form');
    if (!demoForm) return;
    
    // Form submission
    demoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (isLoading) return;
        
        const formData = new FormData(demoForm);
        const messageData = {
            message: formData.get('body'),
            options: { include_details: true }
        };
        
        await analyzeMessage(messageData);
    });
    
    // Clear button
    const clearBtn = document.querySelector('.clear-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            demoForm.reset();
            const resultContainer = document.querySelector('.result-container');
            if (resultContainer) {
                resultContainer.innerHTML = '';
            }
        });
    }
    
    // Example buttons
    const spamExample = document.querySelector('.spam-example');
    const hamExample = document.querySelector('.ham-example');
    
    if (spamExample) {
        spamExample.addEventListener('click', () => {
            document.getElementById('subject').value = "URGENT: Claim your $1000 reward NOW!";
            document.getElementById('body').value = "Congratulations! You've won $1000! Click here immediately to claim your reward before it expires: http://suspicious-site.com/claim. This is a limited time offer! HURRY UP!!!";
            document.getElementById('sender').value = "noreply@suspicious-site.com";
        });
    }
    
    if (hamExample) {
        hamExample.addEventListener('click', () => {
            document.getElementById('subject').value = "Weekly Team Meeting";
            document.getElementById('body').value = "Hi team, just a reminder about our weekly meeting tomorrow at 2 PM. Please review the agenda I sent earlier and come prepared with your status updates. Best regards, John";
            document.getElementById('sender').value = "manager@company.com";
        });
    }
}

// Contact Form Setup
function setupContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (isLoading) return;
        
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        
        try {
            isLoading = true;
            submitBtn.innerHTML = '<span class="loading-spinner"></span> Sending...';
            submitBtn.disabled = true;
            
            const formData = new FormData(contactForm);
            const contactData = {
                name: formData.get('name'),
                email: formData.get('email'),
                subject: formData.get('subject'),
                message: formData.get('message')
            };
            
            // First, check if the message is spam
            const messageCheckResult = await fetch(`${API_BASE_URL}/api/classify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: contactData.message,
                    options: { include_details: false }
                })
            });
            
            if (!messageCheckResult.ok) {
                throw new Error('Failed to verify message');
            }
            
            const spamCheck = await messageCheckResult.json();
            
            // Create a notification element
            const notificationContainer = document.createElement('div');
            notificationContainer.className = 'notification-container';
            
            if (spamCheck.classification === 'spam') {
                // Message is spam
                notificationContainer.innerHTML = `
                    <div class="notification error">
                        <i class="fas fa-exclamation-circle"></i>
                        <p>Your message appears to be spam. Please revise and try again.</p>
                    </div>
                `;
            } else {
                // Message is not spam, simulate sending
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Reset the form
                contactForm.reset();
                
                notificationContainer.innerHTML = `
                    <div class="notification success">
                        <i class="fas fa-check-circle"></i>
                        <p>Thank you! Your message has been sent successfully.</p>
                    </div>
                `;
            }
            
            // Add notification to the page
            contactForm.parentNode.appendChild(notificationContainer);
            
            // Remove notification after 5 seconds
            setTimeout(() => {
                notificationContainer.remove();
            }, 5000);
            
        } catch (error) {
            console.error('Contact form error:', error);
            
            // Show error notification
            const notificationContainer = document.createElement('div');
            notificationContainer.className = 'notification-container';
            notificationContainer.innerHTML = `
                <div class="notification error">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>An error occurred. Please try again later.</p>
                </div>
            `;
            contactForm.parentNode.appendChild(notificationContainer);
            
            // Remove notification after 5 seconds
            setTimeout(() => {
                notificationContainer.remove();
            }, 5000);
        } finally {
            isLoading = false;
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }
    });
}

// Analyze Message Function
async function analyzeMessage(messageData) {
    const submitBtn = document.querySelector('.demo-form .btn-primary');
    const resultContainer = document.querySelector('.result-container');
    
    try {
        isLoading = true;
        
        // Update button state
        submitBtn.innerHTML = '<span class="loading-spinner"></span> Analyzing...';
        submitBtn.disabled = true;
        
        // Show loading indicator in result container
        resultContainer.innerHTML = `
            <div class="result-card loading">
                <div class="loading-animation">
                    <div class="spinner"></div>
                </div>
                <p>Analyzing message...</p>
            </div>
        `;
        
        // Make API call
        const response = await fetch(`${API_BASE_URL}/api/classify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(messageData)
        });
        
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        
        const result = await response.json();
        displayResult(result);
        
    } catch (error) {
        console.error('Error analyzing message:', error);
        displayError('Failed to analyze message. Please try again or check if the backend server is running.');
    } finally {
        isLoading = false;
        submitBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Message';
        submitBtn.disabled = false;
    }
}

// Display Analysis Result
function displayResult(result) {
    const resultContainer = document.querySelector('.result-container');
    
    if (!resultContainer) {
        return;
    }
    
    const classification = result.classification;
    const confidence = result.confidence;
    const isSpam = classification === 'spam';
    const isUncertain = classification === 'uncertain';
    
    let resultClass = isSpam ? 'spam' : (isUncertain ? 'uncertain' : 'safe');
    let resultIcon = isSpam ? 'exclamation-triangle' : (isUncertain ? 'question-circle' : 'check-circle');
    let resultTitle = isSpam ? 'SPAM Detected' : (isUncertain ? 'Uncertain' : 'Safe Message');
    let resultDescription = isSpam 
        ? 'This message has been classified as spam with high confidence.' 
        : (isUncertain 
            ? 'This message contains some suspicious elements but is not clearly spam.' 
            : 'This message appears to be legitimate and safe.');
    
    let details = '';
    if (result.details && result.details.triggered_rules) {
        details = `
            <div class="details-section">
                <h4>Triggered Rules:</h4>
                <ul class="rules-list">
                    ${result.details.triggered_rules.map(rule => `<li>${rule}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    const resultHTML = `
        <div class="result-card ${resultClass}">
            <div class="result-header">
                <i class="fas fa-${resultIcon}"></i>
                <h3>${resultTitle}</h3>
            </div>
            <p class="result-description">${resultDescription}</p>
            <div class="confidence-meter">
                <div class="confidence-label">Confidence: ${Math.round(confidence * 100)}%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill ${resultClass}" style="width: ${confidence * 100}%"></div>
                </div>
            </div>
            <div class="processing-time">
                <small>Processing time: ${result.processing_time}ms</small>
            </div>
            ${details}
        </div>
    `;
    
    resultContainer.innerHTML = resultHTML;
    
    // Animate the result
    setTimeout(() => {
        const resultCard = document.querySelector('.result-card');
        if (resultCard) {
            resultCard.classList.add('show');
        }
    }, 100);
}

// Display Error Message
function displayError(message) {
    const resultContainer = document.querySelector('.result-container');
    
    if (!resultContainer) {
        return;
    }
    
    const errorHTML = `
        <div class="result-card error">
            <div class="result-header">
                <i class="fas fa-exclamation-circle"></i>
                <h3>Error</h3>
            </div>
            <p>${message}</p>
            <div class="error-actions">
                <button class="btn btn-outline retry-btn">
                    <i class="fas fa-redo"></i> Retry
                </button>
            </div>
        </div>
    `;
    
    resultContainer.innerHTML = errorHTML;
    
    // Add retry button functionality
    const retryBtn = document.querySelector('.retry-btn');
    if (retryBtn) {
        retryBtn.addEventListener('click', () => {
            const demoForm = document.getElementById('demo-form');
            if (demoForm) {
                demoForm.dispatchEvent(new Event('submit'));
            }
        });
    }
    
    // Animate the error
    setTimeout(() => {
        const resultCard = document.querySelector('.result-card');
        if (resultCard) {
            resultCard.classList.add('show');
        }
    }, 100);
}

// Scroll Effects
function setupScrollEffects() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Page-specific initializations
function initializeHomePage() {
    // Home page specific animations
    const heroElements = document.querySelectorAll('.hero-content > *');
    heroElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.2}s`;
    });
}

function initializeDemoPage() {
    // Add animation delays to steps
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        step.style.animationDelay = `${index * 0.2}s`;
    });
}

function initializeProjectPage() {
    // Project page specific functionality
    const techStack = document.querySelector('.tech-stack');
    if (techStack) {
        const technologies = [
            { name: 'Python', icon: 'fab fa-python', color: '#3776ab' },
            { name: 'FastAPI', icon: 'fas fa-rocket', color: '#009688' },
            { name: 'Scikit-learn', icon: 'fas fa-brain', color: '#f7931e' },
            { name: 'NLTK', icon: 'fas fa-language', color: '#2e7d32' },
            { name: 'Pandas', icon: 'fas fa-table', color: '#150458' },
            { name: 'NumPy', icon: 'fas fa-calculator', color: '#013243' }
        ];
        
        technologies.forEach((tech, index) => {
            const techCard = document.createElement('div');
            techCard.className = 'tech-card fade-in';
            techCard.style.animationDelay = `${index * 0.1}s`;
            techCard.innerHTML = `
                <div class="tech-icon" style="color: ${tech.color}">
                    <i class="${tech.icon}"></i>
                </div>
                <span class="tech-name">${tech.name}</span>
            `;
            techStack.appendChild(techCard);
        });
    }
}

function initializeAboutPage() {
    // About page animations
    const teamCards = document.querySelectorAll('.team-card');
    teamCards.forEach((card, index) => {
        card.classList.add('fade-in');
        card.style.animationDelay = `${index * 0.2}s`;
    });
}

// Utility Functions
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

// Performance optimized scroll handler
const optimizedScroll = throttle(() => {
    const scrollTop = window.pageYOffset;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    
    // Update scroll progress
    const progress = (scrollTop / (documentHeight - windowHeight)) * 100;
    document.documentElement.style.setProperty('--scroll-progress', `${progress}%`);
}, 16);

window.addEventListener('scroll', optimizedScroll);
