# pisg.github.io

The website for **pisg**, the Perl IRC Statistics Generator — live at <https://pisg.github.io/>.
The program itself is at <https://github.com/PISG/pisg>.

Static HTML, one stylesheet, two small scripts. No build step, no dependencies, no framework, and
**no external requests at all**: system fonts, inline SVG icons, and the bar graphics inside the
example pages as inline data URIs. Nothing is stored in the visitor's browser either — no cookies,
no `localStorage`.

---
## What's in here

| URL | File | What it is |
| --- | --- | --- |
| `/` | `index.html` | Landing page: what pisg is, quick start, what's new in 1.0, themes, log formats, optional tools, FAQ, credits |
| `/docs/` | `docs/index.html` | The manual: setup guide, all 108 options, the optional tools and a complete example `pisg.cfg` |
| `/themes/` | `themes/index.html` | Every colour scheme, how to write one by hand, and the theme creator. Full-width, with the twelve themes in the sidebar |
| `/changelog/` | `changelog/index.html` | Release notes, newest first. 1.0a in full, then 0.80-preview2, 0.80-preview, 0.73 |
| `/privacy/` | `privacy/index.html` | Privacy policy — and the checklist for people who publish statistics about real channels |
| `/cookies/` | `cookies/index.html` | Cookie policy: there are none, and why that means no consent banner |
| `/terms/` | `terms/index.html` | Terms of use: licence, no warranty, liability, what the publisher is responsible for, governing law |
| &mdash; | `404.html` | Styled not-found page that also forwards old option anchors to `/docs/` |
| &mdash; | `assets/site.css` | The whole design system, one file, design tokens at the top |
| &mdash; | `assets/site.js` | Mobile menu, copy buttons, docs filter and scroll-spy. No dependencies |
| &mdash; | `assets/theme-maker.js` | The theme creator: palette, live preview, generated CSS |
| `/demo/` | `demo/index.html` | The landing page pisg ships as `site/index.html`, reading `demo/channels.json` |
| `/demo/nightshift.html` | | Example stats page — a very busy channel, every 1.0a section |
| `/demo/basement.html` | | Example stats page — a quiet channel, with user pictures on |
| `/demo/themes/…` | | The short sample page in each colour scheme, for the theme gallery |
| &mdash; | `tools/*.py` | The scripts that generate `docs/`, the classic palettes and everything in `demo/` |
| &mdash; | `.nojekyll` | Tells GitHub Pages to serve the files as they are, with no Jekyll pass |

## The theme creator

`/themes/` builds a pisg colour scheme in the browser. It fetches the `modern` stylesheet out of
`demo/nightshift.html`, swaps the sixteen palette variables for the ones you pick, injects the result
into the preview frame and offers the finished file as a download.

The preview is **the full busy-channel example**, not the six-nick sample: all nineteen sections, the
relation map, the section menu, the tables with user pictures. That is the point of the page — you
are judging a theme against everything pisg can put on a page. Taking the template from the same file
also means the downloaded CSS carries the rules for the sections 1.0a added, which the older sample
pages in `demo/themes/` do not have.

**The whole editor lives in the sidebar** — the twelve themes (four modern, eight classics), the
file name, light/dark, the sixteen colours and the readability read-out. The main column holds only
the preview, the generated file and the reference sections, and it is unconstrained
(`body.themes-page` widens the sidebar to 328 px; `.main.wide` drops the 900 px cap that the other
sidebar page, `/docs/`, keeps). The preview frame is `100vh` minus the chrome, so the example stats
page is as large as the window allows. This is the only page on the site that is wider than 1080 px.

The interface deliberately has **no native form controls**: presets are cards with their own swatch
strips, light/dark and the preview width are segmented switches, and the file name is a text field
between a fixed `layout/` and `.css`. Browser dropdowns cannot be styled to match a dark site, so
there are none. (`assets/site.css` does carry a proper `select` style with its own arrow, for the day
one is unavoidable.)

It also reports readability: four WCAG contrast ratios, plus the hue gap between the two closest
time-of-day colours. A contrast ratio is the wrong test there — blue and red can be obviously
different and still score 1.1:1 — so that line measures hue separation instead, in degrees.

Nothing is uploaded and nothing is stored: the palette lives in the URL hash, so a theme can be
bookmarked or sent to somebody. That keeps the promise the cookie policy makes.

### The eight classics, converted

`tools/make-classic-palettes.py` reads the old hand-written stylesheets out of the pisg distribution
(`layout/default.css`, `ocean.css`, …) and turns each one into a 1.0a palette:

- `body`, `.hicell`, `.tdtop`, `.rankc` and `.headtext` become the surfaces, rules and heading colour;
- each theme's **own bar colours** are decoded out of the four-colour PNG sprite embedded in its CSS
  (they all turn out to share `#3366ff` / `#66cc33` / `#cccc33` / `#cc3333` — the classic bars);
- a colour that would not have read on the new layout keeps its hue and is moved in lightness until
  it does, because the hue is what makes a theme recognisable.

It writes the `CLASSIC` block inside `assets/theme-maker.js`:

```sh
python3 tools/make-classic-palettes.py           # print it
python3 tools/make-classic-palettes.py --write   # replace the block in theme-maker.js
```

Edit `SRC` at the top if the pisg checkout is somewhere else. Do not edit the block by hand — it is
regenerated.

If `build-themes.py` in the pisg repository ever changes the palette variables, update `FIELDS` and
`MODERN` at the top of `assets/theme-maker.js` to match.

## URLs have no `.html`

Every page is a directory with an `index.html`, so the addresses are `/docs/`, `/changelog/`,
`/privacy/`, `/cookies/` and `/terms/`. GitHub Pages serves those directly — no configuration, no
redirects, no build step. Links between pages are **relative** (`../docs/`, `../assets/site.css`), so
the site also works when it is served from a subfolder or opened from disk.

Old links keep working:

- `/docs.html` and friends land on `404.html`, which explains where things moved.
- Until this rebuild the whole manual lived on the home page, so links like
  `pisg.github.io/#ShowRandQuote` are out there. `index.html` checks on load: if the hash matches
  nothing on the home page, it forwards to `/docs/#<hash>`. `404.html` does the same.

Seven pages, one stylesheet, two scripts, no build step, no dependencies and **no external requests at
all** — system fonts, inline SVG icons, and the bar graphics inside the demo pages as inline data
URIs. That is checked, not assumed: no `<img>`, `<script>`, `<link>` or `<iframe>` on any page points
off-site, and nothing touches `localStorage`, `sessionStorage`, IndexedDB or `document.cookie`.

## The example pages are invented

`demo/` is built from real pisg 1.0a output, then everything that identifies a person is replaced:
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

## Cache: stamp the assets before pushing

GitHub Pages serves `assets/*` with `Cache-Control: max-age=600`. Push a change and a visitor who
loaded the site within the last ten minutes gets **new HTML with the CSS and JavaScript they already
had** — which, when the layout has changed, looks broken rather than merely stale. That happened once
on `/new/themes/`: the new sidebar markup with the previous stylesheet.

`tools/version-assets.py` prevents it. Every `<link>` and `<script>` carries `?v=<hash of the
assets>`, so an asset change is a new URL and the two can never come apart. The hash moves only when
something in `assets/` moves.

```sh
python3 tools/make-docs.py         # if the documentation changed
python3 tools/version-assets.py    # always, last, before committing
```

It also rewrites the template inside `tools/make-docs.py`, so run it **after** the generators, never
before.

## Looking at it locally

```sh
python -m http.server 8000     # from the repository root, then open http://localhost:8000
```

Opening `index.html` straight from disk works for everything **except** `demo/index.html`: that page
`fetch()`es `channels.json`, and browsers refuse `fetch` on `file://`. That is a browser rule, not a
bug in the page — on a web server, including GitHub Pages, it works.

## Where the documentation comes from

`docs/index.html` is **generated from the manual pisg ships** — `docs/pisg-doc.html`, which
`docs/xml2html.py` builds from `docs/pisg-doc.xml`. `tools/make-docs.py` reads that file, turns each
`<section class="option">` into a card, and adds the two chapters the shipped manual does not have
yet: the options added in 1.0aa and the optional tools. It also brings across the complete example
`pisg.cfg` with its copy and download buttons, and updates three passages that had aged (the colour
scheme list, the stylesheet advice, and the SourceForge mailing-list pointer).

That means the website and the distribution cannot drift: when `pisg-doc.xml` changes, regenerate
`pisg-doc.html`, point `SRC` at it and re-run `tools/make-docs.py`. The thirteen 1.0a options are still
written out by hand inside that script — move them into `pisg-doc.xml` and they will come across on
their own.

The page's shell — full-height sidebar, filter box with a match count, scroll-spy, back-to-top — follows
the BlackTools documentation page, in this site's own colours.

## Editing

Colours, fonts, radii and spacing are CSS custom properties at the top of `assets/site.css`. The
accent is a green (`--accent`, `--accent-fill`) picked to sit next to the old site's green without
copying it; change those two and the whole site follows.

The docs page is generated — edit `tools/make-docs.py` (or the manual it reads), not
`docs/index.html`. Its sidebar, option index pills and filter are all built from the chapter and
option ids, so a new option needs nothing else.

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

- **The 1.0a release date.** The site says *September 2026* (`index.html` hero, `changelog/`).
- **The `canada` theme was dropped from the site.** `CHANGELOG-1.0.md` in the pisg repository still
  lists it as one of five modern themes, and `build-themes.py` presumably still builds it — remove it
  there too, or the release notes and the website will disagree. The site now says *four* modern
  themes and twelve in total.
- **The theme sample pages** in `demo/themes/` were generated by 0.80-preview2, so they show the
  older set of sections. The footer version string is rewritten to `v1.0a` by `tools/make-themes.py`,
  but regenerating them with 1.0a itself would make the gallery show the new sections too — and would
  make the theme creator's preview a full 1.0a page.
- **The 1.0 options belong in `docs/pisg-doc.xml`**, so the shipped manual and this site describe the
  same thing. Until then they live in `tools/make-docs.py`.
- **The shipped manual still calls itself “pisg 0.73 documentation”.** Worth retitling when
  `pisg-doc.xml` is next built.
- **Governing law and a contact address** in `terms/` and `privacy/` (see above).
- The optional tools' command-line examples in `docs.html` (`pisg-autoalias.py`, `adiirc2eggdrop.py`,
  `znc-setup.sh`) were written from the changelog. Check the real flag names before publishing.

## Publishing

GitHub Pages serves the default branch from the repository root, so a push is a deploy. Before
committing anything that touched `assets/`, run the version stamp (see above) — it is the one step
that is easy to forget and impossible to notice until somebody's browser shows the old stylesheet
with the new markup.

The site was built in a `new/` folder first and replaced the 2016 GitHub Pages template in place.
Links to the old layout keep working: `404.html` forwards `/new/anything` to `/anything`, and the
home page forwards `pisg.github.io/#SomeOption` — the shape of link that existed when the whole
manual lived on one page — to `/docs/#SomeOption`.


## Credits

pisg was written in 2001 by Morten “mbrix” Brix Pedersen —
<https://sourceforge.net/projects/pisg/> — and is GPL-2.0-or-later. This site is about that program
and carries the same licence.
