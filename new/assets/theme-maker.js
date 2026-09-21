/* ===========================================================================
   pisg theme creator
   Builds a pisg colour scheme in the browser: pick a palette, watch a real
   generated stats page restyle itself, take the CSS file away.

   How it works: the stylesheet of the shipped "modern" theme is fetched from
   the sample page on this site, its palette block is swapped for yours, and
   the result is both injected into the preview frame and offered as a file.
   Nothing is uploaded and nothing is stored — the palette lives in the URL.
   =========================================================================== */
(function () {
  'use strict';

  if (!document.getElementById('maker')) return;

  /* ---- the palette ---------------------------------------------------- */
  var FIELDS = [
    ['bg',       'Background',       'page', 'Behind everything'],
    ['card',     'Section',          'page', 'Each section sits on this'],
    ['row',      'Table row',        'page', 'Rows in the tables'],
    ['row-alt',  'Row, alternate',   'page', 'Every second row, and hover'],
    ['line',     'Rules & borders',  'page', 'Hairlines between things'],

    ['fg',       'Text',             'text', 'Normal text and figures'],
    ['muted',    'Quiet text',       'text', 'Column titles, notes, captions'],
    ['head',     'Headings',         'text', 'Page title and section titles'],
    ['accent',   'Accent',           'text', 'Links, bars, the section marker'],

    ['blue',     'Night',            'time', '0–5h'],
    ['green',    'Morning',          'time', '6–11h'],
    ['yellow',   'Afternoon',        'time', '12–17h'],
    ['red',      'Evening',          'time', '18–23h'],

    ['male',     'Male',             'sex',  ''],
    ['female',   'Female',           'sex',  '']
  ];

  var MODERN = [
    ['midnight', {
      mode: 'dark',
      bg: '#0e1116', fg: '#e6e9ee', muted: '#8b95a3', card: '#171b22', row: '#141820',
      'row-alt': '#1c212a', line: '#2f3743', accent: '#7aa2ff', head: '#f2f4f8',
      blue: '#5b8def', green: '#2fbf8f', yellow: '#e5b13a', red: '#ef6b6b',
      male: '#7aa2ff', female: '#ff8fc0'
    }],
    ['modern', {
      mode: 'light',
      bg: '#f5f6f8', fg: '#1c2128', muted: '#66707c', card: '#ffffff', row: '#ffffff',
      'row-alt': '#eef1f5', line: '#d3d9e1', accent: '#2563eb', head: '#1c2128',
      blue: '#60a5fa', green: '#34d399', yellow: '#fbbf24', red: '#f87171',
      male: '#2563eb', female: '#db2777'
    }],
    ['amoled', {
      mode: 'dark',
      bg: '#000000', fg: '#e6e9ee', muted: '#8b95a3', card: '#0b0b0f', row: '#050508',
      'row-alt': '#101018', line: '#2b2b3c', accent: '#b18cff', head: '#f2f4f8',
      blue: '#5b8def', green: '#2fbf8f', yellow: '#e5b13a', red: '#ef6b6b',
      male: '#9db4ff', female: '#ff9fd0'
    }],
    ['terminal', {
      mode: 'dark',
      bg: '#050805', fg: '#b7f5b7', muted: '#5f9a5f', card: '#0a120a', row: '#080e08',
      'row-alt': '#0f1a0f', line: '#215021', accent: '#3dff7a', head: '#3dff7a',
      blue: '#2f9bff', green: '#3dff7a', yellow: '#f0e040', red: '#ff5f5f',
      male: '#6fd0ff', female: '#ff8ad8'
    }]
  ];

  /* The eight classic schemes, converted from their own CSS by
     tools/make-classic-palettes.py — including the four bar colours,
     decoded out of each theme's own sprite. Do not edit by hand. */
  var CLASSIC = [
    ['default', 'The page pisg has written since 2001', {
      mode: 'light', bg: '#dedeee', card: '#babadd', row: '#babadd', 'row-alt': '#cccccc',
      line: '#c8c8dd', fg: '#000000', muted: '#545463', head: '#5050a5', accent: '#0b407a',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#0000dd',
      female: '#ac1d48'
    }],
    ['pisg', 'The project’s own blue', {
      mode: 'light', bg: '#ffffff', card: '#f0f0f0', row: '#f0f0f0', 'row-alt': '#e2e2e2',
      line: '#bbbbbb', fg: '#000000', muted: '#6c6c6c', head: '#898500', accent: '#0b407a',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#0b407a',
      female: '#0b407a'
    }],
    ['darkgalaxy', 'Dark blue, the first dark theme pisg shipped', {
      mode: 'dark', bg: '#000000', card: '#19354e', row: '#19354e', 'row-alt': '#444444',
      line: '#718292', fg: '#dedede', muted: '#85929d', head: '#ea515d', accent: '#b5c6d5',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#b5c6d5',
      female: '#b5c6d5'
    }],
    ['darkred', 'Dark with a red accent', {
      mode: 'dark', bg: '#000000', card: '#121212', row: '#121212', 'row-alt': '#272727',
      line: '#444444', fg: '#ffffff', muted: '#949494', head: '#ffffff', accent: '#eb0000',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#e00000',
      female: '#e00000'
    }],
    ['justgrey', 'Grey on grey, nothing shouting', {
      mode: 'dark', bg: '#647684', card: '#748494', row: '#748494', 'row-alt': '#818f9e',
      line: '#445464', fg: '#ffffff', muted: '#1e303f', head: '#ffffff', accent: '#f5f7fa',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#f0f0ff',
      female: '#fff0fb'
    }],
    ['ocean', 'Cool blues', {
      mode: 'dark', bg: '#000033', card: '#000066', row: '#000066', 'row-alt': '#171774',
      line: '#336699', fg: '#dedede', muted: '#7a7aa8', head: '#006bd6', accent: '#99ccff',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#99ccff',
      female: '#99ccff'
    }],
    ['orange_grey', 'Grey with an orange accent', {
      mode: 'light', bg: '#ededed', card: '#dddddd', row: '#dddddd', 'row-alt': '#bbbbbb',
      line: '#bbbbbb', fg: '#000000', muted: '#636363', head: '#9f6a01', accent: '#002597',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#0000dd',
      female: '#d8245a'
    }],
    ['softgreen', 'Pale green, easy on the eyes', {
      mode: 'light', bg: '#dfffd1', card: '#c1ddb5', row: '#c1ddb5', 'row-alt': '#b4cea9',
      line: '#cdebc1', fg: '#000000', muted: '#576351', head: '#000000', accent: '#007400',
      blue: '#3366ff', green: '#66cc33', yellow: '#cccc33', red: '#cc3333', male: '#007e00',
      female: '#007e00'
    }],
  ];

  var THEMES = MODERN.concat(CLASSIC);

  function preset(nm) {
    for (var i = 0; i < THEMES.length; i++) if (THEMES[i][0] === nm) return THEMES[i][1];
    return MODERN[0][1];
  }
  function clone(o) { var c = {}; for (var k in o) c[k] = o[k]; return c; }

  var state = clone(preset('midnight'));
  var name = 'mytheme';
  var from = 'midnight';          /* which preset the palette came from, if unchanged */
  var template = null;            /* the modern stylesheet, fetched once */
  var touched = false;            /* nothing goes in the URL until an actual edit */

  /* ---- colour helpers -------------------------------------------------- */
  function hex(v) {
    v = String(v || '').trim();
    if (v[0] !== '#') v = '#' + v;
    if (/^#[0-9a-f]{3}$/i.test(v)) v = '#' + v[1] + v[1] + v[2] + v[2] + v[3] + v[3];
    return /^#[0-9a-f]{6}$/i.test(v) ? v.toLowerCase() : null;
  }
  function rgb(h) {
    return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  }
  function lum(h) {
    return rgb(h).map(function (c) {
      c /= 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    }).reduce(function (a, c, i) { return a + c * [0.2126, 0.7152, 0.0722][i]; }, 0);
  }
  function ratio(a, b) {
    var l1 = lum(a), l2 = lum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }
  function hue(h) {
    var c = rgb(h).map(function (v) { return v / 255; });
    var max = Math.max.apply(null, c), min = Math.min.apply(null, c), d = max - min;
    if (!d) return null;                                   /* grey: no hue */
    var x = max === c[0] ? ((c[1] - c[2]) / d) % 6
          : max === c[1] ? (c[2] - c[0]) / d + 2
          : (c[0] - c[1]) / d + 4;
    return (x * 60 + 360) % 360;
  }
  function hueGap(a, b) {
    var x = hue(a), y = hue(b);
    if (x === null || y === null) return 180;              /* one is grey: far enough */
    var d = Math.abs(x - y) % 360;
    return d > 180 ? 360 - d : d;
  }
  function hsl2hex(h, s, l) {
    h = (h % 360 + 360) % 360; s /= 100; l /= 100;
    var c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = l - c / 2;
    var t = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x]
          : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
    return '#' + t.map(function (v) {
      return ('0' + Math.round((v + m) * 255).toString(16)).slice(-2);
    }).join('');
  }

  /* ---- the stylesheet --------------------------------------------------- */
  function shadow() {
    return state.mode === 'light'
      ? '0 1px 2px rgba(16,24,40,.06), 0 8px 24px rgba(16,24,40,.06)'
      : '0 1px 2px rgba(0,0,0,.5), 0 10px 28px rgba(0,0,0,.35)';
  }
  function vars(pad) {
    pad = pad || '  ';
    var out = [pad + 'color-scheme: ' + state.mode + ';'];
    FIELDS.forEach(function (f) { out.push(pad + '--' + f[0] + ': ' + state[f[0]] + ';'); });
    out.push(pad + '--shadow: ' + shadow() + ';');
    return out.join('\n');
  }
  function css() {
    var head =
      '/* <!-- pisg theme: ' + name + ' - made with the theme creator at\n' +
      '   https://pisg.github.io/themes/  The palette is below; everything under it is\n' +
      '   layout, taken unchanged from the shipped "modern" scheme. --> */\n';

    var root = ':root {\n' + vars() + '\n}\n\n' +
      '/* <!-- one palette, whatever the reader\'s system setting is --> */\n' +
      '@media (prefers-color-scheme: dark) {\n  :root {\n' + vars('    ') + '\n  }\n}\n';

    if (!template) return head + root;

    var body = template
      .replace(/\/\* <!-- pisg theme[\s\S]*?--> \*\/\s*/, '')
      .replace(/:root \{[\s\S]*?\n\}\n/, '')
      .replace(/@media \(prefers-color-scheme: dark\) \{\s*:root \{[\s\S]*?\n  \}\n\}\n/, '');

    return head + root + body.replace(/^\s+/, '\n');
  }

  /* a little colour in the code box: comments, property names, values */
  function highlight(text) {
    var esc = text.replace(/[&<>]/g, function (ch) {
      return ch === '&' ? '&amp;' : ch === '<' ? '&lt;' : '&gt;';
    });
    return esc
      .replace(/(\/\*[\s\S]*?\*\/)/g, '<span class="c">$1</span>')
      .replace(/(--[a-z-]+)(:\s*)([^;\n]+)/g, '<span class="k">$1</span>$2<span class="v">$3</span>');
  }

  /* ---- preview ----------------------------------------------------------- */
  var frame = document.getElementById('mk-iframe');

  function paint() {
    if (!frame || !frame.contentDocument) return;
    var d = frame.contentDocument;
    var host = d.head || d.documentElement;
    if (!host) return;                 /* the frame has not parsed yet; its load event repaints */
    var tag = d.getElementById('mk-live');
    if (!tag) {
      tag = d.createElement('style');
      tag.id = 'mk-live';
      host.appendChild(tag);
    }
    tag.textContent = ':root {\n' + vars() + '\n}\n' +
      '@media (prefers-color-scheme: dark) { :root {\n' + vars() + '\n} }';

    /* The example pages carry a line explaining what they are, and the sample
       pages a "back to all themes" link. Inside this frame both are noise, so
       any subtitle that links back into this site is hidden. */
    [].slice.call(d.querySelectorAll('p.subtitle')).forEach(function (para) {
      if (para.querySelector('a[href^="../"]')) para.style.display = 'none';
    });
  }
  if (frame) frame.addEventListener('load', paint);

  /* ---- controls ----------------------------------------------------------- */
  var inputs = {};

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  function buildColors() {
    FIELDS.forEach(function (f) {
      var key = f[0], label = f[1], group = f[2], hint = f[3];
      var row = el('label', 'mk-color');
      row.innerHTML =
        '<input type="color" data-k="' + key + '" aria-label="' + label + '">' +
        '<span class="mk-color-body"><b>' + label + '</b>' +
        (hint ? '<small>' + hint + '</small>' : '') + '</span>' +
        '<input type="text" class="mk-hex" spellcheck="false" autocomplete="off" maxlength="7" ' +
        'aria-label="' + label + ' hex value">';
      document.getElementById('mk-group-' + group).appendChild(row);

      var color = row.querySelector('input[type=color]');
      var text = row.querySelector('.mk-hex');
      inputs[key] = { color: color, text: text };

      color.addEventListener('input', function () { set(key, color.value); });
      text.addEventListener('change', function () {
        var v = hex(text.value);
        if (v) set(key, v); else render();
      });
      text.addEventListener('keydown', function (e) { if (e.key === 'Enter') text.blur(); });
    });
  }

  function buildThemeList() {
    var add = function (hostId, list) {
      var host = document.getElementById(hostId);
      if (!host) return;
      list.forEach(function (p) {
        var nm = p[0], blurb = p[1], pal = p[2] || p[1];
        if (typeof blurb !== 'string' || p.length < 3) blurb = '';
        var b = el('button', 'thm' + (nm === from ? ' on' : ''));
        b.type = 'button';
        b.dataset.p = nm;
        b.title = blurb || nm;
        b.innerHTML = '<span class="thm-sw">' +
          ['bg', 'card', 'accent', 'green', 'yellow', 'red'].map(function (k) {
            return '<i style="background:' + pal[k] + '"></i>';
          }).join('') + '</span><span class="thm-name">' + nm + '</span>';
        b.addEventListener('click', function () {
          state = clone(pal);
          from = nm;
          name = nm;
          document.getElementById('mk-name').value = nm;
          touched = true;
          render();
          if (window.innerWidth <= 1000) {
            var sb = document.getElementById('sidebar');
            if (sb) sb.classList.remove('open');
          }
        });
        host.appendChild(b);
      });
    };

    add('thm-modern', MODERN.map(function (p) { return [p[0], '', p[1]]; }));
    add('thm-classic', CLASSIC);
  }

  function buildStrip() {
    var host = document.getElementById('mk-strip');
    FIELDS.forEach(function () { host.appendChild(document.createElement('span')); });
  }

  /* segmented switches: base (dark/light) and preview width */
  function segment(id, onPick) {
    var host = document.getElementById(id);
    host.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      [].slice.call(host.querySelectorAll('button')).forEach(function (x) {
        x.classList.toggle('on', x === b);
      });
      onPick(b.dataset.v);
    });
  }

  function set(key, value) {
    var v = hex(value);
    if (!v) return;
    state[key] = v;
    from = null;
    touched = true;
    render();
  }

  /* ---- readability -------------------------------------------------------- */
  function readability() {
    var host = document.getElementById('mk-contrast');
    var checks = [
      ['Text on a section', state.fg, state.card, 4.5],
      ['Quiet text on a section', state.muted, state.card, 4.5],
      ['Accent on a section', state.accent, state.card, 3],
      ['Headings on the background', state.head, state.bg, 4.5]
    ];

    /* Side by side in the bars, what matters is telling the four time colours
       apart: a difference in hue, or in lightness. A contrast ratio is the wrong
       tool — blue and red can be plainly different and still score 1.1:1. */
    var pairs = [['blue', 'green'], ['blue', 'yellow'], ['blue', 'red'],
                 ['green', 'yellow'], ['green', 'red'], ['yellow', 'red']];
    var worstScore = 1e9, worstGap = 0, worstPair = '';
    pairs.forEach(function (p) {
      var gap = hueGap(state[p[0]], state[p[1]]);
      var score = gap + (ratio(state[p[0]], state[p[1]]) - 1) * 40;
      if (score < worstScore) {
        worstScore = score; worstGap = gap; worstPair = p[0] + ' / ' + p[1];
      }
    });

    host.innerHTML = checks.map(function (c) {
      var r = ratio(c[1], c[2]), ok = r >= c[3];
      return '<li class="' + (ok ? 'ok' : 'bad') + '"><span>' + c[0] + '</span><b>' +
             r.toFixed(1) + ':1</b><em>' + (ok ? 'pass' : 'needs ' + c[3]) + '</em></li>';
    }).join('') +
      '<li class="' + (worstScore >= 25 ? 'ok' : 'bad') + '"><span>Closest time colours<br>' +
      '<small style="color:var(--faint)">' + worstPair + '</small></span><b>' +
      Math.round(worstGap) + '&deg;</b><em>' +
      (worstScore >= 25 ? 'distinct' : 'too close') + '</em></li>';
  }

  /* ---- render -------------------------------------------------------------- */
  var cssBox = document.getElementById('mk-css');
  var dls = [document.getElementById('mk-download'),
             document.getElementById('mk-download-2')].filter(Boolean);
  var strip = document.getElementById('mk-strip');
  var blobUrl = null;

  function render() {
    FIELDS.forEach(function (f, i) {
      var k = f[0];
      if (inputs[k]) {
        inputs[k].color.value = state[k];
        /* Chrome paints a restyled colour input inconsistently, so the background
           is set here as well: what you see is always the value. */
        inputs[k].color.style.backgroundColor = state[k];
        if (document.activeElement !== inputs[k].text) inputs[k].text.value = state[k];
      }
      if (strip.children[i]) strip.children[i].style.backgroundColor = state[k];
    });

    [].slice.call(document.querySelectorAll('.thm')).forEach(function (b) {
      b.classList.toggle('on', b.dataset.p === from);
    });
    [].slice.call(document.querySelectorAll('#mk-mode button')).forEach(function (b) {
      b.classList.toggle('on', b.dataset.v === state.mode);
    });

    var text = css();
    cssBox.innerHTML = highlight(text);
    cssBox.dataset.css = text;

    document.getElementById('mk-filename').textContent = name + '.css';
    document.getElementById('mk-path').textContent = 'layout/' + name + '.css';
    document.getElementById('mk-set').textContent = '<set ColorScheme="' + name + '">';
    document.getElementById('mk-frame-title').textContent = '#nightshift — ' + name;

    if (blobUrl) URL.revokeObjectURL(blobUrl);
    blobUrl = URL.createObjectURL(new Blob([text], { type: 'text/css' }));
    dls.forEach(function (a) {
      a.href = blobUrl;
      a.setAttribute('download', name + '.css');
    });

    readability();
    paint();
    writeHash();
  }

  /* ---- the palette travels in the URL, not in storage ----------------------- */
  function writeHash() {
    if (!touched) return;
    var parts = [state.mode, name].concat(FIELDS.map(function (f) { return state[f[0]].slice(1); }));
    history.replaceState(null, '', '#t=' + parts.join('-'));
  }
  function readHash() {
    var m = /#t=([a-z]+)-([A-Za-z0-9_-]{1,32})-([0-9a-f-]+)$/.exec(location.hash);
    if (!m) return false;
    var cols = m[3].split('-');
    if (cols.length !== FIELDS.length) return false;
    state.mode = m[1] === 'light' ? 'light' : 'dark';
    name = m[2];
    FIELDS.forEach(function (f, i) {
      var v = hex(cols[i]);
      if (v) state[f[0]] = v;
    });
    from = null;
    return true;
  }

  /* ---- buttons --------------------------------------------------------------- */
  function copy(btn, text, label) {
    var done = function (ok) {
      btn.textContent = ok ? 'Copied' : 'Ctrl+C';
      btn.classList.toggle('ok', ok);
      setTimeout(function () { btn.textContent = label; btn.classList.remove('ok'); }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
    } else {
      done(false);
    }
  }

  function wire() {
    var nameBox = document.getElementById('mk-name');
    nameBox.addEventListener('input', function () {
      var v = nameBox.value.replace(/[^A-Za-z0-9_-]/g, '').slice(0, 32);
      if (v !== nameBox.value) nameBox.value = v;
      name = v || 'mytheme';
      touched = true;
      render();
    });

    segment('mk-mode', function (v) {
      state.mode = v === 'light' ? 'light' : 'dark';
      touched = true;
      render();
    });

    segment('mk-width', function (v) {
      document.getElementById('mk-frame-body').classList.toggle('narrow', v === 'narrow');
    });

    document.getElementById('mk-reset').addEventListener('click', function () {
      state = clone(preset('midnight'));
      from = 'midnight';
      nameBox.value = name = 'mytheme';
      touched = true;
      render();
    });

    document.getElementById('mk-shuffle').addEventListener('click', function () {
      var dark = state.mode === 'dark';
      var h = Math.floor(Math.random() * 360);
      var s = 55 + Math.floor(Math.random() * 30);
      state.bg         = dark ? hsl2hex(h, 18, 6 + Math.random() * 5) : hsl2hex(h, 22, 96);
      state.card       = dark ? hsl2hex(h, 16, 11) : '#ffffff';
      state.row        = dark ? hsl2hex(h, 16, 9)  : '#ffffff';
      state['row-alt'] = dark ? hsl2hex(h, 16, 15) : hsl2hex(h, 24, 93);
      state.line       = dark ? hsl2hex(h, 14, 24) : hsl2hex(h, 18, 84);
      state.fg         = dark ? hsl2hex(h, 14, 90) : hsl2hex(h, 20, 13);
      state.muted      = dark ? hsl2hex(h, 10, 62) : hsl2hex(h, 10, 42);
      state.head       = state.fg;
      state.accent     = hsl2hex(h + 150, s, dark ? 66 : 45);
      /* the four time colours keep a spread around the wheel, so they never collide */
      state.blue       = hsl2hex(h + 200, s, dark ? 62 : 58);
      state.green      = hsl2hex(h + 120, s, dark ? 55 : 45);
      state.yellow     = hsl2hex(h + 45, s + 10, dark ? 58 : 48);
      state.red        = hsl2hex(h + 350, s, dark ? 64 : 55);
      state.male       = state.blue;
      state.female     = hsl2hex(h + 320, s, dark ? 70 : 55);
      from = null;
      touched = true;
      render();
    });

    document.getElementById('mk-copy').addEventListener('click', function () {
      copy(this, cssBox.dataset.css || cssBox.textContent, 'Copy CSS');
    });
    document.getElementById('mk-share').addEventListener('click', function () {
      copy(this, location.href, 'Copy link');
    });
  }

  /* ---- start ------------------------------------------------------------------ */
  buildStrip();
  buildColors();
  buildThemeList();
  wire();

  if (readHash()) {
    document.getElementById('mk-name').value = name;
    touched = true;                       /* they arrived with a palette: keep it */
  }
  render();

  /* The stylesheet of the page in the preview is the template for the download:
     it is the current "modern" scheme, including the rules for the sections 1.0a
     added (the relation map, the section menu, the overview). */
  fetch('../demo/nightshift.html')
    .then(function (r) { return r.ok ? r.text() : Promise.reject(); })
    .then(function (html) {
      var m = /<style type="text\/css" title="[^"]*">([\s\S]*?)<\/style>/.exec(html);
      if (m) { template = m[1]; render(); }
    })
    .catch(function () { /* no template: the palette block alone is still valid CSS */ });
})();
