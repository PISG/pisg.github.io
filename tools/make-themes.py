# -*- coding: utf-8 -*-
"""
Theme samples: one stats page per colour scheme, made by pisg 1.0a itself from an invented
channel, #teatime.  Nobody in it is real: the nicks, the lines, the topics and the links are
all written here, and the links all point at example.org / example.com / example.net.

The log is written in eggdrop format, one file per day, into a temporary folder, and pisg is
run once per scheme from the pisg repository checked out next to this one (../pisg).

Output : demo/themes/<scheme>.html
Needs  : perl, and ../pisg
"""
import io, os, random, re, shutil, subprocess, sys, tempfile
from datetime import date, timedelta

SITE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PISG   = os.path.join(os.path.dirname(SITE), 'pisg')
DSTDIR = os.path.join(SITE, 'demo', 'themes')
THEMES = ['modern', 'midnight', 'amoled', 'terminal', 'default']

CHAN  = '#teatime'
START = date(2026, 7, 20)
DAYS  = 62
R = random.Random(2026)

# ---------------------------------------------------------------------------
# the people.  weight = how much they talk; hours = when they are around;
# group = who they mostly talk to; words = what they say that nobody else does
# ---------------------------------------------------------------------------
NIGHT   = [0, 1, 2, 3, 4, 23, 22]
MORNING = [6, 7, 8, 9, 10, 11]
DAY     = [11, 12, 13, 14, 15, 16, 17]
EVENING = [18, 19, 20, 21, 22]
ALL     = list(range(24))

P = {}
def person(nick, weight, hours, group, words=(), ident=None, **traits):
    P[nick] = dict(weight=weight, hours=hours, group=group, words=list(words),
                   ident=ident or nick.lower()[:9], **traits)

person('vox',          60, EVENING + DAY,     'core',   ['anyway', 'right then'], op=True, topic=True)
person('kettle',       55, MORNING + DAY,     'core',   ['brew', 'lovely'], action=True, op=True)
person('humbug',       48, NIGHT + EVENING,   'night',  ['meh', 'ugh'], sad=True, foul=True)
person('Iris',         44, DAY + EVENING,     'core',   ['honestly', 'garden'], smile=True, asks=True, excited=True)
person('Fortuna',      40, EVENING,           'core',   ['luck', 'omens'], asks=True, urls=True)
person('kelpie',       36, NIGHT,             'night',  ['splash', 'tide'], action=True)
person('PoeticGuy',    30, EVENING + NIGHT,   'night',  ['alas', 'verily'], long=True)
person('BigMug44',     34, MORNING,           'morning', ['MUG', 'COFFEE'], shout=True, foul=True)
person('zestyanteater', 22, DAY,              'day',    ['zesty', 'ants'], smile=True)
person('Ledger',       26, DAY,               'day',    ['receipts', 'budget'], asks=True, urls=True, op=True)
person('RamblerBobVa', 24, MORNING + DAY,     'morning', ['trail', 'boots'], long=True, urls=True)
person('crumpet',      28, MORNING,           'morning', ['butter', 'toasty'], smile=True)
person('Pekoe',        20, DAY + EVENING,     'day',    ['leaf', 'steep'])
person('marmalade',    18, EVENING,           'core',   ['sticky', 'orange'], smile=True, excited=True, hits=True)
person('bramble',      16, NIGHT + MORNING,   'night',  ['thorns', 'hedge'], sad=True)
person('Oolong',       15, DAY,               'day',    ['oxidised', 'roast'], asks=True)
person('sconewolf',    14, EVENING + NIGHT,   'night',  ['awoo', 'jam first'], shout=True, excited=True, hits=True)
person('Darjeeling',   13, MORNING,           'morning', ['muscatel', 'first flush'])
person('biscuit',      12, DAY,               'day',    ['dunk', 'crumbs'], smile=True)
person('jammy',        10, EVENING,           'core',   ['dodger', 'sweet'])
person('Nettle',       10, NIGHT,             'night',  ['sting', 'foraging'], urls=True)
person('Hobnob',        9, DAY,               'day',    ['oats', 'sturdy'])
person('Tansy',         9, MORNING + DAY,     'morning', ['seeds', 'compost'], asks=True)
person('Custard',       8, EVENING,           'core',   ['wobbly', 'lumps'], smile=True)
person('quill',         8, NIGHT,             'night',  ['ink', 'draft'], long=True)
person('Barley',        7, DAY,               'day',    ['malt'])
person('Juniper',       7, EVENING,           'core',   ['sprig'])
person('Rooibos',       6, MORNING,           'morning', ['red bush'])
person('Clementine',    6, DAY,               'day',    ['peel'])
person('ottercake',     5, NIGHT,             'night',  ['river'])
person('Figgy',         5, EVENING,           'core',   ['pudding'])
person('Sorrel',        4, DAY,               'day',    ['sour'])
person('teasmade',      4, MORNING,           'morning', ['alarm'])
person('Wren',          3, MORNING,           'morning', ['tiny'])
person('Parsnip',       3, EVENING,           'core',   ['roots'])
person('Muffin',        3, DAY,               'day',    ['blueberry'])
person('dunkworth',     2, NIGHT,             'night',  [])
person('lemoncurd',     2, DAY,               'day',    [])
person('Saffron',       2, EVENING,           'core',   [])
person('Tuppence',      1, MORNING,           'morning', [])

NICKS = list(P)
OPS = [n for n in NICKS if P[n].get('op')]

# ---------------------------------------------------------------------------
# what people say
# ---------------------------------------------------------------------------
LINES = """
morning all
evening everyone
the kettle is on, as always
who wants a cup, I am making a pot
did anyone else get rain today, it has not stopped here since lunch
I finally repotted the tomatoes and they look furious about it
the new bakery on the corner does a cardamom bun that is frankly unreasonable
reading a book about lighthouses, it is better than it has any right to be
my cat has decided the keyboard is a bed again
the train was twenty minutes late and nobody said a word, very civilised
I think the wifi is held together with string at this point
the fox was in the garden again last night, bold as anything
I put too much milk in and now it is basically warm milk with a rumour of tea
spent the whole afternoon untangling fairy lights for no reason
there is a thunderstorm coming, the sky has gone that yellow colour
finished the crossword except for one clue and it is haunting me
the neighbour is mowing the lawn at seven again
I burnt the toast, which is a skill at this point
made soup out of whatever was in the fridge and it was somehow excellent
just back from a walk along the canal, saw a heron being dramatic
my plant has one new leaf and I am unreasonably proud
the library had a sale and I came home with nine books
I keep meaning to go to bed early and then it is two in the morning
the bus driver waved at me, today is a good day
it is far too hot for tea and I am having tea anyway
I have been on hold for forty minutes listening to the same four bars
the power went out for an hour and I rediscovered candles
someone left a whole box of apples on the wall with a sign saying help yourself
I baked bread and it came out the shape of a small country
my sourdough starter is older than some of the people in here
finally fixed the dripping tap, only took three trips to the shop
the market had those tiny strawberries that taste like summer
went to the seaside, got sunburnt, ate chips, no regrets
there is a spider in the bath and we have agreed to share it
the heating came on by itself and I have no idea why
I found a tenner in an old coat, best day of the month
honestly the best thing about autumn is the jumpers
the kids next door are learning the trumpet, all of them, at once
my knitting has become a scarf by accident, it was meant to be a hat
nobody tells you how many socks a washing machine eats
I am going to organise the spice drawer, wish me luck
that storm took out half the fence and all of my patience
I tried the green tea everyone keeps going on about and it tastes like a lawn
you cannot rush a proper pot, three minutes minimum
milk after, obviously, we are not animals
the channel is quiet tonight, everyone must be asleep
brb, the pasta is boiling over
back, the pasta survived, the hob did not
I need a nap and it is only half ten
the sunset tonight was absurd, all pink and orange
somebody on the radio said it will snow in October, I refuse
there is a hedgehog living under the shed, I have named him Gerald
the post came and it was all bills and one postcard from a cousin
made a spreadsheet of my tea collection, I have a problem
the museum has a new exhibit on old maps, going on Saturday
anyone else find that biscuits go soft faster in summer
I just watched a documentary about moss for an hour and I loved it
my bike has a puncture again, the universe is sending a message
I am sure I put my glasses down right here
the café was out of scones, I have never recovered
the allotment is producing more courgettes than any human can eat
I planted too many beans and now they are plotting something
the dog stole a whole croissant off the table and looked delighted
I think I have finally found the perfect mug, it is enormous
there is a queue at the post office that goes out the door
good night all, sleep well
night night
see you tomorrow
lol
haha
that is brilliant
oh no
same here
fair enough
ha, typical
exactly
I know right
not again
oh that is lovely
well that went well
sounds about right
tell me about it
no idea, sorry
bless
""".strip().split('\n')

QUESTIONS = """
anyone around?
has anyone tried the smoky one, the lapsang?
what are you all having for dinner?
is it just me or is the channel really quiet today?
who left the kettle on?
does anyone know a good recipe for ginger biscuits?
how do you stop slugs eating everything?
what time is it over there?
are we still doing the book club thing on Sunday?
did anyone see the moon last night?
where did everyone go?
milk first or milk after, settle this once and for all?
is it too late for a coffee?
what is everyone reading at the moment?
can someone remind me what the topic was about?
why does my bread never rise properly?
anyone fancy a quiz later?
has the rain stopped where you are?
""".strip().split('\n')

SHOUTS = """
WHO TOOK MY MUG
THE KETTLE IS BROKEN
I WON THE RAFFLE
IT IS SNOWING, IN AUGUST
NOBODY TOUCH THE LAST SCONE
GOOD MORNING
THE CAT IS ON THE ROOF AGAIN
""".strip().split('\n')

SAD = """
long day :(
the plant died :(
I missed the bus again :(
rain again, of course :(
the shop was closed :(
""".strip().split('\n')

HAPPY = """
that made my day :)
lovely :)
thanks, you are all great :)
cake has been achieved :D
it worked first time :D
aw :)
""".strip().split('\n')

FOUL = """
oh shit, the scones are burning
well shit, missed the train
the printer is being an absolute shit again
""".strip().split('\n')

LONG = """
I have been thinking about it all day, and I really do believe the best cup of the week is the one on a Sunday morning when nothing needs doing and the rain is on the window and the radio is on low
there is a particular kind of quiet you only get at about four in the morning when the birds have not started yet and the street lights are still humming and the whole town seems to be holding its breath
the thing nobody tells you about gardening is that most of it is waiting, and some of it is weeding, and a very small part of it is standing there with a cup looking at what you did and feeling like a genius
I walked the whole length of the old railway line today, past the bridge and the allotments and the broken signal box, and I did not see a single other person for two hours, which was exactly what I needed
""".strip().split('\n')

ACTIONS = """
puts the kettle on
passes round the biscuit tin
yawns
waves
hides the last scone
pours another cup
stretches and cracks every joint
wanders off to find a jumper
makes a fresh pot
opens the window to let the storm in
dunks a biscuit and loses half of it
tips an imaginary hat
""".strip().split('\n')

URLS = [
    'https://example.org/recipes/ginger-biscuits',
    'https://example.org/recipes/lemon-drizzle',
    'https://example.com/photos/heron-on-the-canal.jpg',
    'https://example.com/photos/fox-in-the-garden.jpg',
    'https://example.net/weather/radar',
    'https://example.org/books/the-lighthouse-keepers',
    'https://example.com/maps/old-railway-walk',
    'https://example.net/tea/first-flush-guide',
    'https://example.org/garden/slug-advice',
    'https://example.com/video/moss-documentary',
]

EXCLAIM = """
what a day!
finally, the sun is out!
the cake worked!
I got the last loaf!
ooh, thunder!
we did it!
brilliant!
""".strip().split('\n')

HITS = ['slaps %s with a soggy teabag', 'hits %s with a rolled-up newspaper',
        'smacks %s with a wooden spoon']

REPLIES = """
yes
no
maybe later
I will have one
ha, same
that sounds great
good point
oh I like that
depends on the day
not me, I am afraid
I think so
absolutely
thanks
you are right
""".strip().split('\n')

QUIT_MSGS = ['Quit: bed', 'Quit: off to work', 'Ping timeout: 240 seconds',
             'Quit: see you all later', 'Read error: Connection reset by peer', 'Quit: brb']
KICK_MSGS = ['behave', 'no spoilers please', 'that is enough caps for one day',
             'go to bed', 'the scone was not yours', 'take a breather']
TOPICS = [
    'Welcome to #teatime | put the kettle on | book club on Sunday: The Lighthouse Keepers',
    'Welcome to #teatime | milk after, no arguments | stats: https://example.org/teatime/',
    '#teatime | the great scone debate continues | be nice',
    '#teatime | autumn is coming, get your jumpers out',
    '#teatime | quiz night Friday 21:00 | biscuits provided (imaginary)',
    '#teatime | Gerald the hedgehog is doing fine, thanks for asking',
    '#teatime | the kettle is always on',
    '#teatime | harvest swap on Saturday, bring courgettes, everyone has too many',
]

def hostof(n):
    return '%s!~%s@%s.users.undernet.org' % (n, P[n]['ident'], P[n]['ident'])

def say(n, others):
    p = P[n]
    # each trait gets its own draw, so one does not hide another
    if p.get('shout') and R.random() < 0.10:   t = R.choice(SHOUTS)
    elif p.get('foul') and R.random() < 0.04:  t = R.choice(FOUL)
    elif p.get('sad') and R.random() < 0.12:   t = R.choice(SAD)
    elif p.get('smile') and R.random() < 0.14: t = R.choice(HAPPY)
    elif p.get('long') and R.random() < 0.08:  t = R.choice(LONG)
    elif p.get('urls') and R.random() < 0.07:  t = 'look at this: ' + R.choice(URLS)
    elif p.get('asks') and R.random() < 0.18:  t = R.choice(QUESTIONS)
    elif p.get('excited') and R.random() < 0.20: t = R.choice(EXCLAIM)
    elif R.random() < 0.04:                    t = R.choice(QUESTIONS)
    elif R.random() < 0.03:                    t = R.choice(EXCLAIM)
    elif others and R.random() < 0.25:         t = R.choice(REPLIES)
    else:                                      t = R.choice(LINES)
    if p['words'] and R.random() < 0.22:
        w = R.choice(p['words'])
        t = (w + ', ' + t) if R.random() < 0.5 else (t + ', ' + w)
    if others and R.random() < 0.30:
        t = R.choice(others) + ': ' + t
    return t

# ---------------------------------------------------------------------------
# the log
# ---------------------------------------------------------------------------
def pick(hour, exclude=(), group=None):
    cands = [n for n in NICKS if n not in exclude]
    w = []
    for n in cands:
        x = P[n]['weight'] * (3.0 if hour in P[n]['hours'] else 0.25)
        if group and P[n]['group'] == group:
            x *= 4
        w.append(x)
    return R.choices(cands, weights=w)[0]

def write_logs(logdir):
    here = set()
    topic_i = 0
    total = 0
    for d in range(DAYS):
        day = START + timedelta(days=d)
        ev = []                                   # (seconds, text)
        weekend = day.weekday() >= 5
        for _ in range(R.randint(9, 15) + (4 if weekend else 0)):
            hour = R.choices(range(24), weights=[5,4,3,2,1,1,2,4,6,6,6,6,
                                                 7,7,7,7,7,8,9,10,10,10,9,7])[0]
            t = hour * 3600 + R.randint(0, 3000)
            first = pick(hour)
            people = [first]
            for _ in range(R.randint(1, 4)):
                people.append(pick(hour, exclude=people, group=P[first]['group']))
            for n in people:
                if n not in here:
                    ev.append((t, '%s (~%s@%s.users.undernet.org) joined %s.'
                                  % (n, P[n]['ident'], P[n]['ident'], CHAN)))
                    here.add(n); t += R.randint(5, 60)
            speaker = first
            for _ in range(R.randint(6, 34)):
                t += R.randint(4, 90)
                others = [o for o in people if o != speaker]
                if others and P[speaker].get('hits') and R.random() < 0.03:
                    ev.append((t, 'Action: %s %s' % (speaker, R.choice(HITS) % R.choice(others))))
                elif P[speaker].get('action') and R.random() < 0.10 or R.random() < 0.02:
                    ev.append((t, 'Action: %s %s' % (speaker, R.choice(ACTIONS))))
                else:
                    ev.append((t, '<%s> %s' % (speaker, say(speaker, others))))
                # monologue now and then; otherwise the conversation moves on
                if R.random() > 0.18:
                    speaker = R.choices(people, weights=[P[x]['weight'] for x in people])[0]
            # the odd op event
            if R.random() < 0.03:
                op = R.choice(OPS); victim = R.choice([p for p in people if p != op] or [first])
                if victim != op:
                    t += R.randint(5, 40)
                    ev.append((t, '%s kicked from %s by %s: %s' % (victim, CHAN, op, R.choice(KICK_MSGS))))
                    here.discard(victim)
            if R.random() < 0.06:
                op = R.choice(OPS); tgt = R.choice(people)
                t += R.randint(5, 40)
                ev.append((t, "%s: mode change '%s %s' by %s" % (CHAN, R.choice(['+o', '+v', '-o', '+v']), tgt, hostof(op))))
            if R.random() < 0.015:
                setter = R.choice([n for n in NICKS if P[n].get('topic') or P[n].get('op')])
                topic_i = (topic_i + 1) % len(TOPICS)
                t += R.randint(5, 40)
                ev.append((t, 'Topic changed on %s by %s: %s' % (CHAN, hostof(setter), TOPICS[topic_i])))
            if R.random() < 0.08:
                n = R.choice(people); t += R.randint(5, 40)
                ev.append((t, 'Nick change: %s -> %s|away' % (n, n)))
                ev.append((t + R.randint(600, 2400), 'Nick change: %s|away -> %s' % (n, n)))
            # some leave
            for n in people:
                if n in here and R.random() < 0.35:
                    t += R.randint(10, 200)
                    msg = R.choice(QUIT_MSGS)
                    ev.append((t, '%s (~%s@%s.users.undernet.org) left irc: %s'
                                  % (n, P[n]['ident'], P[n]['ident'], msg)))
                    here.discard(n)
        ev = sorted((min(s, 86399), x) for s, x in ev)
        out = []
        for s, x in ev:
            out.append('[%02d:%02d:%02d] %s' % (s // 3600, s % 3600 // 60, s % 60, x))
        io.open(os.path.join(logdir, 'teatime.log.%s' % day.strftime('%Y%m%d')), 'w',
                encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        total += len(out)
    return total

# ---------------------------------------------------------------------------
# run pisg once per scheme
# ---------------------------------------------------------------------------
def main():
    if not os.path.isfile(os.path.join(PISG, 'pisg')):
        sys.exit('pisg not found at %s' % PISG)
    if not os.path.isdir(DSTDIR):
        os.makedirs(DSTDIR)
    tmp = tempfile.mkdtemp(prefix='teatime-')
    try:
        logdir = os.path.join(tmp, 'logs'); os.makedirs(logdir)
        cfg = os.path.join(tmp, 'teatime.cfg')        # not the repository's own pisg.cfg
        io.open(cfg, 'w', encoding='utf-8').write(u'<set Charset="utf-8">\n')
        n = write_logs(logdir)
        print('%d log lines over %d days, %d nicks' % (n, DAYS, len(NICKS)))
        for theme in THEMES:
            out = os.path.join(tmp, theme + '.html')
            cmd = ['perl', 'pisg', '-s', '-co', cfg, '-ch', CHAN, '-f', 'eggdrop', '-ne', 'Undernet',
                   '-ma', 'vox', '-d', logdir, '-p', 'teatime.log.', '-o', out,
                   '-cf', 'ColorScheme=' + theme, '-cf', 'ChannelIndex=none',
                   '-cf', 'HomeLink=none']
            subprocess.check_call(cmd, cwd=PISG)
            h = io.open(out, encoding='utf-8').read()
            # a line saying what the page is, and a way back
            marker = '<p class="subtitle">'
            assert marker in h, 'no subtitle in pisg output'
            h = h.replace(marker,
              '<p class="subtitle"><a href="../../themes/">&larr; all themes</a> &middot; '
              'colour scheme <b>%s</b> &middot; sample page, invented people</p>\n' % theme
              + marker, 1)
            dst = os.path.join(DSTDIR, theme + '.html')
            io.open(dst, 'w', encoding='utf-8', newline='\n').write(h)
            print('%-10s %7d bytes' % (theme, len(h)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__':
    main()
