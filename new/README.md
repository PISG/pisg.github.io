# pisg.github.io — rebuild (draft)

This folder is the proposed new **pisg.github.io**. Nothing here is live yet: it sits in `new/`
so it can be read, argued with and fixed before it replaces the files at the repository root.

Live site (current): <https://pisg.github.io/> · Source of pisg: <https://github.com/PISG/pisg>

---

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | Landing page: what pisg is, quick start, what's new in 1.0, themes, log formats, optional tools, FAQ, credits |
| `docs.html` | The manual: setup guide + every option, with the 1.0 options added and the old SourceForge pointers updated |
| `changelog.html` | Release notes, newest first. 1.0 in full, then 0.80-preview2, 0.80-preview, 0.73 |
| `privacy.html` | Privacy policy — and the checklist for people who publish statistics about real channels |
| `cookies.html` | Cookie policy: there are none, and why that means no consent banner |
| `terms.html` | Terms of use: licence, no warranty, liability, what the publisher is responsible for, governing law |
| `assets/site.css` | The whole design system, one file, design tokens at the top |
| `assets/site.js` | Mobile menu, copy buttons, docs table-of-contents highlighting. No dependencies |
| `demo/index.html` | The landing page pisg ships as `site/index.html`, reading `demo/channels.json` |
| `demo/nightshift.html` | Example stats page — a very busy channel, every 1.0 section |
| `demo/basement.html` | Example stats page — a quiet channel, with user pictures on |
| `demo/themes/*.html` | The short sample page in each colour scheme, for the theme gallery |
| `tools/*.py` | The scripts that generated `docs.html` and everything in `demo/` (not part of the published site) |

Six pages, one stylesheet, one script, no build step, no dependencies and **no external requests at
all** — system fonts, inline SVG icons, and the bar graphics inside the demo pages as inline data
URIs. That is checked, not assumed: no `<img>`, `<script>`, `<link>` or `<iframe>` on any page points
off-site, and nothing touches `localStorage`, `sessionStorage`, IndexedDB or `document.cookie`.

## The example pages are invented

`demo/` is built from real pisg 1.0 output, then everything that identifies a person is replaced:
nicks, quotes, example lines, topics, most-used words, URLs, user pictures and the channel names.
The numbers, the graphs, the relation map and the markup are untouched, so the pages behave like
real ones at real scale.

The two channels are `#nightshift` (133,944 lines, 915 nicks, 50 days) and `#basement` (6,524 lines,
285 nicks, 176 days); the theme samples use a third name, `#teatime`, so nothing gets mixed up.
`BeanCounter` and `okra` appear in both channels on purpose — the same people turn up in more than
one room.

The scripts that produced them are in `tools/`:

| Script | Makes |
| --- | --- |
| `tools/make-nightshift.py` | `demo/nightshift.html` from a real busy-channel page |
| `tools/make-basement.py` | `demo/basement.html` from a real small-channel page |
| `tools/make-themes.py` | `demo/themes/*.html` from the shipped theme samples |
| `tools/make-docs.py` | `docs.html` from the old site's documentation body plus the 1.0 additions |

They read their input from paths outside this repository — edit the `SRC` constant at the top of each
one before re-running. Each prints an audit at the end: if it does not say
`leftover source nicks: none`, a real nick made it through and the map at the top of that script needs
another entry.

## Looking at it locally

```sh
cd new
python -m http.server 8000     # then open http://localhost:8000
```

Opening `index.html` straight from disk works for everything **except** `demo/index.html`: that page
`fetch()`es `channels.json`, and browsers refuse `fetch` on `file://`. That is a browser rule, not a
bug in the page — on a web server, including GitHub Pages, it works.

## Editing

Colours, fonts, radii and spacing are CSS custom properties at the top of `assets/site.css`. The
accent is a green (`--accent`, `--accent-fill`) picked to sit next to the old site's green without
copying it; change those two and the whole site follows.

The docs page is one long document with an `id` on every heading and every option, and a sidebar
built to match. If you add an option, add a `<div class="opt" id="OptionName">` block **and** a
sidebar entry — nothing generates the sidebar at run time.

## Legal pages

`privacy.html`, `cookies.html` and `terms.html` are written for what this site actually is: static
pages on GitHub Pages that set no cookies, run no analytics and collect nothing. That is the easiest
compliance position there is, and the pages say so plainly rather than hedging. They cover:

- **PIPEDA** and **Quebec Law 25** (Canada), **GDPR**/**ePrivacy** (EEA), **UK GDPR**/**PECR**, and the
  US state privacy laws — all of which turn on collecting, storing or tracking. None of that happens
  here, so there is no banner and no consent flow. If analytics, a comment system or a custom font CDN
  is ever added, all three pages need updating **before** it ships.
- **GitHub as the host**: named as the party that sees IP addresses, with links to its privacy
  statement and its international-transfer terms.
- **The person publishing statistics**: a plain checklist of what running pisg on a real channel means
  under those same laws — tell people, honour `ignore="y"`, think about quotes and retention. That
  belongs on this site because pisg is the tool that creates the risk.
- **Terms**: GPL first and these terms second, no warranty, a liability cap that explicitly does not
  override non-waivable consumer rights, takedown route, and Quebec/Canada as governing law.

Two things to confirm before publishing: the **governing-law clause** (Quebec is assumed — change it
if the maintainer is elsewhere), and the **contact route** (currently GitHub issues only; a mailbox
would be better for a privacy request). These pages were written carefully and in good faith, but
they are not legal advice — if the project wants certainty, have a lawyer read them once.

## Still to decide

- **The 1.0 release date.** The site says *September 2026* in three places (`index.html` hero,
  `changelog.html`). Correct it before this goes live.
- **The theme sample pages** in `demo/themes/` were generated by 0.80-preview2, so they show the
  older set of sections and say `v0.80-preview2` in the footer. Regenerating them with 1.0 would make
  the gallery show the new sections too.
- **`docs.html` ships in the distribution as `docs/pisg-doc.html`.** The two should not drift. Either
  this page is generated from `docs/pisg-doc.xml` like that one is, or one of them links to the other.
- **Governing law and a contact address** in `terms.html` and `privacy.html` (see above).
- The optional tools' command-line examples in `docs.html` (`pisg-autoalias.py`, `adiirc2eggdrop.py`,
  `znc-setup.sh`) were written from the changelog. Check the real flag names before publishing.

## Going live

Replace the root of the repository with the contents of this folder:

```sh
git rm -r index.html params.json stylesheets      # the 2016 GitHub Pages template
git mv new/index.html new/docs.html new/changelog.html        new/privacy.html new/cookies.html new/terms.html new/assets new/demo .
git rm -r new                                     # tools/ and this README stay behind
```

Keep `README.md` at the root (the repository's own, not this one), and add a `CNAME` if the site ever
moves off `pisg.github.io`.

## Credits

pisg was written in 2001 by Morten “mbrix” Brix Pedersen —
<https://sourceforge.net/projects/pisg/> — and is GPL-2.0-or-later. This site is about that program
and carries the same licence.
