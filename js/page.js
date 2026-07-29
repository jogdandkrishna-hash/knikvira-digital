/* ============================================
   KNIKVIRA DIGITAL — Shared Page JS
   Navbar scroll effect, mobile menu, scroll animations
   ============================================ */

(function() {
  // Navbar scroll effect
  var navbar = document.getElementById('kdNav');
  if (navbar) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }, { passive: true });
  }

  // Mobile menu toggle
  var mobileBtn = document.getElementById('kdMobileBtn');
  var mobileMenu = document.getElementById('kdMobileMenu');
  if (mobileBtn && mobileMenu) {
    mobileBtn.addEventListener('click', function() {
      mobileMenu.classList.toggle('open');
      mobileBtn.textContent = mobileMenu.classList.contains('open') ? '✕' : '☰';
    });

    // Close menu on link click
    mobileMenu.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', function() {
        mobileMenu.classList.remove('open');
        mobileBtn.textContent = '☰';
      });
    });
  }

  // Scroll observer animations
  var observerOptions = { threshold: 0.08, rootMargin: '0px 0px -40px 0px' };
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.kd-observe').forEach(function(el) {
    observer.observe(el);
  });

  // Also animate animate-in elements
  var animObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
        animObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.kd-product-card, .kd-exam-card, .kd-testimonial-card, .kd-blog-card, .kd-sample-card, .kd-info-card, .kd-related-card').forEach(function(el) {
    el.style.opacity = '0';
    animObserver.observe(el);
  });
})();
