# -*- coding: utf-8 -*-
"""
Build docs/index.html out of the manual pisg ships (docs/pisg-doc.html, generated
from docs/pisg-doc.xml), plus two chapters that manual does not have: upgrading, and the optional tools.

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
        # head (name, purpose, default) and body are separate so wide screens can set them side by side
        return ('<article class="opt" id="%s" data-k="%s %s">\n'
                '<div class="opt-head"><h3><a class="anchor" href="#%s" aria-label="Link to %s">%s</a>%s</h3>'
                '<p class="purpose">%s</p>'
                '<p class="meta"><b>Default</b> %s</p></div>\n'
                '<div class="opt-body">\n%s\n</div>\n</article>'
                % (oid, oid.lower(), purpose.lower(), oid, oid, oid, badge, purpose,
                   default, body.strip()))
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
# 4. upgrading: the manual has no chapter for it; this follows the release notes
#    (docs/RELEASE-NOTES-1.0.md in the pisg repository)
# ---------------------------------------------------------------------------
OLD_PAGE = ['ShowOverview', 'ShowRelations', 'ShowTimePersonalities', 'ShowConcentration',
            'ShowSignatureWords', 'ShowNavBar']

def crow(n, cmd, note):
    return ('  <div class="crow"><span class="cnum">%s</span>\n'
            '    <div><div class="cmdline">%s</div>\n'
            '    <span class="cnote">%s</span></div>\n'
            '    <button class="copybtn" type="button">Copy</button></div>\n' % (n, cmd, note))

upgrading = (u'''<p class="sec-intro">Coming from 0.73 or one of the 0.80 previews? Upgrading is a copy, not a
migration: 1.0a reads the same <code>pisg.cfg</code>, the same logs and the same log formats. The one
thing you will notice is that your stats page gets <strong>longer</strong> &mdash; seven new sections are on
by default. Everything else is opt-in.</p>

<div class="upg-grid">
  <div class="upg-card"><b>Stays the same</b>
    <ul><li>Your <code>pisg.cfg</code>, every option in it, and the files it includes</li>
    <li>Log formats and parsers</li><li>The default colour scheme, and how the classic ones look</li>
    <li>Requirements: just Perl</li></ul></div>
  <div class="upg-card new"><b>Changes</b>
    <ul><li>Seven new sections, on by default</li><li>A section menu (<code>ShowNavBar</code>)</li>
    <li>Exit status <code>1</code> when a run fails</li>
    <li>A page is replaced only once it is complete</li></ul></div>
  <div class="upg-card opt-in"><b>Yours to switch on</b>
    <ul><li>The modern themes (<code>ColorScheme</code>)</li><li>The landing page for several channels</li>
    <li><code>BadUrls</code>, <code>HomeLink</code></li><li>The optional tools in <code>scripts/</code></li></ul></div>
</div>

<section id="upgrade-before"><h3>Before you start</h3>
<p>Find out what you are running now, so you know which notes apply:</p>
<pre>./pisg --version</pre>
<p>Then put a copy of everything that is yours somewhere safe. A new release ships its own
<code>pisg.cfg</code>, so unpacking one on top of your install would replace your configuration with the
sample:</p>
<ul>
  <li><code>pisg.cfg</code>, and every file it pulls in with <code>&lt;include="..."&gt;</code> &mdash; a
  <code>users.cfg</code>, an alias file;</li>
  <li>any stylesheet you made or edited in <code>layout/</code>;</li>
  <li>your changes to <code>lang.txt</code>, if you translated or reworded anything;</li>
  <li>the crontab line or scheduled task that runs pisg (<code>crontab -l</code> shows it).</li>
</ul>
</section>

<section id="upgrade-steps"><h3>Upgrade in four steps</h3>
<p>Install the new version <em>next to</em> the old one instead of over it. Then going back is only a
matter of pointing your cron job at the old folder again.</p>
<div class="console">
  <div class="bar"><i></i><i></i><i></i><span>upgrade 0.73 &rarr; 1.0a</span></div>
''' + crow('1', '<span class="cmd">git</span> <span class="arg">clone https://github.com/PISG/pisg.git ~/pisg-1.0a</span>',
           'Or unpack the archive from the <a href="https://github.com/PISG/pisg/releases">releases page</a> '
           'into a new folder.')
    + crow('2', '<span class="cmd">cp</span> <span class="arg">~/pisg/pisg.cfg ~/pisg/users.cfg ~/pisg-1.0a/</span>',
           'Bring your configuration across, with every file it includes. Use the names yours '
           'actually has &mdash; <code>users.cfg</code> is only an example.')
    + crow('3', '<span class="cmd">cd</span> <span class="arg">~/pisg-1.0a &amp;&amp; ./pisg</span>',
           'Run it once by hand and read what it prints. A channel it cannot read is skipped with a '
           'reason, and the others are still made.')
    + crow('4', '<span class="cmd">crontab</span> <span class="arg">-e</span>',
           'Point the scheduled run at <code>~/pisg-1.0a/pisg</code>. Keep the old folder until you '
           'are happy with the new pages.')
    + u'''</div>
<p>On Windows it is the same: a new folder, your <code>pisg.cfg</code> copied into it, and the scheduled
task changed to run <code>perl pisg</code> from there.</p>
</section>

<section id="upgrade-sections"><h3>The new sections are on by default</h3>
<p>Your next page will have an overview, a <em>who talks to whom</em> map, closest pairs, social roles,
time personalities, <em>who carries the channel</em>, signature words and a section menu. In the classic
colour schemes they are drawn in a plain style that fits the old look.</p>
<p>To keep the page exactly as it was, switch them off in <code>pisg.cfg</code>:</p>
<pre>''' + '\n'.join('&lt;set %s="0"&gt;' % o for o in OLD_PAGE) + u'''</pre>
<p>Or keep some: each is described in the option reference &mdash;
''' + ', '.join('<a href="#%s">%s</a>' % (o, o) for o in OLD_PAGE) + u'''.
The relation map has two tuning options of its own, <a href="#RelationNicks">RelationNicks</a> and
<a href="#RelationMinWeight">RelationMinWeight</a>, for channels where it is too crowded or too sparse.</p>
</section>

<section id="upgrade-scripts"><h3>Scripts and cron jobs: pisg now fails loudly</h3>
<p>pisg 0.73 exited with status <code>0</code> even when it had failed. 1.0a exits with <code>1</code>
&mdash; and it does so when one channel out of several was skipped, while still writing the pages for the
others. If a wrapper script does <code>pisg &amp;&amp; upload</code>, that upload will now stop on
a partial failure. Decide which you want:</p>
<pre>./pisg --silent &amp;&amp; ./upload.sh     # upload only when every channel worked
./pisg --silent;    ./upload.sh     # upload whatever was made</pre>
<p>The good news that comes with it: pages are written to a temporary file and moved into place only when
complete, so a failed run can no longer leave a half-written page on your site.</p>
</section>

<section id="upgrade-cache"><h3>If you use CacheDir</h3>
<p>Empty the cache folder once after upgrading, so every log is parsed again by the new version. The cache
holds the results of the old parser, and 1.0a gathers things 0.73 never collected &mdash; the relation map,
for one. The <a href="#CacheDir">CacheDir</a> option already asks for this whenever the settings change;
a new version is the same case.</p>
</section>

<section id="upgrade-optional"><h3>Optional: the new look and the landing page</h3>
<p>None of this happens unless you ask for it.</p>
<ul>
  <li><strong>A modern theme</strong> &mdash; <code>&lt;set ColorScheme="modern"&gt;</code>, or
  <code>midnight</code>, <code>amoled</code>, <code>terminal</code>. <code>modern</code> follows the
  reader&rsquo;s light or dark setting. <a href="../themes/">Compare them, or build your own</a>.</li>
  <li><strong>A landing page for several channels</strong> &mdash; copy <code>site/index.html</code> into
  your output folder and run pisg once, so <code>channels.json</code> exists beside it
  (<a href="#ChannelIndex">ChannelIndex</a>). Add <code>&lt;set HomeLink="index.html"&gt;</code> to put
  an &ldquo;All channels&rdquo; button on every stats page. <a href="../demo/">See it live</a>.</li>
  <li><strong>Cleaner link statistics</strong> &mdash; <a href="#BadUrls">BadUrls</a> keeps spam and
  image-host links out of the URL tables.</li>
  <li><strong>The <a href="#tools">optional tools</a></strong> &mdash; they need Python 3, or Tcl 8.6 and
  an eggdrop. pisg itself still needs only Perl; <code>JSON::PP</code>, which
  <code>ChannelIndex</code> uses, is part of core Perl.</li>
</ul>
<div class="note good">Something did not come across the way you expected? Ask in <code>#pisg</code> on
Undernet or open an <a href="https://github.com/PISG/pisg/issues">issue</a>, and say which version you came
from. The full list of changes is in the <a href="../changelog/">changelog</a>.</div>
</section>
''')

# ---------------------------------------------------------------------------
# 5. the tools chapter
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
# 6. sidebar + option index
# ---------------------------------------------------------------------------
def index_pills(html):
    ids = re.findall(r'<article class="opt" id="([^"]+)"', html)
    return ('<div class="pill-row">'
            + ''.join('<a class="pill" href="#%s">%s</a>' % (i, i) for i in ids)
            + '</div>')

# (group, id, title, html, pill index?) — the group is the sidebar heading and the chapter's kicker
CHAPTERS = [
  ('Start here',       'what-is-pisg',       'What is pisg?',          guide1,       False),
  ('Start here',       'setting-up-pisg',    'Setting up pisg',        guide2,       False),
  ('Start here',       'upgrading',          'Upgrading to 1.0a',      upgrading,    False),
  ('Option reference', 'reference',          'General options',        ref_general,  True),
  ('Option reference', 'reference-stats',    'Statistics options',     ref_stats,    True),
  ('Option reference', 'reference-new',      'Options added in 1.0a',  ref_new,      False),
  ('Option reference', 'reference-pictures', 'Picture options',        ref_pictures, True),
  ('Option reference', 'reference-misc',     'Misc options',           ref_misc,     True),
  ('More',             'tools',              'Optional tools',         tools,        False),
  ('More',             'example-config',     'Example configuration',  example_ch,   False),
  ('More',             'copyright',          'Copyright and licence',  copyright_ch, False),
]

body, nav, group = [], [], None
for n, (grp, cid, title, html, pills) in enumerate(CHAPTERS, 1):
    body.append('<section id="%s" class="chapter">\n'
                '<p class="kicker"><span class="ch-num">%02d</span>%s</p>\n'
                '<h2><a class="anchor" href="#%s">%s</a></h2>\n%s%s\n</section>'
                % (cid, n, grp, cid, title, index_pills(html) if pills else '', html))
    if grp != group:
        nav.append('    <h5>%s</h5>' % grp)
        group = grp
    nav.append('    <a href="#%s">%s</a>' % (cid, title))
    # sub-sections of the prose chapters get their own sidebar entries; option cards do not
    if 'class="opt"' not in html:
        nav += ['    <a class="sub" href="#%s">%s</a>' % (s, t)
                for s, t in re.findall(r'<section id="([^"]+)"><h3>([^<]*)</h3>', html)]

body = '\n\n'.join(body)
nav = '\n'.join(nav)

n_opts = len(re.findall(r'<article class="opt"', body))

# ---------------------------------------------------------------------------
# 7. the page
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
<meta name="description" content="The pisg manual: how to install it, how to upgrade, how to write pisg.cfg, what every one of its @@NOPTS@@ options does, the optional tools, and a complete example configuration.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%230d1117'/><rect x='18' y='52' width='14' height='30' fill='%2358a6ff'/><rect x='38' y='34' width='14' height='48' fill='%233fd18b'/><rect x='58' y='44' width='14' height='38' fill='%23e5b567'/><rect x='78' y='24' width='14' height='58' fill='%23bc8cff'/></svg>">
<link rel="stylesheet" href="../assets/site.css?v=852d3d9c">
</head>
<body class="has-sidebar docs-page" id="top">
<a class="skip" href="#main">Skip to content</a>

<header class="top">
  <div class="wrap">
    <a class="brand" href="../" aria-label="pisg — home">
      <span><span class="dollar">$</span>&nbsp;pisg</span>
      <span class="ver">1.0a</span>
    </a>
    <span class="crumb" aria-hidden="true">/ docs</span>
    <button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="navlinks"><span aria-hidden="true">&#9776;</span><span class="sr-only">Menu</span></button>
    <nav class="links" id="navlinks" aria-label="Main">
      <a href="../">Home</a>
      <a href="../#install">Install</a>
      <a href="./" aria-current="page">Documentation</a>
      <a href="../themes/">Themes</a>
      <a href="../changelog/">Changelog</a>
      <span class="sep" aria-hidden="true"></span>
      <a class="ext" href="../demo/">Live example &#8599;</a>
      <a class="x-reg" href="https://github.com/PISG/pisg">GitHub &#8599;</a>
    </nav>
  </div>
</header>

<div class="layout">

<!-- ===================== SIDEBAR ===================== -->
<nav class="sidebar" id="sidebar" aria-label="Documentation">
  <div class="search-box">
    <input id="search" type="search" placeholder="Filter options…" autocomplete="off" spellcheck="false" aria-label="Filter options">
    <kbd aria-hidden="true">/</kbd>
  </div>
  <p class="search-hint"><span id="search-count"></span>&nbsp;</p>
  <div class="nav" id="nav">
@@NAV@@
  </div>
</nav>

<!-- ===================== MAIN ===================== -->
<div class="main">
<main id="main" tabindex="-1">

<button class="side-btn" id="side-btn" aria-expanded="false" aria-controls="sidebar">☰ Contents</button>

<div class="doc-hero">
  <p class="eyebrow"><span class="dot" aria-hidden="true"></span>Manual &middot; pisg 1.0a</p>
  <h1><span class="dollar">$</span> man pisg</h1>
  <p class="tagline">How to set pisg up, how to upgrade, how to write <code>pisg.cfg</code>, and what every
  one of its @@NOPTS@@ options does. Everything applies to 0.73 as well, except the options marked
  <span class="since">1.0a</span>.</p>
  <div class="doc-quick">
    <a class="card" href="#setting-up-pisg"><span class="ico">new here</span><h3>Setting up pisg</h3>
      <p>Logs, a channel block, your first page.</p></a>
    <a class="card" href="#upgrading"><span class="ico">from 0.73 / 0.80</span><h3>Upgrading to 1.0a</h3>
      <p>Four steps, and what changes on your page.</p></a>
    <a class="card" href="#reference"><span class="ico">@@NOPTS@@ options</span><h3>Option reference</h3>
      <p>Filter by name or purpose &mdash; press <kbd>/</kbd>.</p></a>
    <a class="card" href="#example-config"><span class="ico">copy &amp; go</span><h3>Example config</h3>
      <p>A complete <code>pisg.cfg</code> to start from.</p></a>
  </div>
</div>

<div class="doc-body">
@@BODY@@
</div>

<footer class="doc-foot">
  <p><a href="../">pisg</a> &middot; <a href="../changelog/">Changelog</a> &middot;
  <a href="../themes/">Themes</a> &middot; <a href="../demo/">Live example</a> &middot;
  <a href="https://github.com/PISG/pisg">GitHub</a> &middot;
  <a href="https://sourceforge.net/projects/pisg/">Original project</a></p>
  <p><a href="../privacy/">Privacy</a> &middot;
  <a href="../cookies/">Cookies</a> &middot; <a href="../terms/">Terms</a></p>
  <p>pisg 1.0a is free software under the GPL, version 2 or later. Started in 2001 by
  Morten “mbrix” Brix Pedersen. This page is built from <code>docs/pisg-doc.html</code>, which ships
  with pisg.</p>
</footer>

</main>
</div>
</div>

<button id="top-btn" title="Back to top" aria-label="Back to top">↑</button>
<script src="../assets/site.js?v=852d3d9c"></script>
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
