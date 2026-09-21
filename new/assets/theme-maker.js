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

  var maker = document.getElementById('maker');
  if (!maker) return;

  /* ---- the palette -------------------------------------------------- */
  var FIELDS = [
    ['bg',       'Background',      'page',
     'Behind everything.'],
    ['card',     'Section',         'page',
     'Each section sits on this.'],
    ['row',      'Table row',       'page',
     'Rows in the tables.'],
    ['row-alt',  'Row, alternate',  'page',
     'Every second row, and hover.'],
    ['line',     'Rules & borders', 'page',
     'Hairlines between things.'],

    ['fg',       'Text',            'text',
     'Normal text and figures.'],
    ['muted',    'Quiet text',      'text',
     'Column titles, notes, captions.'],
    ['head',     'Headings',        'text',
     'The page title and section titles.'],
    ['accent',   'Accent',          'text',
     'Links, bars, the marker on the section you are reading.'],

    ['blue',     'Night 0–5h',      'time',  ''],
    ['green',    'Morning 6–11h',   'time',  ''],
    ['yellow',   'Afternoon 12–17h','time',  ''],
    ['red',      'Evening 18–23h',  'time',  ''],

    ['male',     'Male',            'sex',   ''],
    ['female',   'Female',          'sex',   '']
  ];

  var PRESETS = {
    modern: {
      mode: 'light',
      bg: '#f5f6f8', fg: '#1c2128', muted: '#66707c', card: '#ffffff', row: '#ffffff',
      'row-alt': '#eef1f5', line: '#d3d9e1', accent: '#2563eb', head: '#1c2128',
      blue: '#60a5fa', green: '#34d399', yellow: '#fbbf24', red: '#f87171',
      male: '#2563eb', female: '#db2777'
    },
    midnight: {
      mode: 'dark',
      bg: '#0e1116', fg: '#e6e9ee', muted: '#8b95a3', card: '#171b22', row: '#141820',
      'row-alt': '#1c212a', line: '#2f3743', accent: '#7aa2ff', head: '#f2f4f8',
      blue: '#5b8def', green: '#2fbf8f', yellow: '#e5b13a', red: '#ef6b6b',
      male: '#7aa2ff', female: '#ff8fc0'
    },
    amoled: {
      mode: 'dark',
      bg: '#000000', fg: '#e6e9ee', muted: '#8b95a3', card: '#0b0b0f', row: '#050508',
      'row-alt': '#101018', line: '#2b2b3c', accent: '#b18cff', head: '#f2f4f8',
      blue: '#5b8def', green: '#2fbf8f', yellow: '#e5b13a', red: '#ef6b6b',
      male: '#9db4ff', female: '#ff9fd0'
    },
    terminal: {
      mode: 'dark',
      bg: '#050805', fg: '#b7f5b7', muted: '#5f9a5f', card: '#0a120a', row: '#080e08',
      'row-alt': '#0f1a0f', line: '#215021', accent: '#3dff7a', head: '#3dff7a',
      blue: '#2f9bff', green: '#3dff7a', yellow: '#f0e040', red: '#ff5f5f',
      male: '#6fd0ff', female: '#ff8ad8'
    }
  };

  var state = clone(PRESETS.midnight);
  var name = 'mytheme';
  var template = null;          /* the modern stylesheet, fetched once */

  function clone(o) { var c = {}; for (var k in o) c[k] = o[k]; return c; }

  /* ---- colour helpers ------------------------------------------------ */
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
    if (!d) return null;                                  /* grey: no hue */
    var x = max === c[0] ? ((c[1] - c[2]) / d) % 6
          : max === c[1] ? (c[2] - c[0]) / d + 2
          : (c[0] - c[1]) / d + 4;
    return (x * 60 + 360) % 360;
  }
  function hueGap(a, b) {
    var x = hue(a), y = hue(b);
    if (x === null || y === null) return 180;             /* one is grey: treat as far */
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

  /* ---- build the stylesheet ------------------------------------------ */
  function shadow() {
    return state.mode === 'light'
      ? '0 1px 2px rgba(16,24,40,.06), 0 8px 24px rgba(16,24,40,.06)'
      : '0 1px 2px rgba(0,0,0,.5), 0 10px 28px rgba(0,0,0,.35)';
  }

  function vars(indent) {
    var pad = indent || '  ';
    var out = [pad + 'color-scheme: ' + state.mode + ';'];
    FIELDS.forEach(function (f) { out.push(pad + '--' + f[0] + ': ' + state[f[0]] + ';'); });
    out.push(pad + '--shadow: ' + shadow() + ';');
    return out.join('\n');
  }

  function css() {
    var head =
      '/* <!-- pisg theme: ' + name + ' - made with the theme creator at\n' +
      '   https://pisg.github.io/themes/  Palette below; everything under it is layout,\n' +
      '   taken unchanged from the shipped "modern" scheme. --> */\n';

    var root = ':root {\n' + vars() + '\n}\n\n' +
      '/* <!-- one palette, whatever the reader\'s system setting is --> */\n' +
      '@media (prefers-color-scheme: dark) {\n  :root {\n' + vars('    ') + '\n  }\n}\n';

    if (!template) return head + root;

    /* replace the template's own palette blocks with ours */
    var body = template
      .replace(/\/\* <!-- pisg theme[\s\S]*?--> \*\/\s*/, '')
      .replace(/:root \{[\s\S]*?\n\}\n/, '')
      .replace(/@media \(prefers-color-scheme: dark\) \{\s*:root \{[\s\S]*?\n  \}\n\}\n/, '');

    return head + root + body.replace(/^\s+/, '\n');
  }

  /* ---- preview -------------------------------------------------------- */
  var frame = document.getElementById('mk-iframe');

  function paint() {
    if (!frame || !frame.contentDocument) return;
    var d = frame.contentDocument;
    var tag = d.getElementById('mk-live');
    if (!tag) {
      tag = d.createElement('style');
      tag.id = 'mk-live';
      (d.head || d.documentElement).appendChild(tag);
    }
    tag.textContent = ':root {\n' + vars() + '\n}\n' +
      '@media (prefers-color-scheme: dark) { :root {\n' + vars() + '\n} }';

    /* the sample page carries a "back to all themes" line of its own;
       inside this little frame it is just noise */
    var note = d.querySelector('p.subtitle a[href*="themes"]');
    if (note && note.parentNode) note.parentNode.style.display = 'none';
  }
  if (frame) frame.addEventListener('load', paint);

  /* ---- the controls --------------------------------------------------- */
  var inputs = {};

  function buildControls() {
    var groups = { page: [], text: [], time: [], sex: [] };

    FIELDS.forEach(function (f) {
      var key = f[0], label = f[1], group = f[2], hint = f[3];
      var wrap = document.createElement('label');
      wrap.className = 'mk-swatch';
      wrap.innerHTML =
        '<input type="color" data-k="' + key + '" aria-label="' + label + '">' +
        '<span class="mk-meta"><b>' + label + '</b>' +
        '<input type="text" class="mk-hex" data-k="' + key + '" spellcheck="false" ' +
        'autocomplete="off" maxlength="7" aria-label="' + label + ' hex value">' +
        (hint ? '<small>' + hint + '</small>' : '') + '</span>';
      groups[group].push(wrap);

      var color = wrap.querySelector('input[type=color]');
      var text = wrap.querySelector('.mk-hex');
      inputs[key] = { color: color, text: text };

      color.addEventListener('input', function () { set(key, color.value); });
      text.addEventListener('change', function () {
        var v = hex(text.value);
        if (v) set(key, v); else render();
      });
    });

    Object.keys(groups).forEach(function (g) {
      var host = document.getElementById('mk-group-' + g);
      groups[g].forEach(function (el) { host.appendChild(el); });
    });
  }

  function set(key, value) {
    var v = hex(value);
    if (!v) return;
    state[key] = v;
    touched = true;
    render();
  }

  /* ---- contrast readout ------------------------------------------------ */
  function contrast() {
    var host = document.getElementById('mk-contrast');
    var checks = [
      ['Text on section', state.fg, state.card, 4.5],
      ['Quiet text on section', state.muted, state.card, 4.5],
      ['Accent on section', state.accent, state.card, 3],
      ['Headings on background', state.head, state.bg, 4.5]
    ];
    /* The four time-of-day colours sit side by side in the bars, so what matters is
       whether a reader can tell them apart — a difference in hue or in lightness.
       A contrast ratio is the wrong tool here: blue and red can be plainly different
       and still score 1.1:1. */
    var pairs = [['blue', 'green'], ['blue', 'yellow'], ['blue', 'red'],
                 ['green', 'yellow'], ['green', 'red'], ['yellow', 'red']];
    var worst = 999, worstPair = '', worstLum = 1;
    pairs.forEach(function (p) {
      var gap = hueGap(state[p[0]], state[p[1]]);
      var lr = ratio(state[p[0]], state[p[1]]);
      /* either a clear hue difference or a clear lightness difference will do */
      var score = gap + (lr - 1) * 40;
      if (score < worst) { worst = score; worstPair = p[0] + ' / ' + p[1]; worstLum = gap; }
    });

    host.innerHTML = checks.map(function (c) {
      var r = ratio(c[1], c[2]);
      var ok = r >= c[3];
      return '<li class="' + (ok ? 'ok' : 'bad') + '"><span>' + c[0] + '</span>' +
             '<b>' + r.toFixed(1) + ':1</b><em>' + (ok ? 'passes' : 'needs ' + c[3] + ':1') + '</em></li>';
    }).join('') +
      '<li class="' + (worst >= 25 ? 'ok' : 'bad') + '"><span>Time colours, closest pair</span><b>' +
      Math.round(worstLum) + '&deg;</b><em>' +
      (worst >= 25 ? 'far enough apart' : 'too close: ' + worstPair) + '</em></li>';
  }

  /* ---- render everything ------------------------------------------------ */
  var cssBox = document.getElementById('mk-css');
  var dl = document.getElementById('mk-download');
  var blobUrl = null;

  function render() {
    FIELDS.forEach(function (f) {
      var k = f[0];
      if (inputs[k]) {
        inputs[k].color.value = state[k];
        /* Chrome paints its own swatch inconsistently once the control is restyled,
           so the background is set here too: what you see is always the value. */
        inputs[k].color.style.backgroundColor = state[k];
        if (document.activeElement !== inputs[k].text) inputs[k].text.value = state[k];
      }
    });

    var text = css();
    cssBox.textContent = text;
    cssBox.dataset.css = text;

    document.getElementById('mk-filename').textContent = name + '.css';
    document.getElementById('mk-path').textContent = 'layout/' + name + '.css';
    document.getElementById('mk-set').textContent = '<set ColorScheme="' + name + '">';
    document.getElementById('mk-frame-title').textContent = '#teatime — ' + name;

    if (blobUrl) URL.revokeObjectURL(blobUrl);
    blobUrl = URL.createObjectURL(new Blob([text], { type: 'text/css' }));
    dl.href = blobUrl;
    dl.setAttribute('download', name + '.css');

    contrast();
    paint();
    writeHash();
  }

  /* ---- the palette travels in the URL, not in storage --------------------
     Nothing is written until the reader actually changes something, so arriving
     at /themes/#creator still jumps to the creator. */
  var touched = false;
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
    return true;
  }

  /* ---- buttons ----------------------------------------------------------- */
  function wire() {
    var nameBox = document.getElementById('mk-name');
    var mode = document.getElementById('mk-mode');
    var preset = document.getElementById('mk-preset');

    nameBox.addEventListener('input', function () {
      var v = nameBox.value.replace(/[^A-Za-z0-9_-]/g, '').slice(0, 32);
      name = v || 'mytheme';
      touched = true;
      render();
    });

    mode.addEventListener('change', function () { state.mode = mode.value; touched = true; render(); });

    preset.addEventListener('change', function () {
      var p = PRESETS[preset.value];
      if (!p) return;
      state = clone(p);
      mode.value = state.mode;
      touched = true;
      render();
    });

    document.getElementById('mk-reset').addEventListener('click', function () {
      preset.value = 'midnight';
      state = clone(PRESETS.midnight);
      mode.value = state.mode;
      nameBox.value = name = 'mytheme';
      touched = true;
      render();
    });

    document.getElementById('mk-shuffle').addEventListener('click', function () {
      var dark = state.mode === 'dark';
      var h = Math.floor(Math.random() * 360);
      var s = 55 + Math.floor(Math.random() * 30);
      state.bg       = dark ? hsl2hex(h, 18, 6 + Math.random() * 5)  : hsl2hex(h, 22, 96);
      state.card     = dark ? hsl2hex(h, 16, 11) : '#ffffff';
      state.row      = dark ? hsl2hex(h, 16, 9)  : '#ffffff';
      state['row-alt'] = dark ? hsl2hex(h, 16, 15) : hsl2hex(h, 24, 93);
      state.line     = dark ? hsl2hex(h, 14, 24) : hsl2hex(h, 18, 84);
      state.fg       = dark ? hsl2hex(h, 14, 90) : hsl2hex(h, 20, 13);
      state.muted    = dark ? hsl2hex(h, 10, 62) : hsl2hex(h, 10, 42);
      state.head     = state.fg;
      state.accent   = hsl2hex(h + 150, s, dark ? 66 : 45);
      /* the four time colours stay a spread around the wheel, so they never collide */
      state.blue     = hsl2hex(h + 200, s, dark ? 62 : 58);
      state.green    = hsl2hex(h + 120, s, dark ? 55 : 45);
      state.yellow   = hsl2hex(h + 45,  s + 10, dark ? 58 : 48);
      state.red      = hsl2hex(h + 350, s, dark ? 64 : 55);
      state.male     = state.blue;
      state.female   = hsl2hex(h + 320, s, dark ? 70 : 55);
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

  /* ---- start -------------------------------------------------------------- */
  buildControls();
  wire();

  if (readHash()) {
    document.getElementById('mk-name').value = name;
    document.getElementById('mk-mode').value = state.mode;
    touched = true;               /* they arrived with a palette: keep it in the URL */
  }
  render();

  /* the stylesheet of the shipped theme is the template for the download */
  fetch('../demo/themes/modern.html')
    .then(function (r) { return r.ok ? r.text() : Promise.reject(); })
    .then(function (html) {
      var m = /<style type="text\/css" title="[^"]*">([\s\S]*?)<\/style>/.exec(html);
      if (m) { template = m[1]; render(); }
    })
    .catch(function () { /* no template: the palette block alone is still valid CSS */ });
})();
