# -*- coding: utf-8 -*-
"""Assemble new/docs.html from the old site's documentation body plus the 1.0 additions."""
import io, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)                       # .../pisg.github.io/new
SRC  = os.path.join(os.path.dirname(SITE), 'index.html')   # the 2016 site's index.html
OUT  = os.path.join(SITE, 'docs.html')

# The old site keeps the whole manual inside <main class="docs-content">; take it from there.
_old = io.open(SRC, encoding='utf-8').read()
body = _old[_old.index('<main class="docs-content">') + len('<main class="docs-content">'):
            _old.index('</main>')]
body = body.replace('<p><em>pisg 0.73 documentation — how to install and configure pisg.</em></p>\n', '')
body = re.sub(r'<p class="back-top">.*?</p>\s*$', '', body, flags=re.S)
body = body.replace('class="opt-link" ', '')

# --------------------------------------------------------------------------
# 1. corrections / updates to the inherited text
# --------------------------------------------------------------------------

body = body.replace(
 '<h3 id="mailing-list-and-bugs">Obtaining help and reporting bugs</h3>\n'
 '<p>If your problem could not be resolved through here, then you should send an e-mail to the pisg mailing list. You can subscribe and see more info at <a href="http://lists.sourceforge.net/lists/listinfo/pisg-general">lists.sourceforge.net/lists/listinfo/pisg-general</a>.</p>\n'
 '<p>If you believe that you have found a bug, you should use the SourceForge <a href="http://sourceforge.net/tracker/?group_id=31862&amp;atid=403711">bug tracking system</a>.</p>',
 '<h3 id="mailing-list-and-bugs">Obtaining help and reporting bugs</h3>\n'
 '<p>If this page did not answer it, ask in <code>#PISG</code> on Undernet '
 '(<code>irc.undernet.org</code>) &mdash; that is where the people who work on pisg are.</p>\n'
 '<p>For bugs, patches and feature requests, use the '
 '<a href="https://github.com/PISG/pisg/issues">issue tracker</a> on GitHub. Say which pisg version '
 'you run, which log format, and paste the error: <code>./pisg</code> prints the channel it was working '
 'on when it stopped.</p>\n'
 '<p>The old SourceForge tracker and the <code>pisg-general</code> mailing list are read-only history. '
 'They are still worth searching &mdash; fifteen years of answers are in there &mdash; at '
 '<a href="https://sourceforge.net/projects/pisg/">sourceforge.net/projects/pisg</a>.</p>')

# ColorScheme list of schemes: mention the 1.0 themes
body = body.replace(
 'The colorschemes distributed with pisg are: default (which is the default), darkgalaxy, darkred, justgrey, ocean, orange_grey, pisg, softgreen.',
 'The colour schemes distributed with pisg are the five modern ones added in 1.0 &mdash; '
 '<code>modern</code>, <code>midnight</code>, <code>amoled</code>, <code>terminal</code>, '
 '<code>canada</code> &mdash; and the eight classic ones: <code>default</code> (which is still the '
 'default), <code>darkgalaxy</code>, <code>darkred</code>, <code>justgrey</code>, <code>ocean</code>, '
 '<code>orange_grey</code>, <code>pisg</code>, <code>softgreen</code>. '
 '<a href="index.html#themes">See all of them side by side</a>.')

body = body.replace(
 '<p>If you have created a nice stylesheet which others can take advantage of, you are encouraged to send it to the pisg mailing list so that it can be distributed with the next version of pisg.</p>',
 '<p>The five modern schemes are generated from a single palette by '
 '<code>layout/build-themes.py</code>, so if you want to change all of them at once &mdash; or add a '
 'sixth in the same style &mdash; edit the palette in that script and run it instead of editing the '
 'CSS files.</p>\n'
 '<p>If you have created a nice stylesheet which others can take advantage of, you are encouraged to '
 'open a pull request on <a href="https://github.com/PISG/pisg">GitHub</a> so that it can be '
 'distributed with the next version of pisg.</p>')

# a short pointer under the intro of the reference
body = body.replace(
 '<h2 id="reference">General pisg options</h2>',
 '<h2 id="reference">General pisg options</h2>\n'
 '<p class="muted">Every option below can be set globally with <code>&lt;set Option="value"&gt;</code> '
 'or inside a <code>&lt;channel&gt;</code> block, where it applies to that channel only. Option names '
 'are not case sensitive.</p>')

# --------------------------------------------------------------------------
# 2. new 1.0 option reference, inserted before the picture options
# --------------------------------------------------------------------------

def opt(oid, title, code, desc, default, since=True):
    badge = ' <span class="since">1.0</span>' if since else ''
    return (
      '<div class="opt" id="%s">\n<h4>%s%s</h4>\n<pre>%s</pre>\n<p><b>Description:</b> %s</p>\n'
      '<p class="meta"><b>Default:</b> %s</p>\n</div>\n' % (oid, title, badge, code, desc, default))

new_opts = ['<h2 id="reference-new">Options added in 1.0</h2>\n'
 '<p class="muted">The seven new sections are on by default in every colour scheme. Set them to '
 '<code>0</code> if you want the page pisg wrote before 1.0. See the '
 '<a href="changelog.html#v1.0-upgrading">upgrade notes</a>.</p>\n']

new_opts.append(opt('ShowOverview', 'ShowOverview &mdash; the channel overview section',
 '&lt;set ShowOverview="1"&gt;',
 'Shows the <code>Channel overview</code> section at the top of the page: one headline sentence '
 '(lines, nicks, days) and the key facts &mdash; words, lines per day, busiest and quietest hour, '
 'questions asked, links shared, top talker, joins and kicks.', '1'))

new_opts.append(opt('ShowRelations', 'ShowRelations &mdash; who talks to whom',
 '&lt;set ShowRelations="1"&gt;',
 'Shows three sections built from the same data: the interactive <code>Who talks to whom</code> map, '
 '<code>Closest pairs</code>, and <code>Social roles</code> (most talked to, most outgoing, connector, '
 'best listener, lone wolf). A connection is counted when a line starts with someone\'s nick, mentions '
 'it, or is a quick reply to them. Nicks marked <code>sex="b"</code> or <code>ignore="y"</code> are '
 'treated as bots and left out. The map needs JavaScript; the two tables do not.', '1'))

new_opts.append(opt('RelationNicks', 'RelationNicks &mdash; how many nicks the map shows',
 '&lt;set RelationNicks="30"&gt;',
 'The number of nicks drawn in the relation map, most active first. Beyond about 40 the map gets hard '
 'to read on a laptop screen; the tables below it are not affected.', '30'))

new_opts.append(opt('RelationMinWeight', 'RelationMinWeight &mdash; the weakest link worth drawing',
 '&lt;set RelationMinWeight="3"&gt;',
 'How strong a connection has to be before a line is drawn between two nicks. Raise it on a very busy '
 'channel where everyone has said something to everyone.', '3'))

new_opts.append(opt('ShowTimePersonalities', 'ShowTimePersonalities &mdash; who owns which part of the day',
 '&lt;set ShowTimePersonalities="1"&gt;',
 'Shows the <code>Time personalities</code> section: the night owls (0&ndash;5h), early birds '
 '(6&ndash;11h), afternoon regulars (12&ndash;17h) and evening regulars (18&ndash;23h), with the share '
 'of each person\'s own lines that falls in that window.', '1'))

new_opts.append(opt('ShowConcentration', 'ShowConcentration &mdash; who carries the channel',
 '&lt;set ShowConcentration="1"&gt;',
 'Shows how much of the talking comes from the top 1, 3, 5, 10 and 20 nicks, and how few people it '
 'takes to account for half of all lines.', '1'))

new_opts.append(opt('ShowSignatureWords', 'ShowSignatureWords &mdash; everyone\'s own word',
 '&lt;set ShowSignatureWords="1"&gt;',
 'Shows the word each regular uses a lot and hardly anybody else does, with how many times they used '
 'it and what share of all its uses that is. Words filtered by <a href="#IgnoreWords">IgnoreWords</a> '
 'and shorter than <a href="#WordLength">WordLength</a> are not considered.', '1'))

new_opts.append(opt('ShowNavBar', 'ShowNavBar &mdash; section navigation',
 '&lt;set ShowNavBar="1"&gt;',
 'Adds the section menu: a fixed list down the left on screens 1000&nbsp;px and wider, and a slim bar '
 'with a <code>Sections</code> button on narrower ones. The bar is plain HTML and works with '
 'JavaScript off; JavaScript only adds the marker that follows the section you are reading.', '1'))

new_opts.append(opt('HomeLink', 'HomeLink &mdash; the &ldquo;All channels&rdquo; button',
 '&lt;set HomeLink="index.html"&gt;\n&lt;set HomeLink="https://example.org/stats/"&gt;',
 'Puts an <code>&larr; All channels</code> button above the page title, pointing at your '
 '<a href="#ChannelIndex">landing page</a>. A plain relative <code>.html</code> path or an http(s) '
 'address. Empty, or <code>none</code>, means no button &mdash; which is what you want if you only '
 'publish one channel.', 'Unset'))

new_opts.append(opt('BadUrls', 'BadUrls &mdash; keep URLs out of the URL statistics',
 '&lt;set BadUrls="postimg.cc/* tinyurl.com/* /ads/"&gt;',
 'A space separated list of patterns. A URL is left out of <code>Most referenced URLs</code> if any '
 'pattern matches anywhere in it, case insensitively; <code>*</code> and <code>?</code> work as '
 'wildcards. This is the blunt instrument for image hosts, tracking links and spam. To drop one exact '
 'address instead, use <code>&lt;link url="..." ignore="y"&gt;</code> &mdash; see '
 '<a href="#ignoring-links">Ignoring links</a>.', 'Unset'))

new_opts.append(opt('ChannelIndex', 'ChannelIndex &mdash; the file the landing page reads',
 '&lt;set ChannelIndex="channels.json"&gt;\n&lt;set ChannelIndex="none"&gt;',
 'pisg writes a small JSON file next to your pages holding one entry per channel: name, network, file, '
 'lines, words, nicks, days, joins, questions, links, the 24-hour profile, the last 30 days and the '
 'five busiest nicks. <code>site/index.html</code> from the distribution reads it and needs nothing '
 'else &mdash; no PHP, no database. <code>none</code> switches it off. Needs <code>JSON::PP</code>, '
 'which is part of core Perl.', 'channels.json'))

new_opts.append(opt('ShareStats', 'ShareStats &mdash; opt-in listing of your page',
 '&lt;set ShareStats="preview"&gt;\n&lt;set ShareStats="1"&gt;',
 'Off unless you turn it on. When on, pisg submits the entry described by <a href="#ShareLink">'
 'ShareLink</a> &mdash; the page address, the maintainer name and the network &mdash; so your channel '
 'can be listed publicly. Nothing from your logs is ever sent. <code>preview</code> prints exactly '
 'what would be sent and sends nothing, which is the setting to try first.', '0'))

new_opts.append(opt('ShareLink', 'ShareLink, ShareWebhook &mdash; what gets shared, and where',
 '&lt;set ShareLink="https://example.org/stats/nightshift.html"&gt;\n'
 '&lt;set ShareWebhook="https://example.org/hooks/pisg"&gt;',
 '<code>ShareLink</code> is the public address of the page the shared entry should point at; without '
 'it there is nothing useful to share. <code>ShareWebhook</code> optionally posts the same entry to a '
 'URL of your own, which is how you feed a channel list or a bot of your own. Both do nothing while '
 '<a href="#ShareStats">ShareStats</a> is off.', 'Unset'))

new_opts = ''.join(new_opts)

body = body.replace('<h2 id="reference-pictures">Picture options</h2>',
                    new_opts + '<h2 id="reference-pictures">Picture options</h2>')

# --------------------------------------------------------------------------
# 3. the optional tools, inserted before the example config
# --------------------------------------------------------------------------

tools = u'''<h2 id="tools">Optional tools</h2>
<p class="muted">None of these are needed to run pisg. They live in <code>scripts/</code> and each one
solves something that otherwise means editing config files by hand. Every one of them refuses to
overwrite work you did yourself.</p>

<h3 id="tool-eggdrop">eggdrop-pisg.tcl &mdash; profiles people manage from IRC</h3>
<p>A Tcl script for an <a href="https://www.eggheads.org/">eggdrop</a> (Tcl 8.6) that lets the people in
your channel set their own <code>&lt;user&gt;</code> options, so you do not have to. The bot writes a
config file; pisg reads it:</p>
<pre>&lt;include="users.cfg"&gt;</pre>
<p>Nothing is stored inside pisg itself, and the file is plain text you can read and edit. Commands work
in the channel with <code>!</code> and in a private message without it:</p>
<div class="tablewrap">
<table>
<thead><tr><th>Command</th><th>What it does</th></tr></thead>
<tbody>
<tr><td><code>!pisghelp [command]</code></td><td>Explains the commands, one at a time.</td></tr>
<tr><td><code>!pisginfo</code></td><td>Set your sex, your picture and your link.</td></tr>
<tr><td><code>!pisgmerge</code></td><td>Count another of your nicks as the same person.</td></tr>
<tr><td><code>!pisgunmerge</code></td><td>Undo that.</td></tr>
<tr><td><code>!pisgshow</code></td><td>Show what the bot has stored for you.</td></tr>
<tr><td><code>!pisgdel</code></td><td>Delete your own entry.</td></tr>
<tr><td><code>!pisgdeluser</code></td><td>Delete somebody else's entry. Bot masters only.</td></tr>
<tr><td><code>!pisgstats</code></td><td>Reply with the address of the stats page. Open to everyone.</td></tr>
</tbody>
</table>
</div>
<p>The rules it enforces, so that opening this up is safe:</p>
<ul>
  <li>People are identified by their <strong>network account</strong> (<code>getaccount</code>, or the
  account host on Undernet), not by the nick they happen to be using.</li>
  <li>Somebody can only claim the nick they are currently using.</li>
  <li>A <code>&lt;user&gt;</code> line <strong>you</strong> wrote by hand can never be overwritten by
  the bot.</li>
  <li>Changes are rate limited.</li>
  <li><code>!pisgstats</code> does not run pisg inside the bot &mdash; it only answers with a link.</li>
</ul>
<p>There is a test suite, <code>eggdrop-pisg-test.tcl</code>, with 107 checks. Run it before you load
the script on a busy bot.</p>

<h3 id="tool-autoalias">pisg-autoalias.py &mdash; merge nicks automatically</h3>
<p>Python 3. On a network with account services, the same person shows up as
<code>nick</code>, <code>nick|afk</code>, <code>nick_</code> and <code>nick2</code> &mdash; but all of
them share one authenticated host, such as <code>*.users.undernet.org</code>. This script reads your
logs, groups nicks by that host, and writes an include file of <code>&lt;user&gt;</code> lines with
aliases. Run it before pisg, from the same cron job.</p>
<pre>python3 scripts/pisg-autoalias.py --logdir logs/nightshift/ --out aliases.cfg</pre>
<pre>&lt;include="aliases.cfg"&gt;</pre>
<p>What it will not do: merge a shared host, a gateway, or a bouncer that several people use; and it
never touches a nick you already described yourself &mdash; your own lines always win. A test suite
ships with it.</p>

<h3 id="tool-adiirc">adiirc2eggdrop.py &mdash; turn client logs into bot logs</h3>
<p>Python 3. You have years of channel history in your client's log folder and a bot that only started
logging last spring. This converts the client logs into the format a bot writes, so the old history can
join the statistics:</p>
<pre>python3 scripts/adiirc2eggdrop.py --in "AdiIRC/logs/#nightshift.log" --out logs/nightshift/
python3 scripts/adiirc2eggdrop.py --in "AdiIRC/logs/#nightshift.log" --out logs/nightshift/ --format znc</pre>
<p><code>--format znc</code> writes what the ZNC log module writes: one file per day, in
<code>energymech</code> format. The rules it follows:</p>
<ul>
  <li>Public channel events only. Private messages, notices and your own server messages are dropped.</li>
  <li>Local timestamps are converted to UTC, which is what bots log in.</li>
  <li>It never overwrites an existing file.</li>
  <li>It stops at the moment your real logging starts, so nothing is counted twice.</li>
</ul>

<h3 id="tool-znc">znc-setup.sh &mdash; let pisg read a ZNC log folder</h3>
<p>Shell. ZNC's logs live under the ZNC user's home directory, and pisg usually runs as somebody else.
This script puts converted logs into the right ZNC account folder and opens up read access to exactly
the channel folders pisg needs &mdash; not the whole home directory.</p>
<pre>scripts/znc-setup.sh --znc-user znc --pisg-user stats --channel '#nightshift'</pre>
<p>It prints everything it intends to do before it changes anything, so you can read the plan first.</p>
<p>Once that is done, read the logs like any other daily-log folder:</p>
<pre>&lt;channel="#nightshift"&gt;
 Format = "energymech"
 LogDir = "/var/lib/znc/moddata/log/nightshift/"
&lt;/channel&gt;</pre>

'''

body = body.replace('<h2 id="example-config">', tools + '<h2 id="example-config">')

# --------------------------------------------------------------------------
# 4. build the table of contents from the ids in the body
# --------------------------------------------------------------------------

GROUPS = []   # [(h2id, h2title, [(id, label, is_opt)])]
token = re.compile(
  r'<h2 id="([^"]+)">(.*?)</h2>'
  r'|<h3 id="([^"]+)">(.*?)</h3>'
  r'|<div class="opt" id="([^"]+)">\s*<h4>([^<\u2014]+)')

for m in token.finditer(body):
    if m.group(1):
        GROUPS.append([m.group(1), re.sub(r'<[^>]+>', '', m.group(2)), []])
    elif m.group(3):
        if GROUPS:
            GROUPS[-1][2].append((m.group(3), re.sub(r'<[^>]+>', '', m.group(4)), False))
    else:
        if GROUPS:
            GROUPS[-1][2].append((m.group(5), m.group(6).strip(), True))

toc = []
for gid, gtitle, kids in GROUPS:
    count = ('<span class="n">%d</span>' % len(kids)) if len(kids) > 3 else ''
    toc.append('  <div class="toc-group">')
    toc.append('    <h2><a href="#%s">%s</a>%s</h2>' % (gid, gtitle, count))
    if kids:
        toc.append('    <ul>')
        for kid, label, is_opt in kids:
            toc.append('      <li><a %shref="#%s">%s</a></li>'
                       % ('class="optlink" ' if is_opt else '', kid, label))
        toc.append('    </ul>')
    toc.append('  </div>')
toc = '\n'.join(toc)

# --------------------------------------------------------------------------
# 5. page shell
# --------------------------------------------------------------------------

PAGE = u'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#0b0e13">
<link rel="canonical" href="https://pisg.github.io/docs.html">
<title>Documentation — pisg</title>
<meta name="description" content="The pisg manual: how to install it, how to write pisg.cfg, and what every single option does — including the options added in 1.0.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%230d1117'/><rect x='18' y='52' width='14' height='30' fill='%2358a6ff'/><rect x='38' y='34' width='14' height='48' fill='%233fd18b'/><rect x='58' y='44' width='14' height='38' fill='%23e5b567'/><rect x='78' y='24' width='14' height='58' fill='%23bc8cff'/></svg>">
<link rel="stylesheet" href="assets/site.css">
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a>

<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="pisg — home">
      <span><span class="dollar">$</span>&nbsp;pisg</span>
      <span class="ver">1.0</span>
    </a>
    <button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="navlinks"><span aria-hidden="true">&#9776;</span><span class="sr-only">Menu</span></button>
    <nav class="links" id="navlinks" aria-label="Main">
      <a href="index.html">Home</a>
      <a href="index.html#install">Install</a>
      <a href="index.html#themes">Themes</a>
      <a href="docs.html" aria-current="page">Documentation</a>
      <a href="changelog.html">Changelog</a>
      <span class="sep" aria-hidden="true"></span>
      <a class="ext" href="demo/">Live example &#8599;</a>
      <a class="x-reg" href="https://github.com/PISG/pisg">GitHub &#8599;</a>
    </nav>
  </div>
</header>

<div style="border-bottom:1px solid var(--border);background:var(--bg2);padding:44px 0 40px">
  <div class="wrap">
    <p class="kicker">Documentation</p>
    <h2>The pisg manual.</h2>
    <p class="lede">How to set pisg up, how to write <code>pisg.cfg</code>, and what every option does.
    This page covers pisg 1.0 and everything in it applies to 0.73 as well, except where an option is
    marked <span class="since">1.0</span>. The same text ships with the distribution as
    <code>docs/pisg-doc.html</code>.</p>
    <div class="cta-row">
      <a class="btn" href="#setting-up-pisg">Set up pisg</a>
      <a class="btn" href="#reference">Option reference</a>
      <a class="btn" href="#reference-new">New in 1.0</a>
      <a class="btn" href="#example-config">Full example config</a>
    </div>
  </div>
</div>

<main id="main" tabindex="-1">
<div class="wrap docs">

<details class="docs-toc" id="docs-toc" open>
<summary>Contents</summary>
<div class="toc-body">
  <div class="toc-search">
    <label class="sr-only" for="toc-filter">Filter the contents</label>
    <input id="toc-filter" type="search" placeholder="Filter options&hellip;" autocomplete="off" spellcheck="false">
    <kbd>/</kbd>
  </div>
  <p class="toc-none" id="toc-none" hidden>Nothing matches that.</p>
@@TOC@@
</div>
</details>

<div class="docs-body">
@@BODY@@
<p class="backtop"><a href="#top">&uarr; Back to top</a></p>
</div>

</div>
</main>

<footer class="site">
  <div class="wrap">
    <div class="foot-bottom" style="border-top:0;padding-top:0">
      <span class="foot-mark"><span style="color:var(--accent)">$</span> pisg 1.0 &mdash; GPL-2.0-or-later</span>
      <span><a href="index.html">Home</a> &middot; <a href="privacy.html">Privacy</a> &middot;
      <a href="cookies.html">Cookies</a> &middot; <a href="terms.html">Terms</a></span>
    </div>
  </div>
</footer>

<script src="assets/site.js"></script>
</body>
</html>
'''.replace('@@TOC@@', toc).replace('@@BODY@@', body)

io.open(OUT, 'w', encoding='utf-8', newline='\n').write(PAGE)
print('wrote', OUT, len(PAGE), 'bytes,', len(GROUPS), 'groups')
for g in GROUPS:
    print('  %-22s %s (%d)' % (g[0], g[1], len(g[2])))
