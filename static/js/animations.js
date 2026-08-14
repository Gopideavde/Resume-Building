document.addEventListener("DOMContentLoaded", function() {
    // Only run if user hasn't preferred reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    if (!prefersReducedMotion.matches) {
        const revealElements = document.querySelectorAll('.reveal-up');
        
        if (revealElements.length > 0) {
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.15 // trigger when 15% visible
            };
            
            const observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('active');
                        // Stop observing once animated
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            
            revealElements.forEach(el => {
                observer.observe(el);
            });
        }
    }
});
