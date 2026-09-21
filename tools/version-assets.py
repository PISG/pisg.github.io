# -*- coding: utf-8 -*-
"""
Stamp the stylesheet and script links with a version, so a browser can never pair
new HTML with an old asset.

GitHub Pages serves assets with `Cache-Control: max-age=600`. Push a change and a
visitor who loaded the site in the last ten minutes gets the new HTML with the CSS
and JavaScript they already had — which, when the layout has changed, looks broken.
Adding ?v=<hash of the assets> makes every asset change a new URL, so that cannot
happen; the hash only moves when the assets themselves move.

Run it after touching anything in assets/ (and after tools/make-docs.py, which
writes docs/index.html):

    python3 tools/version-assets.py
"""
import hashlib, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
ASSETS = ['assets/site.css', 'assets/site.js', 'assets/theme-maker.js']


def stamp():
    h = hashlib.sha1()
    for name in ASSETS:
        path = os.path.join(SITE, name)
        if os.path.exists(path):
            h.update(io.open(path, 'rb').read())
    return h.hexdigest()[:8]


def main():
    v = stamp()
    pattern = re.compile(r'((?:href|src)="[^"]*assets/(?:site\.css|site\.js|theme-maker\.js))(\?v=[0-9a-f]+)?(")')
    touched = 0

    targets = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in ('tools', 'demo')]
        for f in files:
            if f.endswith('.html'):
                targets.append(os.path.join(root, f))
    targets.append(os.path.join(HERE, 'make-docs.py'))   # keep the generator in step

    for path in targets:
        if not os.path.exists(path):
            continue
        s = io.open(path, encoding='utf-8').read()
        new = pattern.sub(lambda m: m.group(1) + '?v=' + v + m.group(3), s)
        if new != s:
            io.open(path, 'w', encoding='utf-8', newline='\n').write(new)
            touched += 1

    print('asset version %s, %d file(s) updated' % (v, touched))


if __name__ == '__main__':
    main()
