/* ============================================
   KNIKVIRA DIGITAL — Shared Page JS
   Navbar scroll effect, mobile menu, scroll animations,
   scroll-to-top button, smooth page transitions
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

  // Also animate product cards, exam cards, etc.
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

  // Scroll-to-top button
  var scrollTopBtn = document.createElement('button');
  scrollTopBtn.id = 'kdScrollTop';
  scrollTopBtn.innerHTML = '↑';
  scrollTopBtn.title = 'Scroll to top';
  scrollTopBtn.setAttribute('aria-label', 'Scroll to top');
  var stStyle = document.createElement('style');
  stStyle.textContent = '#kdScrollTop{position:fixed;bottom:24px;right:24px;width:44px;height:44px;border-radius:12px;background:var(--gradient-primary);color:#fff;font-size:20px;font-weight:800;border:none;cursor:pointer;box-shadow:0 4px 16px rgba(79,70,229,0.35);z-index:999;opacity:0;transform:translateY(20px);transition:all 0.3s ease;pointer-events:none}#kdScrollTop.visible{opacity:1;transform:translateY(0);pointer-events:auto}#kdScrollTop:hover{transform:translateY(-3px);box-shadow:0 6px 24px rgba(79,70,229,0.5)}';
  document.head.appendChild(stStyle);
  document.body.appendChild(scrollTopBtn);

  scrollTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  window.addEventListener('scroll', function() {
    if (window.scrollY > 400) {
      scrollTopBtn.classList.add('visible');
    } else {
      scrollTopBtn.classList.remove('visible');
    }
  }, { passive: true });

  // Smooth page load animation
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.3s ease';
  requestAnimationFrame(function() {
    document.body.style.opacity = '1';
  });
})();
