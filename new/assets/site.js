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

  /* ---- docs: filter the contents -------------------------------------- */
  var filter = document.getElementById('toc-filter');
  if (filter) {
    var groups = [].slice.call(document.querySelectorAll('.toc-group'));
    var none = document.getElementById('toc-none');

    var apply = function () {
      var q = filter.value.trim().toLowerCase();
      var shown = 0;
      groups.forEach(function (g) {
        var items = [].slice.call(g.querySelectorAll('li'));
        var head = g.querySelector('h2');
        var headMatch = !q || head.textContent.toLowerCase().indexOf(q) !== -1;
        var kept = 0;
        items.forEach(function (li) {
          var hit = !q || headMatch || li.textContent.toLowerCase().indexOf(q) !== -1;
          li.hidden = !hit;
          if (hit) kept++;
        });
        var keep = kept > 0 || (headMatch && items.length === 0);
        g.hidden = !keep;
        if (keep) shown++;
      });
      if (none) none.hidden = shown !== 0;
    };

    filter.addEventListener('input', apply);
    filter.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { filter.value = ''; apply(); filter.blur(); }
    });
    /* "/" focuses the filter, the way a search box on a docs page usually does */
    document.addEventListener('keydown', function (e) {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      var t = e.target;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      e.preventDefault();
      filter.focus();
      filter.select();
    });
  }

  /* ---- docs: highlight the section you are reading -------------------- */
  var toc = document.querySelector('.toc-body') || document.querySelector('.docs-toc');
  if (toc && 'IntersectionObserver' in window) {
    var links = {};
    Array.prototype.forEach.call(toc.querySelectorAll('a[href^="#"]'), function (a) {
      links[a.getAttribute('href').slice(1)] = a;
    });
    var targets = Object.keys(links)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);

    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var a = links[en.target.id];
        if (!a || a === current) return;
        if (current) current.classList.remove('on');
        a.classList.add('on');
        current = a;
        /* keep the active entry in view inside the sticky column */
        if (toc.scrollHeight > toc.clientHeight) {
          var top = a.offsetTop - toc.clientHeight / 2;
          toc.scrollTo({ top: top < 0 ? 0 : top, behavior: 'smooth' });
        }
      });
    }, { rootMargin: '-74px 0px -70% 0px', threshold: 0 });

    targets.forEach(function (t) { io.observe(t); });
  }
})();
