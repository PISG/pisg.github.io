# Changelog — pisg.github.io

Changes to the website, newest first. Changes to pisg itself are in
[`CHANGELOG.md`](https://github.com/PISG/pisg/blob/master/CHANGELOG.md) in the pisg repository
and on the site at [/changelog/](https://pisg.github.io/changelog/).

---

## 2026-09-21 — ready for the 1.0a release

### Changed

- `/docs/` is now built from the manual in the pisg repository (`../pisg/docs/pisg-doc.html`)
  instead of an old copy. The eleven options added in 1.0a come from the manual too, each marked
  *1.0a* in its own chapter; "Options added in 1.0a" is now a short list of links to them.
- The optional tools chapter matches the scripts that ship: the real arguments of
  `pisg-autoalias.py`, `adiirc2eggdrop.py` and `znc-setup.sh`, and `!pisgstats` is a
  channel command.
- The IRC channel is written `#pisg` everywhere (it was `#PISG` in places), on Undernet.
- The manual's shell prompt no longer says `pisg-0.37`.
- The theme samples in `/demo/themes/` are now made by pisg 1.0a itself, from an invented
  channel (`#teatime`, forty made-up regulars over two months), so they show every section 1.0a
  writes. They used to be short 0.80-preview2 pages. `tools/make-themes.py` generates them.
- Privacy and terms name the maintainer, Seb, as the person in charge of personal information
  (Quebec's Law 25) and give a private contact route: <https://dooubletap.github.io/>. Governing
  law stays Quebec.

### Removed

- `ShareStats`, `ShareLink` and `ShareWebhook` from the docs, the changelog, the FAQ and the
  privacy page. pisg has no such options: it opens no network connection at all, and the pages
  now say so.

### Fixed

- The docs page links for the options added in 1.0a (`#ShowOverview`, `#HomeLink`, …) point at
  the manual's own entries, so there is one description of each option, not two.

## 2026-09-20 — the new site

The 2016 GitHub Pages template was replaced by a site built for pisg 1.0a.

### Added

- **Home page**: what pisg is, what the page looks like, the 1.0a highlights, how to install it,
  where to host the pages, FAQ, and credit to Morten "mbrix" Brix Pedersen, who started pisg in
  2001 ([original project](https://sourceforge.net/projects/pisg/)).
- **`/docs/`**: the whole manual on one page, with a sidebar, an option filter (<kbd>/</kbd>),
  an index of every option, the optional tools, and the complete example `pisg.cfg` with copy
  and download buttons.
- **`/changelog/`**: the 1.0a release notes and upgrade steps, and the history back to 2001.
- **`/demo/`**: two complete example stats pages (`#nightshift`, a busy channel, and
  `#basement`, a small one) and the landing page that compares them. They are made from real
  pisg output with every nick, quote, topic and URL replaced.
- **`/themes/`**: the twelve colour schemes side by side — four modern ones and the eight
  classic ones converted to 1.0a palettes — and a theme creator that builds a stylesheet from a
  palette and previews it on a full stats page, on the widest layout the site has.
- **Privacy, cookies and terms** pages (`/privacy/`, `/cookies/`, `/terms/`): the site sets no
  cookies, runs no analytics, loads nothing from other sites and stores nothing in the browser.
- **`404.html`** that explains where things moved.

### Changed

- Clean addresses: `/docs/`, `/themes/`, `/changelog/`, … instead of `.html` files.
- Old links keep working: `/new/anything` forwards to `/anything`, and `/#SomeOption` — from the
  days when the manual was the home page — forwards to `/docs/#SomeOption`.
- Every stylesheet and script link carries `?v=<hash>` (`tools/version-assets.py`), so a visitor
  never gets new pages with an old stylesheet.

### Removed

- The `canada` colour scheme, from the site and from pisg: it was never released.

## 2016-02-21

- First GitHub Pages site: the manual and the changelog, moved from SourceForge.
