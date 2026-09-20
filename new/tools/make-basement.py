# -*- coding: utf-8 -*-
"""
Second example channel: a small, chatty room with user pictures.
Same idea as build_demo.py — real pisg 1.0 output, invented people.
"""
import io, re, json

SRC = r'C:\Users\admin\Desktop\output\canada.html'
DST = r'C:\Users\admin\Desktop\Github\pisg.github.io\new\demo\basement.html'

h = io.open(SRC, encoding='utf-8', errors='replace').read()

# ---------------------------------------------------------------------------
# people.  Two nicks (BeanCounter, okra) are deliberately the same as in
# #nightshift: on a real network the same people turn up in both channels.
# ---------------------------------------------------------------------------
MAP = {
    'Agent': 'Ledger', 'Seb': 'vox', 'alakon': 'lantern', 'DUT': 'dux',
    'LateDogg': 'BeanCounter', 'LateDogg_YS': 'BeanCounter_YS',
    'Adacic1033': 'Bartok1033', 'AdaCiC1033_': 'BarTok1033_',
    'JustaPsychic': 'JustaTypist', 'PiMp0r_': 'PiXel0r_', 'mihaivzr': 'pilotvzr',
    '[Canada]': '[Basement]', 'Danny': 'Bobbin', 'Danny____aJ': 'Bobbin____aJ',
    'Danny2_': 'Bobbin2_', 'Danny2': 'Bobbin2', 'Danny-': 'Bobbin-', 'D4nny': 'B0bbin',
    'OwnerNB': 'OwnerNB', 'God29': 'God29',
    'ikce': 'okra', 'ikce-av': 'okra-av', 'ikce-gl': 'okra-gl', 'ikce-Ul': 'okra-Ul',
    'ikce-lV': 'okra-lV', 'ikce-qI': 'okra-qI', 'ikce-vu': 'okra-vu',
    'ikce-kids-Su': 'okra-kids-Su',
    'cicada3301': 'sundial3301', 'cicada3301__': 'sundial3301__',
    'jakob-_': 'jitter-_', 'VegasBlack': 'VelvetBlack', 'Serbian': 'Sundowner',
    'humility': 'humbug', 'BuhBye|': 'ByeNow|', 'dark\\s|de': 'sable\\s|de',
    'cna_': 'cnc_', 'Tezz': 'Tozz', 'TEZ': 'TOZ', 'Th3^On3': 'Th3^0th3r',
    'Slipknot-': 'Sidecar-', 'zas': 'zax', 'Aces304': 'Acorn304',
    'burnout': 'brownout', 'ARICIU2K': 'ARCANE2K', 'Isa': 'Iris', 'Hans': 'Hank',
    'Pipes': 'Pylon', 'Jamie': 'Jinx', 'loomer': 'looper', 'offGuard': 'onGuard',
    'favouritecar': 'favouritebike', 'kaustic': 'kelpie', 'StatiK': 'Cobble',
    'garslaitte': 'oatmealstout', 'MrPresident': 'MrChairman',
    'MrPresident6': 'MrChairman6', 'AlexMontreal': 'AlexTheTall',
    'debileprofon': 'dizzyprofon', 'haldolhahaha': 'halliehahaha',
    'MartyMcFly': 'MartyMcFlea', 'Tel_efon': 'Tel_ephon', 'Secoupe': 'Saucer',
    'Eklezys': 'Eklipsis', 'Kalibro': 'Kaliber', 'gorkule': 'gherkin',
    'chine`': 'chime`', 'slave_lin': 'sleeve_lin', 'vitaltigerBr': 'vividTigerBr',
    'nhlbg': 'leaguebg', 'Jimboray': 'Jamboray', 'birthday': 'birthday',
    'aStory': 'aStory', 'Turbo_': 'Turbo_', 'burnout_': 'brownout_',
    # nickname families
    'ZaPsTeRman': 'ZigZagMan', 'ZAPziesMan': 'ZigZiesMan', 'ZAPziesMAn': 'ZigZiesMAn',
    'THE_ZAPSTER': 'THE_ZIGSTER', 'KRAXTERman': 'KRUXTERman',
    'CRACKSTERman': 'CRUXTERman', 'ICRACKSTmydk': 'ICRACKEDmydb',
    'JESUS': 'JEEVES', 'NOTinTheASS': 'NOTinTheOFFICE',
    'NINEintheASS': 'NINEintheMORNING', 'Hey_HOMO': 'Hey_HELLO',
    'BIbeMAn': 'BIkeMAn', 'PENISrick': 'PEONYrick', 'CRISSEman': 'CRIKEYman',
    'TABRNACLEman': 'TAMBOURINEman', 'MEOWmixMAn': 'MEOWmixMAn', 'MEOWman': 'MEOWman',
    'CrkstrDsnowm': 'CrkstrDsnowm', 'CrkStrSnoman': 'CrkStrSnoman',
    'Xtreemdude': 'Xtreemdude',
    'Ry': 'Rye', 'Rybsd': 'Ryebsd', 'pUnk`BSD': 'pUnk`BSD', 'pUnk`37': 'pUnk`37',
    'JoK3-[1]': 'JoK3-[1]', '[RY][B][S][D': '[RY][E][S][D', '[R][Y][B][S]': '[R][Y][E][S]',
    'Xcarton': 'Xcartoon', 'WyxeMan': 'WyxeMan', 'x_corky': 'x_corky',
    'creton': 'crouton', 'xT-70': 'xT-70', 'carton': 'cartoon',
    'LeMacaque': 'LeMacaw', 'Dolly_Fan': 'Dolly_Fan', 'vikce': 'vokra',
    'YouDied': 'YouDied',
}

# ---------------------------------------------------------------------------
# what they said
# ---------------------------------------------------------------------------
QUOTES = [
    '[a] &gt; Missed.   [missed: -1 xp]',
    ' the good chair is load bearing, do not move it',
    'nobody picked the winner, they picked the loudest',
    'mornin! o/',
    'round two, same as round one',
    'I am simply electric today',
    '(-___- )',
    '!RELOAD',
    '-.,&#184;&#184;.-&#183;&#176;\'`\'&#176;&#183;-.,&#184;&#184;.-&#183;&#176;\'`\'...',
    'Basement humidity up again, blame the dryer ve...',
]

WORDS = [                       # most used words, in page order
    ('QUACK', 'QUACK'), ('escapes', 'escapes'), ('laval', 'thermos'),
    ('enfants', 'blanket'), ('golden', 'golden'), ('jeunes', 'mittens'),
    ('Serco', 'kettle'), ('p\u00e8re', 'laundry'),
    ('com/a/y7nE7qI', 'thursday'), ('habite', 'postcard'),
]

SIGWORDS = [                    # signature words, in page order
    ('lockdown', 'lockdown'), ('marde', 'blimey'), ('matin', 'mornin'),
    ('duckstats', 'duckstats'), ('tar\u00e9', 'bonkers'), ('gonna', 'gonna'),
    ('situation', 'situation'), ('cesar_', 'tinsel_'), ('account', 'account'),
    ('timeline', 'timeline'), ('\u0432\u0435\u0447\u0435', '\u0432\u0435\u0447\u0435'),
    ('ahaha', 'ahaha'),
]

URLS = [
    ('https://postimg.cc/4nY30bSq', 'https://0x0.st/paint-chip.png'),
    ('https://postimg.cc/rdLPyx6p', 'https://0x0.st/bench-plan.png'),
    ('https://undernet.xyz/', 'https://github.com/PISG/pisg'),
    ('https://undernet.xyz', 'https://github.com/PISG/pisg'),
]

TEXT = [
    # topics
    ('Welcome to the official channel of Canada \u2022 Bienvenue dans le canal officiel du Canada',
     'Welcome to #basement \u2022 the room with the good chair \u2022 quiet after midnight, mostly'),
    ('(DUT) * Bonne F\u00eate du Canada!/Happy Canada Day! *',
     '(dux) * the shelf is up. the shelf is UP. *'),
    ('(DUT) * Bonne F\u00eate du Canada/Happy Canada Day *',
     '(dux) * shelf day, everyone. shelf day. *'),
    # the kick reason
    ('((Seb) Ton s\u00e9jour avec nous ce termine ici, je suis tanner de te voir beg, pis agir comme un '
     'enfant immature. Tu attire le trouble, tu attire les floodbots. Ceci est permanant. Bonne chance '
     'dans la vie.)',
     '((vox) that is enough for tonight. Come back when you have slept, and leave the floodbots at home.)'),
    # examples
    ('* Th3^On3 goodday!', '* Th3^0th3r puts the kettle on'),
    ('pisg</a> v1.0.a', 'pisg</a> v1.0'),
]

# user pictures: the source page links to the maintainer's own image host.
# Swap them for two inline placeholders, so the demo makes no outside requests.
AVATAR_DEF = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E"
              "%3Crect width='60' height='60' rx='8' fill='%23dfe3ea'/%3E"
              "%3Ccircle cx='30' cy='23' r='9' fill='%23aab3c0'/%3E"
              "%3Cpath d='M12 56c2-11 9-16 18-16s16 5 18 16z' fill='%23aab3c0'/%3E%3C/svg%3E")
AVATAR_VOX = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E"
              "%3Crect width='60' height='60' rx='8' fill='%230d1117'/%3E"
              "%3Ctext x='30' y='39' font-family='monospace' font-size='26' font-weight='700' "
              "text-anchor='middle' fill='%233fd18b'%3Evx%3C/text%3E%3C/svg%3E")

# ---------------------------------------------------------------------------
# relation map data
# ---------------------------------------------------------------------------
m = re.search(r'(<script type="application/json" id="relmap-data">)(.*?)(</script>)', h, re.S)
data = json.loads(m.group(2))
for node in data['nodes']:
    node['id'] = MAP.get(node['id'], node['id'])
    node['partners'] = [[MAP.get(p, p), w] for p, w in node['partners']]
h = h[:m.start(2)] + json.dumps(data, separators=(',', ':'), sort_keys=True,
                                ensure_ascii=False) + h[m.end(2):]

# ---------------------------------------------------------------------------
# free text first
# ---------------------------------------------------------------------------
qi = [0]
def _q(match):
    i = qi[0]; qi[0] += 1
    return match.group(1) + (QUOTES[i] if i < len(QUOTES) else QUOTES[-1]) + match.group(2)
h = re.sub(r'(class="quote">")(?:.*?)("</td>)', _q, h)

for old, new in TEXT:
    h = h.replace(old, new)

# the two Canada Day topics carry mIRC control characters around the asterisks
h = re.sub(r'\(DUT\)[^<]*Canada Day![^<]*',
           '(dux) * the shelf is up. the shelf is UP. *', h)
h = re.sub(r'\(DUT\)[^<]*Canada Day[^<]*',
           '(dux) * shelf day, everyone. shelf day. *', h)
for old, new in URLS:
    h = h.replace(old, new)

def cell(old, new, text):
    return text.replace('>' + old + '<', '>' + new + '<', 1)
for old, new in WORDS + SIGWORDS:
    if old != new:
        h = cell(old, new, h)

# the ASCII-art uppercase example keeps its shape, only the nick changes (done below)

h = h.replace('https://r2.fivemanage.com/X8I0LGoLdHY2Wx9DdTrvx/Pics/me.png', AVATAR_VOX)
h = h.replace('https://r2.fivemanage.com/X8I0LGoLdHY2Wx9DdTrvx/Pics/basic.png', AVATAR_DEF)

# ---------------------------------------------------------------------------
# nicks
# ---------------------------------------------------------------------------
NICKCH = r'A-Za-z0-9_\[\]\\|`\^\-'
for old in sorted(MAP, key=len, reverse=True):
    new = MAP[old]
    if old == new:
        continue
    pat = r'(?<![%s])%s(?![%s])' % (NICKCH, re.escape(old), NICKCH)
    h = re.sub(pat, new.replace('\\', '\\\\'), h)

# ---------------------------------------------------------------------------
# the channel
# ---------------------------------------------------------------------------
h = h.replace('#Canada', '#basement').replace('#canada', '#basement')

h = h.replace(
  '<nav class="pisg-nav"',
  '<p class="subtitle" style="max-width:74ch;margin:0 auto 6px">'
  '<em>Example page for <a href="../index.html">pisg.github.io</a> &mdash; a small channel, with user '
  'pictures switched on. The channel, the people and everything they say here are invented; the numbers '
  'and the layout are a real pisg run.</em></p>\n'
  '<nav class="pisg-nav"', 1)

io.open(DST, 'w', encoding='utf-8', newline='\n').write(h)
print('wrote', DST, len(h), 'bytes')

left = [o for o in MAP if o != MAP[o]
        and re.search(r'(?<![%s])%s(?![%s])' % (NICKCH, re.escape(o), NICKCH), h)]
print('leftover source nicks:', left or 'none')
for bad in ('fivemanage', 'postimg', 'Canada', 'undernet.xyz', 'v1.0.a'):
    if bad in h:
        print('  still present:', bad)
