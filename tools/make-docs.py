# -*- coding: utf-8 -*-
"""
Build docs/index.html out of the manual pisg ships (docs/pisg-doc.html, generated
from docs/pisg-doc.xml), plus a chapter that manual does not have: the optional tools.

Input  : ../pisg/docs/pisg-doc.html — the pisg repository checked out next to this one.
         Rebuild it there first (python3 docs/xml2html.py docs/pisg-doc.xml docs/pisg-doc.html).
Output : docs/index.html
"""
import io, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)                                    # the repository root
SRC  = os.path.join(os.path.dirname(SITE), 'pisg', 'docs', 'pisg-doc.html')
OUT  = os.path.join(SITE, 'docs', 'index.html')

doc = io.open(SRC, encoding='utf-8').read()

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def chapter(cid):
    """Inner HTML of one <section class="chapter" id="cid">, without its <h2>.

    Chapters contain nested <section> elements, so the end is found by looking for the
    next chapter (or the end of <main>), not for the next </section>.
    """
    m = re.search(r'<section class="chapter" id="%s">\s*<h2>[^<]*</h2>' % re.escape(cid), doc)
    if not m:
        raise SystemExit('chapter %s not found' % cid)
    rest = doc[m.end():]
    nxt = re.search(r'\n</section>\s*(?=<section class="chapter"|</main>)', rest)
    if not nxt:
        raise SystemExit('end of chapter %s not found' % cid)
    return rest[:nxt.start()]

def tidy(html):
    """The generated manual wraps lists and pre blocks inside <p>; unwrap them."""
    html = re.sub(r'<p>\s*<ul>', '<ul>', html)
    html = re.sub(r'</ul>\s*</p>', '</ul>', html)
    html = re.sub(r'<p>\s*<ol>', '<ol>', html)
    html = re.sub(r'</ol>\s*</p>', '</ol>', html)
    html = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'<li>\1</li>', html, flags=re.S)
    html = re.sub(r'<p>([^<]*?)\s*<pre>', r'<p>\1</p>\n<pre>', html)
    html = re.sub(r'</pre>\s*</p>', '</pre>', html)
    return html

# options added in 1.0a: they are in the manual's own chapters and get a badge there
NEW_1_0A = ['ShowOverview', 'ShowRelations', 'RelationNicks', 'RelationMinWeight',
            'ShowTimePersonalities', 'ShowConcentration', 'ShowSignatureWords',
            'ShowNavBar', 'HomeLink', 'BadUrls', 'ChannelIndex']

def cards(chapter_html):
    """Turn <section class="option"> blocks into the site's option cards."""
    def one(m):
        oid, name, purpose, body = m.group(1), m.group(2), m.group(3), m.group(4)
        body = tidy(body)
        body = re.sub(r'<h4>Description</h4>\s*', '', body)
        body = re.sub(r'<h4>Default</h4>\s*<p>(.*?)</p>', '', body, flags=re.S)
        default = re.search(r'<h4>Default</h4>\s*<p>(.*?)</p>',
                            m.group(4), re.S)
        default = re.sub(r'\s+', ' ', default.group(1)).strip() if default else 'Unset'
        badge = ' <span class="since">1.0a</span>' if oid in NEW_1_0A else ''
        return ('<article class="opt" id="%s" data-k="%s %s">\n'
                '<h3><a class="anchor" href="#%s" aria-label="Link to %s">%s</a>'
                '<span class="purpose">%s</span>%s</h3>\n%s\n'
                '<p class="meta"><b>Default:</b> %s</p>\n</article>'
                % (oid, oid.lower(), purpose.lower(), oid, oid, oid, purpose, badge,
                   body.strip(), default))
    return re.sub(r'<section class="option" id="([^"]+)"><h3>([^<]*?)\s*'
                  r'<span class="purpose">([^<]*)</span></h3>(.*?)\n</section>',
                  one, chapter_html, flags=re.S)

# ---------------------------------------------------------------------------
# 1. the guide chapters, with the parts that have aged fixed
# ---------------------------------------------------------------------------
guide1 = tidy(chapter('what-is-pisg'))
guide2 = tidy(chapter('setting-up-pisg'))

guide2 = re.sub(
  r'<p>There are a few predefined color schemes.*?softgreen\.</p>',
  '<p>There are predefined colour schemes for you to use &mdash; set one with the '
  '<a href="#ColorScheme">ColorScheme</a> option. pisg 1.0a added four modern ones &mdash; '
  '<code>modern</code>, <code>midnight</code>, <code>amoled</code> and <code>terminal</code>; '
  '<code>modern</code> follows the reader\'s light/dark setting. The eight classic schemes are '
  'unchanged: '
  '<code>default</code> (still the default), <code>darkgalaxy</code>, <code>darkred</code>, '
  '<code>justgrey</code>, <code>ocean</code>, <code>orange_grey</code>, <code>pisg</code> and '
  '<code>softgreen</code>. <a href="../themes/">See them side by side, or build your own</a>.</p>',
  guide2, flags=re.S)

guide2 = re.sub(
  r'<p>If you have created a nice stylesheet which others? can take advantage of,.*?</p>',
  '<p>The four modern schemes are generated from one palette by '
  '<code>layout/build-themes.py</code>, so to change them all at once &mdash; or add a fifth in the '
  'same style &mdash; edit the palette in that script and run it, rather than editing the CSS files '
  'one by one. There is also a <a href="../themes/">theme creator</a> on this site that '
  'builds the file for you.</p>\n'
  '<p>If you have made a stylesheet others could use, open a pull request on '
  '<a href="https://github.com/PISG/pisg">GitHub</a> so it can ship with the next version.</p>',
  guide2, flags=re.S)

guide2 = re.sub(
  r'<section id="mailing-list-and-bugs"><h3>Obtaining help and reporting bugs</h3>.*?</section>',
  '<section id="mailing-list-and-bugs"><h3>Obtaining help and reporting bugs</h3>\n'
  '<p>If this page did not answer it, ask in <code>#pisg</code> on Undernet '
  '(<code>irc.undernet.org</code>) &mdash; that is where the people who work on pisg are.</p>\n'
  '<p>For bugs, patches and feature requests, use the '
  '<a href="https://github.com/PISG/pisg/issues">issue tracker</a> on GitHub. Say which pisg version '
  'you run and which log format, and paste the error: pisg prints the channel it was working on when '
  'it stopped.</p>\n'
  '<p>The old SourceForge tracker and the <code>pisg-general</code> mailing list are read-only '
  'history now. They are still worth searching &mdash; fifteen years of answers are in there &mdash; '
  'at <a href="https://sourceforge.net/projects/pisg/">sourceforge.net/projects/pisg</a>.</p>\n'
  '</section>',
  guide2, flags=re.S)

# the old manual says "pisg-0.37" in the shell prompt; make it current
guide2 = guide2.replace('user@host:pisg-0.37$ ./pisg', 'user@host:~/pisg$ ./pisg')  # older manuals

# ---------------------------------------------------------------------------
# 2. the reference chapters as cards
# ---------------------------------------------------------------------------
ref_general  = cards(chapter('reference'))
ref_stats    = cards(chapter('reference-stats'))
ref_pictures = cards(chapter('reference-pictures'))
ref_misc     = cards(chapter('reference-misc'))
copyright_ch = tidy(chapter('copyright'))
example_ch   = tidy(chapter('example-config'))

# the shipped example config still offers a theme that is no longer distributed
example_ch = example_ch.replace('midnight, amoled, terminal, canada, or default',
                                'midnight, amoled, terminal, or default')
example_ch = example_ch.replace('midnight%2C%20amoled%2C%20terminal%2C%20canada%2C%20or%20default',
                                'midnight%2C%20amoled%2C%20terminal%2C%20or%20default')

# the example config chapter ships its own copy/download bar; give it the site's classes
example_ch = example_ch.replace('class="btn copy"', 'class="btn small copybtn"')
example_ch = example_ch.replace('class="btn"', 'class="btn small"')

# ---------------------------------------------------------------------------
# 3. a short chapter pointing at the options added in 1.0a
# ---------------------------------------------------------------------------
ref_new = ('<p class="sec-intro">The seven sections added in 1.0a are on by default in every colour '
           'scheme. Set them to <code>0</code> for the page pisg wrote before 1.0a &mdash; see the '
           '<a href="../changelog/#v1.0-upgrading">upgrade notes</a>. Each option is described in its '
           'chapter, marked <span class="since">1.0a</span>.</p>\n'
           + '<div class="pill-row">'
           + ''.join('<a class="pill" href="#%s">%s</a>' % (o, o) for o in NEW_1_0A)
           + '</div>')

# ---------------------------------------------------------------------------
# 4. the tools chapter
# ---------------------------------------------------------------------------
tools = u'''<p class="sec-intro">None of these are needed to run pisg. They live in <code>scripts/</code>
and each one solves something that otherwise means editing config files by hand. Every one of them
refuses to overwrite work you did yourself.</p>

<section id="tool-eggdrop"><h3>eggdrop-pisg.tcl &mdash; profiles people manage from IRC</h3>
<p>A Tcl script for an <a href="https://www.eggheads.org/">eggdrop</a> (Tcl 8.6) that lets the people in
your channel set their own <code>&lt;user&gt;</code> options, so you do not have to. The bot writes a
config file; pisg reads it:</p>
<pre>&lt;include="users.cfg"&gt;</pre>
<p>Nothing is stored inside pisg itself, and the file is plain text you can read and edit. Commands work
in the channel with <code>!</code> and in a private message without it:</p>
<div class="table-scroll">
<table>
<thead><tr><th>Command</th><th>What it does</th></tr></thead>
<tbody>
<tr><td><code>!pisghelp [command]</code></td><td>Explains the commands, one at a time.</td></tr>
<tr><td><code>!pisginfo</code></td><td>Set your sex, your picture and your link.</td></tr>
<tr><td><code>!pisgmerge</code></td><td>Count another of your nicks as the same person.</td></tr>
<tr><td><code>!pisgunmerge</code></td><td>Undo that.</td></tr>
<tr><td><code>!pisgshow</code></td><td>Show what the bot has stored for you.</td></tr>
<tr><td><code>!pisgdel</code></td><td>Delete your own entry.</td></tr>
<tr><td><code>!pisgdeluser</code></td><td>Delete somebody else&rsquo;s entry. Bot masters only.</td></tr>
<tr><td><code>!pisgstats</code></td><td>Reply with the address of the stats page. Open to everyone; in the
channel only.</td></tr>
</tbody>
</table>
</div>
<p>The rules it enforces, which are what make opening this up safe:</p>
<ul>
  <li>People are identified by their <strong>network account</strong> (<code>getaccount</code>, or the
  account host on Undernet), not by the nick they happen to be using.</li>
  <li>Somebody can only claim the nick they are currently using.</li>
  <li>A <code>&lt;user&gt;</code> line <strong>you</strong> wrote by hand can never be overwritten by
  the bot.</li>
  <li>Changes are rate limited.</li>
  <li><code>!pisgstats</code> does not run pisg inside the bot &mdash; it only answers with a link.</li>
</ul>
<p>A test suite, <code>eggdrop-pisg-test.tcl</code>, ships with it: 107 checks. Run it before you load
the script on a busy bot.</p>
</section>

<section id="tool-autoalias"><h3>pisg-autoalias.py &mdash; merge nicks automatically</h3>
<p>Python 3. On a network with account services the same person shows up as <code>nick</code>,
<code>nick|afk</code>, <code>nick_</code> and <code>nick2</code> &mdash; but all of them share one
authenticated host, such as <code>*.users.undernet.org</code>. This script reads your logs, groups nicks
by that host, and writes an include file of <code>&lt;user&gt;</code> lines with aliases. Run it before
pisg, from the same cron job.</p>
<pre>python3 scripts/pisg-autoalias.py --logdir ~/eggdrop/logs --prefix nightshift.log. \\
    --manual ~/pisg/pisg.cfg --out ~/pisg/aliases.auto.cfg</pre>
<pre>&lt;include="/home/you/pisg/aliases.auto.cfg"&gt;</pre>
<p><code>--manual</code> names the config files whose <code>&lt;user&gt;</code> lines are yours (repeat it
for each); <code>--hosts</code> changes the host pattern for another network; <code>--report</code> prints
what was merged and what was skipped, and why.</p>
<p>What it will not do: merge a shared host, a gateway, or a bouncer several people use; and it never
touches a nick you already described yourself &mdash; your own lines always win. A test suite ships with
it.</p>
</section>

<section id="tool-adiirc"><h3>adiirc2eggdrop.py &mdash; turn client logs into bot logs</h3>
<p>Python 3. You have years of channel history in your client&rsquo;s log folder and a bot that only
started logging last spring. This converts the client logs into the format a bot writes, so the old
history can join the statistics:</p>
<pre>python3 scripts/adiirc2eggdrop.py "#nightshift.log" logs/ --channel '#nightshift' --nick YourNick \\
    --tz Europe/Paris --before '2026-01-31 03:00' --prefix nightshift.log.</pre>
<p><code>--tz</code> is the time zone your client logged in, <code>--before</code> the moment (UTC) your
bot started logging, and <code>--nick</code> your own nick. Add <code>--dry-run</code> to see what it would
write. <code>--format znc</code> writes what the ZNC log module writes instead: one
<code>YYYY-MM-DD.log</code> per day, read with <code>Format="energymech"</code>. The rules it follows:</p>
<ul>
  <li>Public channel events only. Private messages, notices, <code>/whois</code> output and server text are
  dropped.</li>
  <li>Local timestamps are converted to UTC, which is what bots log in.</li>
  <li>It never overwrites an existing file.</li>
  <li>It stops at <code>--before</code>, where your real logging starts, so nothing is counted twice.</li>
</ul>
</section>

<section id="tool-znc"><h3>znc-setup.sh &mdash; let pisg read a ZNC log folder</h3>
<p>Shell. ZNC&rsquo;s logs live under the ZNC user&rsquo;s home directory, and pisg usually runs as
somebody else. This script puts converted logs into the right ZNC account folder and opens up read
access to exactly the channel folders pisg needs &mdash; not the whole home directory.</p>
<p>Put the converted logs in <code>~/znc-import/#channel/</code> of the pisg user, then, as the ZNC
account (or with <code>sudo</code>):</p>
<pre>PISG_USER=stats bash scripts/znc-setup.sh            # shows what it found and what it would do
PISG_USER=stats bash scripts/znc-setup.sh --apply    # does it</pre>
<p>Without <code>--apply</code> it changes nothing, so you can read the plan first. It never deletes or
replaces a file, and it links each channel folder to <code>~/znc-logs/</code> of the pisg
user, so the configuration does not need to know ZNC&rsquo;s layout:</p>
<pre>&lt;channel="#nightshift"&gt;
 Format = "energymech"
 LogDir = "/home/stats/znc-logs/nightshift/"
&lt;/channel&gt;</pre>
</section>
'''

# ---------------------------------------------------------------------------
# 5. sidebar + option index
# ---------------------------------------------------------------------------
def index_pills(html):
    ids = re.findall(r'<article class="opt" id="([^"]+)"', html)
    return ('<div class="pill-row">'
            + ''.join('<a class="pill" href="#%s">%s</a>' % (i, i) for i in ids)
            + '</div>')

CHAPTERS = [
  ('what-is-pisg',      'What is pisg?',            guide1,       None),
  ('setting-up-pisg',   'Setting up pisg',          guide2,       None),
  ('reference',         'General options',          ref_general,  'General options'),
  ('reference-stats',   'Statistics options',       ref_stats,    'Statistics options'),
  ('reference-new',     'Options added in 1.0a',     ref_new,      'Options added in 1.0'),
  ('reference-pictures','Picture options',          ref_pictures, 'Picture options'),
  ('reference-misc',    'Misc options',             ref_misc,     'Misc options'),
  ('tools',             'Optional tools',           tools,        None),
  ('example-config',    'Example configuration',    example_ch,   None),
  ('copyright',         'Copyright and licence',    copyright_ch, None),
]

body, nav_start, nav_ref, nav_end = [], [], [], []
for n, (cid, title, html, isref) in enumerate(CHAPTERS, 1):
    pills = index_pills(html) if isref and cid != 'reference-new' else ''
    body.append('<section id="%s">\n<h2><span class="hash">#</span>%s</h2>\n%s%s\n</section>'
                % (cid, title, pills, html))
    # sub-sections of the two guide chapters get their own sidebar entries
    subs = re.findall(r'<section id="([^"]+)"><h3>([^<]*)</h3>', html) if not isref else []
    entry = '    <a href="#%s">%s</a>' % (cid, title)
    sub_entries = ['    <a class="sub" href="#%s">%s</a>' % (s, t) for s, t in subs]
    if cid in ('what-is-pisg', 'setting-up-pisg'):
        nav_start.append(entry); nav_start += sub_entries
    elif isref:
        nav_ref.append(entry)
    else:
        nav_end.append(entry); nav_end += sub_entries

body = '\n\n'.join(body)
nav = ('    <h5>Start here</h5>\n' + '\n'.join(nav_start) +
       '\n    <h5>Option reference</h5>\n' + '\n'.join(nav_ref) +
       '\n    <h5>More</h5>\n' + '\n'.join(nav_end))

n_opts = len(re.findall(r'<article class="opt"', body))

# ---------------------------------------------------------------------------
# 6. the page
# ---------------------------------------------------------------------------
PAGE = u'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#0b0e13">
<link rel="canonical" href="https://pisg.github.io/docs/">
<title>Documentation — pisg</title>
<meta name="description" content="The pisg manual: how to install it, how to write pisg.cfg, what every one of its @@NOPTS@@ options does, the optional tools, and a complete example configuration.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%230d1117'/><rect x='18' y='52' width='14' height='30' fill='%2358a6ff'/><rect x='38' y='34' width='14' height='48' fill='%233fd18b'/><rect x='58' y='44' width='14' height='38' fill='%23e5b567'/><rect x='78' y='24' width='14' height='58' fill='%23bc8cff'/></svg>">
<link rel="stylesheet" href="../assets/site.css?v=ae94b127">
</head>
<body class="has-sidebar">
<a class="skip" href="#main">Skip to content</a>

<div class="layout">

<!-- ===================== SIDEBAR ===================== -->
<nav class="sidebar" id="sidebar" aria-label="Documentation">
  <a class="logo" href="../">
    <span class="dollar">$</span>
    <span><b>pisg</b><small>1.0a &middot; DOCUMENTATION</small></span>
  </a>
  <input id="search" type="search" placeholder="Filter options… ( / )" autocomplete="off" spellcheck="false" aria-label="Filter options">
  <p class="search-hint"><span id="search-count"></span>&nbsp;</p>
  <div class="nav" id="nav">
@@NAV@@
    <h5>Elsewhere</h5>
    <a class="out" href="../">Home</a>
    <a class="out" href="../changelog/">Changelog</a>
    <a class="out" href="../themes/">Themes &amp; creator</a>
    <a class="out" href="../demo/">Live example</a>
    <a class="out" href="https://github.com/PISG/pisg">GitHub ↗</a>
  </div>
</nav>

<!-- ===================== MAIN ===================== -->
<div class="main"><div class="wrap">
<main id="main" tabindex="-1">

<button class="side-btn" id="side-btn" aria-expanded="false" aria-controls="sidebar">☰ Contents</button>

<div class="hero doc">
  <h1>pisg <span>documentation</span></h1>
  <p class="tagline">How to set pisg up, how to write <code>pisg.cfg</code>, and what every option does.</p>
  <div class="badges">
    <span class="badge hot">1.0a</span>
    <span class="badge">@@NOPTS@@ options</span>
    <span class="badge">Perl 5</span>
    <span class="badge gold">GPL-2.0-or-later</span>
    <span class="badge">also ships as <code>docs/pisg-doc.html</code></span>
  </div>
  <p class="sec-intro" style="margin-top:18px">Everything here applies to 0.73 as well, except the
  options marked <span class="since">1.0a</span>. Use the filter in the sidebar, or press
  <kbd>/</kbd>, to find an option by name or by what it does.</p>
</div>

@@BODY@@

<footer>
  <p><a href="../">pisg</a> &middot; <a href="../changelog/">Changelog</a> &middot;
  <a href="../demo/">Live example</a> &middot;
  <a href="https://github.com/PISG/pisg">GitHub</a> &middot;
  <a href="https://sourceforge.net/projects/pisg/">Original project</a></p>
  <p style="margin-top:8px"><a href="../privacy/">Privacy</a> &middot;
  <a href="../cookies/">Cookies</a> &middot; <a href="../terms/">Terms</a></p>
  <p style="margin-top:8px">pisg 1.0a is free software under the GPL, version 2 or later. Started in 2001 by
  Morten “mbrix” Brix Pedersen.</p>
</footer>

</main>
</div></div>
</div>

<button id="top-btn" title="Back to top" aria-label="Back to top">↑</button>
<script src="../assets/site.js?v=ae94b127"></script>
</body>
</html>
'''
PAGE = (PAGE.replace('@@NAV@@', nav)
            .replace('@@BODY@@', body)
            .replace('@@NOPTS@@', str(n_opts)))

if not os.path.isdir(os.path.dirname(OUT)):
    os.makedirs(os.path.dirname(OUT))
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(PAGE)
print('wrote %s  (%d bytes, %d options, %d chapters)' % (OUT, len(PAGE), n_opts, len(CHAPTERS)))

# a quick self-check: every in-page link must have a target
ids = set(re.findall(r'\sid="([^"]+)"', PAGE))
missing = sorted({m for m in re.findall(r'href="#([^"]+)"', PAGE) if m not in ids})
print('dangling anchors:', missing or 'none')
