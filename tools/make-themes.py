# -*- coding: utf-8 -*-
"""
Theme previews: the short sample page pisg ships for each colour scheme, with the
people in it invented.  Third channel name (#teatime) so it is not confused with
the two example channels.
"""
import io, re, os

SRCDIR = r'C:\Users\admin\Desktop\output\themes'
SITE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DSTDIR = os.path.join(SITE, 'demo', 'themes')
THEMES = ['modern', 'midnight', 'amoled', 'terminal', 'default']

MAP = {
    'Seb': 'vox', 'humility': 'humbug', 'Isa': 'Iris', 'Clairvoyant': 'Fortuna',
    'kaustic': 'kelpie', 'RomanticGuy': 'PoeticGuy', 'BigMan44': 'BigMug44',
    'zestyantlion': 'zestyanteater', 'OhCanada': 'Ledger', 'Agent': 'Ledger',
    'RangerBobVa': 'RamblerBobVa',
}

QUOTES = [
    'the kettle is on, as always',
    'Ahoy! \\o',
    'vox: I was a poor student when I bought this chair',
    'vox: go to bed, the logs will still be here',
    'I was testing some sh*t on my mIRC ;p',
    'Hi',
]

TEXT = [
    ('* humility smax Agent', '* humbug smax Ledger'),
    ('Isabelle', 'kettle'),
    # the shipped samples were generated before 1.0
    ('</a> v0.80-preview2', '</a> v1.0a'),
]

NICKCH = r'A-Za-z0-9_\[\]\\|`\^\-'

if not os.path.isdir(DSTDIR):
    os.makedirs(DSTDIR)

for theme in THEMES:
    h = io.open(os.path.join(SRCDIR, theme + '.html'), encoding='utf-8', errors='replace').read()

    qi = [0]
    def _q(match):
        i = qi[0]; qi[0] += 1
        return match.group(1) + (QUOTES[i] if i < len(QUOTES) else QUOTES[-1]) + match.group(2)
    h = re.sub(r'(>")(?:[^"<]*)("</td>)', _q, h)

    for old, new in TEXT:
        h = h.replace(old, new)

    for old in sorted(MAP, key=len, reverse=True):
        new = MAP[old]
        h = re.sub(r'(?<![%s])%s(?![%s])' % (NICKCH, re.escape(old), NICKCH),
                   new.replace('\\', '\\\\'), h)

    h = h.replace('#canada', '#teatime').replace('#Canada', '#teatime')

    # a line saying what the page is, and a way back
    h = h.replace(
      '<p class="subtitle">',
      '<p class="subtitle"><a href="../../themes/">&larr; all themes</a> &middot; '
      'colour scheme <b>%s</b> &middot; sample page, invented people</p>\n<p class="subtitle">' % theme,
      1)

    out = os.path.join(DSTDIR, theme + '.html')
    io.open(out, 'w', encoding='utf-8', newline='\n').write(h)
    left = [o for o in MAP if o != MAP[o]
            and re.search(r'(?<![%s])%s(?![%s])' % (NICKCH, re.escape(o), NICKCH), h)]
    print('%-10s %6d bytes  leftover: %s' % (theme, len(h), left or 'none'))
