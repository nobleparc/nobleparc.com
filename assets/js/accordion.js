// Nobleparc — Accordion, nav toggle, and mobile CTA
// Zero dependencies, ~1KB minified

(function(){
  'use strict';

  // Delegated click handler — works for accordion, nav, and everything else
  document.addEventListener('click', function(e) {

    // --- Accordion toggle ---
    var btn = e.target.closest('.faq-question');
    if (btn) {
      e.preventDefault();
      var answer = btn.nextElementSibling;
      var isOpen = btn.getAttribute('aria-expanded') === 'true';

      btn.setAttribute('aria-expanded', String(!isOpen));
      if (answer) answer.classList.toggle('open');

      // Close other open items (one-at-a-time accordion behavior)
      if (!isOpen) {
        var others = document.querySelectorAll('.faq-question[aria-expanded="true"]');
        for (var i = 0; i < others.length; i++) {
          if (others[i] !== btn) {
            others[i].setAttribute('aria-expanded', 'false');
            var otherAns = others[i].nextElementSibling;
            if (otherAns) otherAns.classList.remove('open');
          }
        }
      }
      return;
    }

    // --- Mobile nav toggle ---
    var toggle = e.target.closest('.nav-toggle');
    if (toggle) {
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      var nav = document.querySelector('.nav-links');
      if (nav) nav.classList.toggle('open');
      return;
    }
  });

})();