# -*- coding: utf-8 -*-
"""
Turn the eight classic pisg colour schemes into palettes the 1.0a stylesheet can use.

The classic themes are hand-written CSS from the SourceForge era: they colour the page
with `body`, `.hicell`, `.tdtop`, `.rankc` and friends, and they draw the time-of-day bars
with a four-colour PNG sprite embedded in the file. The 1.0a themes are the same layout
every time, driven by sixteen custom properties.

This reads each classic file, pulls out the colours it actually uses — including the four
bar colours, decoded straight out of the sprite's PLTE chunk — and writes the palette block
that assets/theme-maker.js embeds, so the classics can be picked in the theme creator and
downloaded as modern stylesheets.

    python3 tools/make-classic-palettes.py          # prints the JS block
    python3 tools/make-classic-palettes.py --write  # writes it into assets/theme-maker.js
"""
import base64, io, os, re, struct, sys, zlib

SRC = r'C:\Users\admin\Desktop\pisg\layout'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'assets', 'theme-maker.js')

# name -> how to describe it in the creator
CLASSICS = [
    ('default',     'The page pisg has written since 2001'),
    ('pisg',        'The project\u2019s own blue'),
    ('darkgalaxy',  'Dark blue, the first dark theme pisg shipped'),
    ('darkred',     'Dark with a red accent'),
    ('justgrey',    'Grey on grey, nothing shouting'),
    ('ocean',       'Cool blues'),
    ('orange_grey', 'Grey with an orange accent'),
    ('softgreen',   'Pale green, easy on the eyes'),
]

NAMED = {'black': '#000000', 'white': '#ffffff', 'red': '#ff0000', 'blue': '#0000ff',
         'green': '#008000', 'grey': '#808080', 'gray': '#808080', 'silver': '#c0c0c0',
         'navy': '#000080', 'yellow': '#ffff00', 'orange': '#ffa500'}


def norm(v):
    """'#ABC', '#AABBCC' or a colour name -> '#aabbcc'."""
    if not v:
        return None
    v = v.strip().lower()
    if v in NAMED:
        return NAMED[v]
    if not v.startswith('#'):
        return None
    v = v[1:]
    if len(v) == 3:
        v = v[0] * 2 + v[1] * 2 + v[2] * 2
    return '#' + v if re.match(r'^[0-9a-f]{6}$', v) else None


def rule(css, selectors, prop):
    """The value of one property inside the first matching rule, or None.

    The classic files are hand-written: some use uppercase selectors and properties,
    some put the brace on its own line, some group selectors. `css` is expected to be
    lowercased already; `selectors` may be one selector or a list to try in order.
    """
    if isinstance(selectors, str):
        selectors = [selectors]
    # "color" must not match inside "background-color"
    prop_re = r'(?<![-a-z])' + re.escape(prop) + r'\s*:\s*([^;}]+)'
    for sel in selectors:
        for m in re.finditer(r'(?:^|[}\n])\s*' + re.escape(sel) + r'\s*(?:,[^{]*)?\{([^}]*)\}',
                             css, re.S):
            m2 = re.search(prop_re, m.group(1))
            if m2:
                v = norm(m2.group(1))
                if v:
                    return v
    return None


def mix(a, b, t):
    """Blend two hex colours; t=0 gives a, t=1 gives b."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join('%02x' % round(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))


def lum(h):
    c = [int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def hsl(h):
    r, g, b = [int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    mx, mn = max(r, g, b), min(r, g, b)
    l, d = (mx + mn) / 2, mx - mn
    if not d:
        return 0.0, 0.0, l
    sat = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hue = ((g - b) / d) % 6
    elif mx == g:
        hue = (b - r) / d + 2
    else:
        hue = (r - g) / d + 4
    return hue * 60, sat, l


def from_hsl(hue, sat, l):
    hue = (hue % 360 + 360) % 360
    c = (1 - abs(2 * l - 1)) * sat
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = l - c / 2
    t = ([c, x, 0] if hue < 60 else [x, c, 0] if hue < 120 else [0, c, x] if hue < 180
         else [0, x, c] if hue < 240 else [x, 0, c] if hue < 300 else [c, 0, x])
    return '#' + ''.join('%02x' % round((v + m) * 255) for v in t)


def contrast(a, b):
    l1, l2 = lum(a), lum(b)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def readable(colour, background, target=4.0, lighter=None):
    """Keep the hue, move the lightness until the colour reads on this background.

    The classic dark themes were written for a page where links sat on a light
    highlight cell; on the 1.0a layout the same colour sits on the section itself,
    so a few of them need lifting. The hue is what carries the theme's identity,
    so only the lightness changes.
    """
    if contrast(colour, background) >= target:
        return colour
    hue, sat, l = hsl(colour)
    up = lum(background) < 0.4 if lighter is None else lighter
    best, step = colour, 0.02
    for _ in range(50):
        l = min(0.97, l + step) if up else max(0.05, l - step)
        cand = from_hsl(hue, max(sat, 0.35) if sat else 0, l)
        if contrast(cand, background) >= target:
            return cand
        best = cand
    return best


def bar_colours(css):
    """The four time-of-day colours, read out of the theme's own bar sprite.

    Each classic file draws the bars with one PNG containing a 4-colour palette,
    offset by 15px per colour. Decode the PLTE chunk and read the pixels the four
    offsets land on, so the converted palette keeps the theme's real bar colours.
    """
    m = re.search(r'#green-h\s*\{[^}]*base64,([A-Za-z0-9+/=]+)', css, re.S)
    if not m:
        return None
    raw = base64.b64decode(m.group(1))

    plte, ihdr, idat = None, None, b''
    pos = 8
    while pos < len(raw):
        ln = struct.unpack('>I', raw[pos:pos + 4])[0]
        typ = raw[pos + 4:pos + 8]
        data = raw[pos + 8:pos + 8 + ln]
        if typ == b'IHDR':
            ihdr = struct.unpack('>IIBBBBB', data)
        elif typ == b'PLTE':
            plte = data
        elif typ == b'IDAT':
            idat += data
        pos += 12 + ln
    if not (plte and ihdr):
        return None

    width, height, depth, ctype = ihdr[0], ihdr[1], ihdr[2], ihdr[3]
    if ctype != 3:                      # not palette-based: give up
        return None

    # un-filter the scanlines (these sprites are 1px wide or 1px tall, filter 0)
    rows, data = [], zlib.decompress(idat)
    stride = (width * depth + 7) // 8
    prev = bytearray(stride)
    p = 0
    for _ in range(height):
        f = data[p]; p += 1
        line = bytearray(data[p:p + stride]); p += stride
        if f == 2:                      # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        rows.append(line)
        prev = line

    def pixel(x, y):
        line = rows[y]
        if depth == 8:
            idx = line[x]
        else:                           # 1, 2 or 4 bits per pixel
            per = 8 // depth
            byte = line[x // per]
            shift = 8 - depth * (x % per + 1)
            idx = (byte >> shift) & ((1 << depth) - 1)
        return '#%02x%02x%02x' % (plte[idx * 3], plte[idx * 3 + 1], plte[idx * 3 + 2])

    # the sprite is a vertical strip: green, red, yellow, blue at 15px intervals
    if height >= 60:
        g, r, y, b = (pixel(0, 7), pixel(0, 22), pixel(0, 37), pixel(0, 52))
    elif width >= 60:
        g, r, y, b = (pixel(7, 0), pixel(22, 0), pixel(37, 0), pixel(52, 0))
    else:
        return None
    return {'green': g, 'red': r, 'yellow': y, 'blue': b}


def convert(nameticket):
    name, blurb = nameticket
    raw = io.open(os.path.join(SRC, name + '.css'), encoding='utf-8', errors='replace').read()
    css = raw.lower()          # selectors and properties are written both ways

    bg = (rule(css, 'body', 'background-color') or rule(css, 'body', 'background')
          or '#ffffff')
    fg = rule(css, ['body', 'td'], 'color') or '#000000'
    link = rule(css, ['a:link', 'a'], 'color') or fg
    headbg = rule(css, '.headtext', 'background-color')
    hicell = rule(css, '.hicell', 'background-color')
    tdtop = rule(css, '.tdtop', 'background-color')
    rankc = rule(css, '.rankc', 'background-color')
    headfg = rule(css, '.headtext', 'color')
    headfg = rule(css, '.headtext', 'color')
    male = rule(css, '.male', 'color') or link
    female = rule(css, '.female', 'color') or link

    dark = lum(bg) < 0.4
    mode = 'dark' if dark else 'light'

    # A section sits on --card. The old .hicell is the right colour when it was a
    # surface (close to the page background); when it was a bright highlight cell
    # instead, derive a surface from the background.
    if hicell and contrast(hicell, bg) < 2.2:
        card = hicell
    else:
        card = mix(bg, '#ffffff', 0.55) if not dark else mix(bg, '#ffffff', 0.07)
    row = card

    row_alt = rankc if (rankc and 1.02 < contrast(rankc, card) < 2.2) else \
        (mix(card, '#000000', 0.06) if not dark else mix(card, '#ffffff', 0.09))
    line = tdtop if (tdtop and 1.05 < contrast(tdtop, card) < 3.2) else mix(card, fg, 0.22)

    # Quiet text must stay quieter than the body text, so it moves away from --fg
    # rather than always towards the lighter end (justgrey sits mid-grey, where
    # "lighter" would land on the same white as the text).
    muted = readable(mix(fg, card, 0.45), card, 3.4, lighter=lum(fg) < lum(card))

    # --head is heading *text* in 1.0a. The old headline bar carried the scheme's
    # character (default's purple, orange_grey's orange, darkred's red), so when that
    # bar had a colour of its own, use it — lifted until it reads on the section.
    if headbg and hsl(headbg)[1] >= 0.15:
        head = readable(headbg, card, 3.4)
    elif headfg and contrast(headfg, card) >= 3:
        head = headfg
    else:
        head = fg
    # keep the link's hue — that is the theme's signature — and lift it until it reads
    accent = readable(link, card, 4.0)
    male_c = readable(male, card, 3.5)
    female_c = readable(female, card, 3.5)

    bars = bar_colours(raw) or {'blue': '#3366ff', 'green': '#66cc33',
                                'yellow': '#cccc33', 'red': '#cc3333'}

    return name, blurb, {
        'mode': mode, 'bg': bg, 'card': card, 'row': row, 'row-alt': row_alt, 'line': line,
        'fg': fg, 'muted': muted, 'head': head, 'accent': accent,
        'blue': bars['blue'], 'green': bars['green'], 'yellow': bars['yellow'],
        'red': bars['red'], 'male': male_c, 'female': female_c,
    }


ORDER = ['mode', 'bg', 'card', 'row', 'row-alt', 'line', 'fg', 'muted', 'head', 'accent',
         'blue', 'green', 'yellow', 'red', 'male', 'female']


def js_block():
    out = ['  /* The eight classic schemes, converted from their own CSS by',
           '     tools/make-classic-palettes.py — including the four bar colours,',
           '     decoded out of each theme\'s own sprite. Do not edit by hand. */',
           '  var CLASSIC = [']
    for spec in CLASSICS:
        name, blurb, pal = convert(spec)
        pairs = []
        for k in ORDER:
            key = "'" + k + "'" if '-' in k else k
            pairs.append('%s: %r' % (key, pal[k]))
        body = ', '.join(pairs).replace("'", '"').replace('"row-alt"', "'row-alt'")
        body = body.replace('"', "'")
        out.append("    ['%s', '%s', {" % (name, blurb))
        # wrap the pairs at a sensible width
        line = '      '
        for i, p in enumerate(pairs):
            p = p.replace('"', "'")
            if len(line) + len(p) > 96:
                out.append(line.rstrip())
                line = '      '
            line += p + (', ' if i < len(pairs) - 1 else '')
        out.append(line.rstrip())
        out.append('    }],')
    out.append('  ];')
    return '\n'.join(out)


if __name__ == '__main__':
    block = js_block()
    if '--write' in sys.argv:
        js = io.open(OUT, encoding='utf-8').read()
        start = js.index('  /* The eight classic schemes')
        end = js.index('  ];', start) + len('  ];')
        js = js[:start] + block + js[end:]
        io.open(OUT, 'w', encoding='utf-8', newline='\n').write(js)
        print('wrote the palette block into', OUT)
    else:
        print(block)
