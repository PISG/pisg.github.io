/* ===========================================================================
   pisg.github.io — shared behaviour
   Mobile menu, copy-to-clipboard buttons, docs TOC highlighting.
   No dependencies, no network requests.
   =========================================================================== */
(function () {
  'use strict';

  /* ---- mobile menu ---------------------------------------------------- */
  var btn = document.getElementById('menu-btn');
  var nav = document.getElementById('navlinks');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- copy buttons --------------------------------------------------- */
  /* <button class="copybtn" data-copy="text to copy">Copy</button>
     or a button inside a .copyline / .crow, which copies that row's code. */
  function textFor(el) {
    if (el.dataset.copy) return el.dataset.copy;
    if (el.dataset.target) {
      var named = document.getElementById(el.dataset.target);
      return named ? named.textContent : '';
    }
    var host = el.closest('.copyline') || el.closest('.crow');
    if (!host) return '';
    var src = host.querySelector('code, .cmdline');
    return src ? src.textContent.trim() : '';
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.copybtn') : null;
    if (!b) return;
    var text = textFor(b);
    if (!text) return;

    var done = function (ok) {
      var was = b.dataset.label || b.textContent;
      b.dataset.label = was;
      b.textContent = ok ? 'Copied' : 'Ctrl+C';
      b.classList.toggle('ok', ok);
      setTimeout(function () {
        b.textContent = was;
        b.classList.remove('ok');
      }, 1400);
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
    } else {
      /* older browsers: select the text so Ctrl+C works */
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
      document.body.removeChild(ta);
      done(ok);
    }
  });

  /* ---- docs: sidebar toggle on narrow screens ------------------------- */
  var sideBtn = document.getElementById('side-btn');
  var sidebar = document.getElementById('sidebar');
  if (sideBtn && sidebar) {
    sideBtn.addEventListener('click', function () {
      var open = sidebar.classList.toggle('open');
      sideBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    sidebar.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && window.innerWidth <= 1000) {
        sidebar.classList.remove('open');
        sideBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- docs: filter the options --------------------------------------- */
  var search = document.getElementById('search');
  if (search) {
    var count = document.getElementById('search-count');
    var opts = [].slice.call(document.querySelectorAll('.opt'));
    var pills = [].slice.call(document.querySelectorAll('.pill'));
    var sections = [].slice.call(document.querySelectorAll('.main section[id]'));

    /* the shipped manual spells it "color", the 1.0 text spells it "colour";
       whichever the reader types should find both */
    var norm = function (t) { return t.toLowerCase().replace(/colour/g, 'color'); };

    var apply = function () {
      var q = norm(search.value.trim());
      var n = 0;

      opts.forEach(function (c) {
        var hit = !q
          || norm(c.getAttribute('data-k') || '').indexOf(q) !== -1
          || norm(c.textContent).indexOf(q) !== -1;
        c.classList.toggle('hidden', !hit);
        if (hit) n++;
      });

      pills.forEach(function (p) {
        var id = p.getAttribute('href').slice(1);
        var card = document.getElementById(id);
        p.classList.toggle('hidden', !!card && card.classList.contains('hidden'));
      });

      /* while filtering, hide chapters that have nothing left to show */
      sections.forEach(function (sec) {
        if (!q) { sec.hidden = false; return; }
        var own = sec.querySelectorAll('.opt');
        if (!own.length) {
          sec.hidden = norm(sec.textContent).indexOf(q) === -1;
          return;
        }
        sec.hidden = !sec.querySelector('.opt:not(.hidden)');
      });

      if (count) {
        count.style.display = q ? 'inline' : 'none';
        count.textContent = n + (n === 1 ? ' option' : ' options');
      }

      /* take the reader to the first match instead of leaving them where they were */
      if (q && n) {
        var first = document.querySelector('.opt:not(.hidden)');
        if (first) {
          var y = first.getBoundingClientRect().top + window.scrollY - 90;
          window.scrollTo(0, y < 0 ? 0 : y);
        }
      }
    };

    search.addEventListener('input', apply);
    document.addEventListener('keydown', function (e) {
      var t = e.target;
      var typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if (e.key === '/' && !typing && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        if (sidebar) sidebar.classList.add('open');
        search.focus();
        search.select();
      }
      if (e.key === 'Escape' && document.activeElement === search) {
        search.value = '';
        apply();
        search.blur();
      }
    });
  }

  /* ---- docs: mark the section being read, and the back-to-top button --- */
  var navLinks = [].slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  var topBtn = document.getElementById('top-btn');
  if (navLinks.length || topBtn) {
    var targets = navLinks.map(function (a) {
      return document.getElementById(a.getAttribute('href').slice(1));
    });

    var spy = function () {
      var y = window.scrollY + 130, cur = null;
      targets.forEach(function (t) {
        if (t && !t.hidden && t.offsetTop <= y) cur = t.id;
      });
      navLinks.forEach(function (a) {
        var on = a.getAttribute('href') === '#' + cur;
        if (on && !a.classList.contains('active') && sidebar && sidebar.scrollHeight > sidebar.clientHeight) {
          /* keep the entry being read visible in a sidebar that scrolls on its own */
          var r = a.getBoundingClientRect(), s = sidebar.getBoundingClientRect();
          if (r.top < s.top + 60 || r.bottom > s.bottom - 40) {
            sidebar.scrollTop += r.top - s.top - sidebar.clientHeight / 3;
          }
        }
        a.classList.toggle('active', on);
      });
      if (topBtn) topBtn.style.display = window.scrollY > 600 ? 'block' : 'none';
    };

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () { spy(); ticking = false; });
    });
    spy();

    if (topBtn) {
      topBtn.addEventListener('click', function () {
        /* animate a short hop, jump a long one */
        window.scrollTo({ top: 0, behavior: window.scrollY > 4000 ? 'auto' : 'smooth' });
      });
    }
  }

})();
