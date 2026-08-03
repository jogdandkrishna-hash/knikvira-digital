/* ============================================
   KNIKVIRA DIGITAL — Language Switcher
   English / Marathi — localStorage persistence
   Also syncs with interactive product pages (knv_lang)
   ============================================ */

(function() {
  const STORAGE_KEY = 'kd-lang';
  const PRODUCT_LANG_KEY = 'knv_lang'; // used by 3-language product pages

  function getLang() {
    return localStorage.getItem(STORAGE_KEY) || 'mr';
  }

  function setLang(lang) {
    localStorage.setItem(STORAGE_KEY, lang);
    // Sync with interactive product pages' language system
    // Product pages use: 'mr' (Marathi), 'hi' (Hindi), 'en' (English)
    // Main site uses: 'mr' (Marathi), 'en' (English)
    // When main site switches to EN, product pages should show English
    // When main site switches to MR, product pages should show Marathi
    localStorage.setItem(PRODUCT_LANG_KEY, lang);
    applyLang(lang);
    updateToggle(lang);
  }

  function applyLang(lang) {
    // Update html lang attribute
    document.documentElement.lang = lang === 'en' ? 'en' : 'mr';

    // Update all elements with data-en and data-mr attributes
    document.querySelectorAll('[data-en]').forEach(function(el) {
      var text = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-mr');
      if (text) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.placeholder = text;
        } else {
          el.innerHTML = text;
        }
      }
    });

    // Update elements with data-en-placeholder / data-mr-placeholder
    document.querySelectorAll('[data-en-placeholder]').forEach(function(el) {
      el.placeholder = lang === 'en' ? el.getAttribute('data-en-placeholder') : el.getAttribute('data-mr-placeholder');
    });

    // Update page title if data-en-title exists
    var titleEl = document.querySelector('title');
    if (titleEl && titleEl.hasAttribute('data-en')) {
      titleEl.textContent = lang === 'en' ? titleEl.getAttribute('data-en') : titleEl.getAttribute('data-mr');
    }

    // Update meta description if exists
    var descMeta = document.querySelector('meta[name="description"]');
    if (descMeta && descMeta.hasAttribute('data-en')) {
      descMeta.content = lang === 'en' ? descMeta.getAttribute('data-en') : descMeta.getAttribute('data-mr');
    }
  }

  function updateToggle(lang) {
    // Desktop toggle
    document.querySelectorAll('.kd-lang-btn').forEach(function(btn) {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
    // Mobile toggle
    document.querySelectorAll('.kd-lang-btn-mobile').forEach(function(btn) {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
  }

  function init() {
    var lang = getLang();
    
    // On init, also sync knv_lang from kd-lang if kd-lang is set
    // This ensures product pages pick up the right language
    if (localStorage.getItem(STORAGE_KEY)) {
      localStorage.setItem(PRODUCT_LANG_KEY, lang);
    } else {
      // If no kd-lang set, check knv_lang from product pages
      var productLang = localStorage.getItem(PRODUCT_LANG_KEY);
      if (productLang && (productLang === 'en' || productLang === 'mr')) {
        lang = productLang;
        localStorage.setItem(STORAGE_KEY, lang);
      }
    }
    
    applyLang(lang);
    updateToggle(lang);

    // Desktop toggle buttons
    document.querySelectorAll('.kd-lang-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        setLang(btn.getAttribute('data-lang'));
      });
    });

    // Mobile toggle buttons
    document.querySelectorAll('.kd-lang-btn-mobile').forEach(function(btn) {
      btn.addEventListener('click', function() {
        setLang(btn.getAttribute('data-lang'));
      });
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose for manual use
  window.kdSetLang = setLang;
  window.kdGetLang = getLang;
})();
