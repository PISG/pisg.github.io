# -*- coding: utf-8 -*-
"""
Build the example stats page for the site out of a real pisg 1.0 page.

The markup, the CSS, the graphs and the relation-map script are exactly what pisg wrote.
Everything that identifies a person or repeats what they said is replaced: nicks, quotes,
example lines, words, URLs, topics and the channel itself. The numbers are left alone, so
the page still behaves like a real one at real scale.
"""
import io, re, json, os, sys

SRC = r'C:\Users\admin\Desktop\output\montreal.html'
DST = r'C:\Users\admin\Desktop\Github\pisg.github.io\new\demo\nightshift.html'

h = io.open(SRC, encoding='utf-8', errors='replace').read()

# ---------------------------------------------------------------------------
# 1. who the invented people are.  Top 30 first, in the page's own order.
# ---------------------------------------------------------------------------
NICKS = [
    ('Kendrick', 'helix'), ('LateDogg', 'BeanCounter'), ('dark\\side', 'sable\\side'),
    ('mmk', 'nn'), ('ikce', 'okra'), ('perruche', 'kestrel'), ('J[a]zzy', 'Br[i]xie'),
    ('Elyse-', 'Margo-'), ('CowPokPifPaf', 'DialUpDinosaur'), ('asm-', 'tilde-'),
    ('Tamarack', 'Sputnik'), ('TroubleMaker', 'QuietRiot'), ('PaNDhors', 'PopTart'),
    ('GSTARR', 'Ferrite'), ('GOa_uLD', 'Vela_Rx'), ('JWales', 'Grommet'),
    ('P0ULET', 'W0MBAT'), ('_X_', '_zeph_'), ('SiD`', 'mux`'), ('Simon', 'Calliope'),
    ('plume', 'bramble'), ('garslaitte', 'oatmealstout'), ('`^AN|M4L^`', '`^SN|ORK^`'),
    ('stvenouellet', 'jenspenwriter'), ('integra', 'cinder'), ('GabBonbon', 'GlibGlob'),
    ('Core9224', 'Node9224'), ('alxd', 'rasp'), ('MTL', 'YUL'), ('juan-', 'yarrow-'),
]

# variants and everybody else the page names once or twice
EXTRA = [
    ('GSTARR_', 'Ferrite_'), ('MTLz', 'YULz'), ('juan_', 'yarrow_'), ('juan', 'yarrow'),
    ('ikce_', 'okra_'), ('Tamarack__', 'Sputnik__'), ('doomm', 'driveljar'),
    ('tony2-', 'stilt2-'), ('VeNoNa-', 'Pemmican-'), ('Azriel____rP', 'Rambleford____rP'),
    ('OpodboqO', 'WhatnowWho'), ('jONYbLAzE', 'aSKiNGaGAIN'), ('Intel|ika', 'Klaxon|ika'),
    ('SLAPcorp', 'CAPScorp'), ('alxdandra', 'raspberry_pi3'), ('DANOU44|3', 'TINCAN44|3'),
    ('NomorePTer', 'GloomBucket'), ('CCR', 'Moss'), ('ZaPsTeRman', 'ZigZagMan'),
    ('StatiK', 'Cobble'), ('Core3757', 'Node3757'), ('cruisader', 'whiskbroom'),
    ('akimbo', 'hexed'), ('tpoi', 'spool'), ('Dan_', 'Pockets_'), ('yoooyoyo', 'heyheyhey'),
    ('Reid', 'Quartz'), ('FanoBottomRS', 'FerryDockRS'), ('AbZaure', 'AbAcus'),
    ('voidah', 'jitterbug'), ('alain', 'ripple'), ('|KaBoOm|', '|KaBoOm|'),
    ('AminoAcid', 'AminoAcid'), ('mdr_6510', 'nn_6510'), ('Moderateur', 'Curfew'),
    ('simon_23', 'Calliope_23'), ('simon_', 'Calliope_'),
    ('GGhy88', 'Toastie88'), ('distributed_', 'clockwork_'), ('justin51', 'lantern51'),
    ('SS-012', 'NS-012'), ('CA_SE_POURRA', 'IT_WILL_KEEP'), ('Nomore', 'Nomore'),
    ('GobLeCrob', 'GrubbleCrumb'), ('TUPAC43', 'TUBA43'), ('Irccloud__', 'Irccloud__'),
    ('weechat_02', 'weechat_02'), ('LadyBot', 'LadyBot'),
    # alias families listed in "Users with most nicknames"
    ('carton', 'cartoon'), ('creton', 'crouton'), ('xObiWan', 'xOkraWan'),
    ('x_corky', 'x_corky'), ('xQuiGon', 'xQuietGon'), ('X_unit', 'X_unit'),
    ('chatte', 'chatter'), ('ikc[e]', 'okr[a]'), ('ikse', 'okse'), ('YouDied', 'YouDied'),
    ('ZaPPsTERRMan', 'ZiGGsTERRMan'), ('ZaPsTERRMann', 'ZiGsTERRMann'),
    ('ZaPsTERRMan', 'ZiGsTERRMan'), ('Xtreemdude', 'Xtreemdude'),
    ('Hey_HOMO', 'Hey_HELLO'), ('SSATANN', 'SSANDMANN'), ('ERECTEDpENIS', 'ELECTEDpRESS'),
    ('NOTinTheASS', 'NOTinTheOFFICE'), ('NINEintheASS', 'NINEintheMORNING'),
    ('PasMalBlatte', 'NotBadBeetle'), ('Coquerelle', 'Cockroach'),
    ('DrHouse1Pedo', 'DrHouse1Fan'), ('Super-Poulet', 'Super-Wombat'),
    ('Poulet_', 'Wombat_'), ('Demi-Poulet', 'Demi-Wombat'), ('Poulet', 'Wombat'),
    ('Cock`r`il', 'Cock`r`il'), ('Caffard', 'Beetle'),
    ('mombituZ', 'pebbleZ'), ('chien', 'hound'), ('Patof', 'Patof'), ('Meo', 'Meo'),
    ('mombitu', 'pebble'), ('Chatton', 'Kitten'), ('MenCaliss', 'OhBother'),
    ('bubblefart', 'bubblewrap'), ('Core7489', 'Node7489'), ('joubert', 'joubert'),
    ('tabarnac', 'blimey'), ('Core7935', 'Node7935'), ('whatthefuck', 'whatonearth'),
    ('joob', 'joob'), ('calisse', 'crikey'),
]

MAP = dict(NICKS + EXTRA)
NEW = dict(NICKS)          # top-30 only, for regenerated content

CHANNEL_OLD, CHANNEL_NEW = '#montreal', '#nightshift'
MAINT_OLD, MAINT_NEW = 'Seb', 'vox'

# ---------------------------------------------------------------------------
# 2. free text: quotes, example lines, words, URLs, topics
# ---------------------------------------------------------------------------
QUOTES = [                                   # in the page's own order, top 10
    'no, the other server, not this one',
    '-- and that, folks, is a coincidence --',
    'my uptime is older than this channel',
    'Buddy Rich - Big Swing Face',
    'meh, ship it and go to bed',
    'kestrel: eat something, it is 4am',
    'okra: can I pm you about the log parser?',
    'how are you holding up, kestrel?',
    'so I went and bought the wrong cable. again.',
    'namaste, night crew',
]

EXAMPLES = [
    ('&lt;SLAPcorp&gt; I BEAT YOU !!!', '&lt;CAPScorp&gt; I FIXED IT !!!'),
    ('* J[a]zz slaps joob', '* Br[i]xie slaps joob'),
    ('&lt;|KaBoOm|&gt; fuck pk personne me parle',
     '&lt;|KaBoOm|&gt; oh for f**ks sake, the bouncer died again'),
    ('</a> v1.0.a', '</a> v1.0a'),
]

WORDS = [                                    # (old, new) most used words
    ("c'est", 'because'), ('faire', 'anyway'), ('comme', 'coffee'), ('quand', 'tonight'),
    ('juste', 'really'), ('aussi', 'actually'), ('monde', 'tomorrow'), ('toute', 'people'),
    ('encore', 'kernel'), ('youtube', 'youtube'),
]

URLS = [
    ('https://youtu.be/0pGOFX1D_jg?si=gkMXX8bzDd0TlQFc', 'https://archive.org/details/78_night-shift'),
    ('https://www.dixieleefriedchicken.com', 'https://en.wikipedia.org/wiki/Aurora'),
    ('https://youtu.be/kuMHuWcXdss?si=ZxCVd8ftIl0uYUgC', 'https://xkcd.com/2347/'),
    ('https://www.youtube.com/watch?v=gwNQqnEYMXw', 'https://www.gnu.org/software/screen/'),
    ('https://bien-etre.social', 'https://tildes.net'),
]

SIGWORDS = [                                 # (old, new) signature words, in page order
    ('êᴛᴇs-ᴠᴏᴜs', 'ᴀɴʏᴏɴᴇ-ᴀʀᴏᴜɴᴅ'),
    ('nwers', 'graveyards'), ('beauce', 'basement'),
    ('mouer', 'meh'), ('lexus', 'forklift'), ('paske', 'cuz'), ('image', 'diagram'),
    ('accord', 'agreed'), ('estie', 'blimey'), ('yeules', 'earbuds'),
    ('lawll', 'lolol'), ('jajajaja', 'hahahaha'), ('héhé', 'heheh'),
    ('c’est', 'it’s'), ('states', 'timezones'),
]

TOPIC_OLD = 'Attention à la marche !'
TOPIC_NEW = 'mind the gap | quiet hours are a rumour | stats: /stats'

AVATAR_DEF = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E"
              "%3Crect width='60' height='60' rx='8' fill='%23dfe3ea'/%3E"
              "%3Ccircle cx='30' cy='23' r='9' fill='%23aab3c0'/%3E"
              "%3Cpath d='M12 56c2-11 9-16 18-16s16 5 18 16z' fill='%23aab3c0'/%3E%3C/svg%3E")

# ---------------------------------------------------------------------------
# 3. rewrite the relation-map data with the new nicks
# ---------------------------------------------------------------------------
m = re.search(r'(<script type="application/json" id="relmap-data">)(.*?)(</script>)', h, re.S)
data = json.loads(m.group(2))
for node in data['nodes']:
    node['id'] = MAP.get(node['id'], node['id'])
    node['partners'] = [[MAP.get(p, p), w] for p, w in node['partners']]
newjson = json.dumps(data, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
h = h[:m.start(2)] + newjson + h[m.end(2):]

# ---------------------------------------------------------------------------
# 4. free-text replacements (before the nick pass, so nicks inside them follow)
# ---------------------------------------------------------------------------
# random quotes in the "most active nicks" table
qi = [0]
def _q(match):
    i = qi[0]; qi[0] += 1
    return match.group(1) + (QUOTES[i] if i < len(QUOTES) else QUOTES[-1]) + match.group(3)
h = re.sub(r'(class="quote">&quot;|class="quote">")(.*?)(&quot;</td>|"</td>)', _q, h)

for old, new in EXAMPLES:
    h = h.replace(old, new)

# most used words / signature words / URLs: replace the cell contents only
def cell(old, new, text):
    """Replace >old< with >new< the first time it appears as a whole table cell."""
    return text.replace('>' + old + '<', '>' + new + '<', 1)

for old, new in WORDS + SIGWORDS:
    h = cell(old, new, h)

# the first signature word is stored in NFD form in the source page; catch it by position
h = re.sub(r'(class="hicell sigword">)[^<]+(</td>)',
           lambda m: m.group(1) + SIGWORDS[0][1] + m.group(2), h, count=1)
for old, new in URLS:
    h = h.replace(old, new)

h = h.replace(TOPIC_OLD, TOPIC_NEW)

# user pictures: the source page links to the maintainer's own image host.
# Swap them for an inline placeholder, so the demo makes no outside requests.
h = re.sub(r'https://r2\.fivemanage\.com/[^"]+', AVATAR_DEF, h)

# ---------------------------------------------------------------------------
# 5. the nick pass
# ---------------------------------------------------------------------------
NICKCH = r'A-Za-z0-9_\[\]\\|`\^\-'          # characters a nick may be made of
for old in sorted(MAP, key=len, reverse=True):
    new = MAP[old]
    if old == new:
        continue
    pat = r'(?<![%s])%s(?![%s])' % (NICKCH, re.escape(old), NICKCH)
    h = re.sub(pat, new.replace('\\', '\\\\'), h)

# ---------------------------------------------------------------------------
# 6. the channel itself
# ---------------------------------------------------------------------------
h = h.replace(CHANNEL_OLD, CHANNEL_NEW)
h = h.replace('#nightshift @ Undernet stats by ' + MAINT_OLD,
              '#nightshift @ Undernet stats by ' + MAINT_NEW)

# a line saying what this page is, right under the title, in the page's own voice
h = h.replace(
  '<nav class="pisg-nav"',
  '<p class="subtitle" style="max-width:74ch;margin:0 auto 6px">'
  '<em>Example page for <a href="../index.html">pisg.github.io</a> &mdash; the output of pisg 1.0 '
  'at the scale of a channel that never sleeps. The channel, the people and everything they say here '
  'are invented; the numbers and the layout are a real pisg run.</em></p>\n'
  '<nav class="pisg-nav"', 1)

io.open(DST, 'w', encoding='utf-8', newline='\n').write(h)
print('wrote', DST, len(h), 'bytes')

# ---------------------------------------------------------------------------
# 7. audit: any of the original nicks still in the file?
# ---------------------------------------------------------------------------
left = []
for old in MAP:
    if old == MAP[old]:
        continue
    if re.search(r'(?<![%s])%s(?![%s])' % (NICKCH, re.escape(old), NICKCH), h):
        left.append(old)
print('leftover source nicks:', left or 'none')
