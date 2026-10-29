# Mom Tried These, rebuild 3. Curated collections, occasion gifts, one journal.
import os, json, html, re, shutil, sys, datetime as dt, email.utils
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from catalog import COLLECTIONS, GIFTS, P as CAT
from journal import J
from journal2 import J2
J = J2 + J
from popular import POP, POPULAR_EXISTING, GIFT_SEC, SECTIONS
from picks2 import P2
from picks3 import P3, BOUGHT_EXISTING
from PIL import Image

SITE = "https://momtriedthese.com"; OUT = 'out3'
TODAY = dt.date.today().isoformat()
US = "momtriedthese-20"; AE = "momtriedthese-21"
E = html.escape
import hashlib
CSSV = hashlib.md5(open('style3.css','rb').read()).hexdigest()[:8]
SLBAR = '<a class="slbar" href="/shortlist/"><span class="slk">Free guide</span><span class="slt">The Christmas Gift Shortlist, by age. Five picks for every age, 6 to 10.</span><span class="slgo">Get it free &rarr;</span></a>' if TODAY <= '2026-12-25' else ''
IMGSRC = os.environ.get('MTT_IMAGES', '../images/out')   # folder of <slug>.jpg

# ---------- ASINs from the old data
ASIN = json.load(open('data/asin.json'))
OLD = {}
for pk in json.load(open('data/picks.json')): OLD[pk['name']] = (pk.get('us'), pk.get('ae'))
for r in P2: OLD.setdefault(r[0], (r[1], r[2]))
for r in P3: OLD.setdefault(r[0], (r[1], r[2]))
BOUGHT = set(BOUGHT_EXISTING) | {r[0] for r in P3 if r[6]} | {"Smiggle Minecraft Trio Lunchbox", "Smiggle Spritz Spray Water Bottle"}

PR = {}
for slug, src, disp, home, why, best, _ in CAT:
    us_, ae_ = OLD.get(src, (ASIN.get(src), None))
    if not us_ and not ae_: us_ = ASIN.get(src)
    img = os.path.exists(f'{IMGSRC}/{slug}.jpg')
    PR[slug] = dict(slug=slug, src=src, name=disp, home=home, why=why, best=best, us=us_, ae=ae_,
                    bought=src in BOUGHT, img=img, pop=POPULAR_EXISTING.get(slug), sec=GIFT_SEC.get(slug, ''))
for slug, disp, asin, home, why, best, cnt, sec in POP:
    PR[slug] = dict(slug=slug, src=disp, name=disp, home=home, why=why, best=best, us=asin, ae=None, bought=False,
                    img=os.path.exists(f'{IMGSRC}/{slug}.jpg'), pop=cnt or 'top', sec=sec)
# vegetarian site: no egg or meat products
for s in ('egg-cooker',): PR.pop(s, None)
# the Smiggle bottle we bought is the Minecraft one
PR['smiggle-spritz'].update(name='Smiggle Minecraft Spritz Bottle', us=None, ae=None, src='Smiggle Minecraft spritz drink bottle',
    why="We bought this one, in Minecraft. A water bottle that also sprays a cool mist. On hot days, that's the feature that matters.")
def popn(p):
    v = p.get('pop') or ''; m = re.match(r'([\d.]+)K', v)
    return float(m.group(1)) * 1000 if m else (float(v.rstrip('+')) if v[:1].isdigit() else (500 if v == 'top' or v == '' and p.get('pop') is not None else 0))
SHOWN = {s: p for s, p in PR.items() if p['img']}
def q(n): return re.sub(r'\s+', '+', re.sub(r"[()'&!:,]", ' ', n).strip())
def link_us(p): return f"https://www.amazon.com/dp/{p['us']}?tag={US}" if p['us'] else f"https://www.amazon.com/s?k={q(p['src'])}&tag={US}"
def link_ae(p): return f"https://www.amazon.ae/dp/{p['ae']}?tag={AE}" if p['ae'] else f"https://www.amazon.ae/s?k={q(p['src'])}&tag={AE}"
def in_home(h): return [p for p in SHOWN.values() if p['home'] == h]

COLL = {c[0]: dict(slug=c[0], title=c[1], kicker=c[2], role=c[3], how=c[4]) for c in COLLECTIONS}
GIFT = {g[0]: dict(slug=g[0], title=g[1], kicker=g[2], role=g[3], banner=g[4], start=g[5], end=g[6]) for g in GIFTS}

# ---------- images: product copies + collages
os.makedirs(f'{OUT}/img/p', exist_ok=True); os.makedirs(f'{OUT}/img/c', exist_ok=True)
for p in SHOWN.values():
    im = Image.open(f'{IMGSRC}/{p["slug"]}.jpg').convert('RGB'); im.thumbnail((640, 640))
    im.save(f'{OUT}/img/p/{p["slug"]}.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
TINTS = {'quiet-hour': (236, 226, 212), 'game-night': (230, 222, 232), 'little-makers': (222, 231, 226), 'lunchbox': (242, 229, 210),
         'travel-day': (224, 231, 238), 'kid-tech': (229, 229, 222), 'fast-kitchen': (240, 226, 214), 'calm-home': (231, 226, 219),
         'windowsill-garden': (221, 232, 220), 'just-for-you': (243, 226, 226), 'minecraft-kid': (222, 233, 218),
         'christmas': (226, 236, 226), 'diwali': (246, 226, 198), 'party-favors': (240, 228, 236)}
def tile(im, size):
    """Square product image on white, with a soft rounded card."""
    t = Image.new('RGB', (size, size), (255, 255, 255)); im = im.copy(); im.thumbnail((int(size * .86), int(size * .86)))
    t.paste(im, ((size - im.width) // 2, (size - im.height) // 2)); return t
def collage(slug, items, w, h, name):
    from PIL import ImageDraw
    bg = Image.new('RGB', (w, h), TINTS.get(slug, (240, 236, 230)))
    ims = [Image.open(f'{IMGSRC}/{p["slug"]}.jpg').convert('RGB') for p in items[:4]]
    if not ims: bg.save(f'{OUT}/img/c/{name}.jpg', quality=82); return
    n = len(ims)
    if w > h:   # banner: 2x2 grid in the right half, fully visible
        s = int(min(h * .44, w * .2)); g = int(s * .08); gw = s * 2 + g
        x0 = int(w * .72 - gw / 2); y0 = int((h - gw) / 2)
        pos = [(x0, y0), (x0 + s + g, y0), (x0, y0 + s + g), (x0 + s + g, y0 + s + g)]
    else:       # square tile: 2x2
        s = int(w * .42); g = int(w * .04); x0 = int((w - (2 * s + g)) / 2)
        pos = [(x0, x0), (x0 + s + g, x0), (x0, x0 + s + g), (x0 + s + g, x0 + s + g)]
    if name.startswith('j-') and w > h:   # journal card: products side by side, large
        s = int(min(h * .66, (w * .86) / n)); g = int(s * .08); tot = n * s + (n - 1) * g; x0 = int((w - tot) / 2)
        pos = [(x0 + i * (s + g), int((h - s) / 2)) for i in range(n)]
    elif n == 1: pos = [(int(w * .72 - s / 2) if w > h else int((w - s) / 2), int((h - s) / 2))]
    if n == 2 and not name.startswith('j-'): pos = [pos[0], pos[3]]
    if n == 3 and not name.startswith('j-'): pos = [pos[0], pos[1], (int((pos[0][0] + pos[1][0]) / 2), pos[2][1])]
    xs = [a for a, b in pos[:n]]; ys = [b for a, b in pos[:n]]
    mask = Image.new('L', (s, s), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * .08), fill=255)
    for im, x, y in zip(ims, xs, ys):
        sh = Image.new('RGB', (s, s), tuple(max(0, c - 18) for c in TINTS.get(slug, (240, 236, 230))))
        bg.paste(sh, (x + 6, y + 10), mask); bg.paste(tile(im, s), (x, y), mask)
    bg.save(f'{OUT}/img/c/{name}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)

# ---------- HTML shell
URLS = []
def write(path, body):
    URLS.append(path)
    d = OUT + path; os.makedirs(d, exist_ok=True); open(d + 'index.html', 'w').write(body)
NAV = [("Collections", "/collections/"), ("Gifts", "/gifts/"), ("Journal", "/journal/"), ("About", "/about/")]
def head(title, desc, path, schema=(), img="/og.jpg", noindex=False):
    url = SITE + path; t = title if len(title) <= 62 else title.split(' | ')[0]
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if path.startswith(h) else ""}>{n}</a>' for n, h in NAV)
    sch = ''.join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schema)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="p:domain_verify" content="23cb3eb23d3625355cafdcaa68082097"/>
<title>{E(t)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">{'<meta name="robots" content="noindex">' if noindex else ''}
<meta property="og:type" content="website"><meta property="og:site_name" content="Mom Tried These"><meta property="og:title" content="{E(t)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}{img}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg"><link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Mom Tried These">
<link rel="preload" href="/fonts/lora-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/s3.css?v={CSSV}">{sch}</head><body>
<header class="top"><div class="wrap bar"><a class="logo" href="/">Mom Tried These</a><nav>{nav}</nav></div></header>'''
FOOT = f'''<section class="keep"><div class="wrap keepin"><div><p class="k">The monthly short list</p><h2>One email a month. Only the things that earned a spot.</h2><p>No daily deals, no countdown timers. Unsubscribe in one click.</p></div>
<form method="post" action="/subscribe.php" class="subf"><label class="vh" for="em">Email</label><input id="em" name="email" type="email" required placeholder="you@email.com" autocomplete="email"><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button>Join</button></form></div></section>
<footer class="foot"><div class="wrap fgrid"><div><a class="logo" href="/">Mom Tried These</a><p>The short list, from one busy mom to another.</p></div>
<div><p class="k">Explore</p><a href="/collections/">Collections</a><a href="/gifts/">Gifts</a><a href="/journal/">Journal</a></div>
<div><p class="k">About</p><a href="/about/">About</a><a href="/how-we-pick/">How we pick</a><a href="/contact/">Contact</a><a href="/disclosure/">Disclosure</a><a href="/privacy/">Privacy</a></div>
<div><p class="k">Shopping from</p><div class="store" role="group" aria-label="Choose your Amazon store"><button data-s="ae">UAE</button><button data-s="us">US</button></div></div></div>
<div class="wrap small"><p>As an Amazon Associate I earn from qualifying purchases. That never changes what goes on the list.</p><p>© 2026 Mom Tried These</p></div></footer>
<script>(function(){{var k='mtt-store',s;try{{s=localStorage.getItem(k)}}catch(e){{}}if(!s){{s=/Dubai|Muscat|Riyadh|Qatar|Kuwait|Bahrain|Asia\\/(Dubai|Muscat)/.test(Intl.DateTimeFormat().resolvedOptions().timeZone)?'ae':'us'}}
function set(v){{s=v;try{{localStorage.setItem(k,v)}}catch(e){{}}document.querySelectorAll('a.buy').forEach(function(a){{a.href=a.dataset[v]}});document.querySelectorAll('.store button').forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.s==v)}})}}
document.querySelectorAll('.store button').forEach(function(b){{b.onclick=function(){{set(b.dataset.s)}}}});set(s);
var sl=document.querySelectorAll('.slide'),i=0;if(sl.length>1){{var dots=document.querySelectorAll('.dots button');function go(n){{sl[i].classList.remove('on');dots[i].classList.remove('on');i=n;sl[i].classList.add('on');dots[i].classList.add('on')}}dots.forEach(function(d,n){{d.onclick=function(){{go(n)}}}});setInterval(function(){{go((i+1)%sl.length)}},6500)}}
var f=document.querySelectorAll('.filt button');f.forEach(function(b){{b.onclick=function(){{f.forEach(function(x){{x.setAttribute('aria-pressed',x==b)}});document.querySelectorAll('.jlist .jc').forEach(function(c){{c.hidden=b.dataset.k!='all'&&c.dataset.k!=b.dataset.k}})}}}})}})();</script>
</body></html>'''

def card(p, n=None, big=False):
    lab = '<span class="lab own">We bought this</span>' if p['bought'] else '<span class="lab">Shortlisted</span>'
    return f'''<article class="card{' big' if big else ''}" id="{p['slug']}"><div class="ph"><img src="/img/p/{p['slug']}.jpg" alt="{E(p['name'])}" width="640" height="640" loading="lazy"></div>
<div class="cb">{f'<span class="n">{n:02d}</span>' if n else ''}{lab}<h3>{E(p['name'])}</h3><p>{E(re.sub(r'^We bought (this|these|this one)\. ', '', p['why']))}</p><p class="best">{E(p['best'])}</p>
<a class="buy" rel="sponsored nofollow noopener" target="_blank" href="{link_ae(p)}" data-ae="{link_ae(p)}" data-us="{link_us(p)}">Check the price <span aria-hidden="true">↗</span></a></div></article>'''

def crumbs(items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' / '.join(f'<a href="{u}">{E(n)}</a>' for n, u in items[:-1]) + f' / <span>{E(items[-1][0])}</span></nav>', ld

# ---------- markup for journal bodies
def md(s):
    out, ul = [], False
    for block in s.strip().split('\n\n'):
        lines = block.split('\n')
        if all(l.startswith('[[') for l in lines):
            cards = [SHOWN[l[2:-2]] for l in lines if l[2:-2] in SHOWN]
            if cards: out.append('<div class="grid g2 inpost">' + ''.join(card(c) for c in cards) + '</div>')
            continue
        if lines[0].startswith('## '): out.append(f'<h2>{E(lines[0][3:])}</h2>'); lines = lines[1:]
        if not lines: continue
        if all(l.startswith('- ') for l in lines): out.append('<ul>' + ''.join(f'<li>{inline(l[2:])}</li>' for l in lines) + '</ul>')
        else: out.append('<p>' + '<br>'.join(inline(l) for l in lines) + '</p>')
    return ''.join(out)
def inline(t): return re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', r'<a href="\2">\1</a>', E(t))

KIND = {"list": ("A list", "Lists"), "note": ("A note", "Notes"), "idea": ("An idea", "Ideas"), "bought": ("Why we bought it", "Why we bought it")}
def jcard(o):
    img = f'/img/c/j-{o["slug"]}.jpg'
    return f'<a class="jc" data-k="{o["kind"]}" href="/journal/{o["slug"]}/"><img src="{img}" alt="" width="600" height="400" loading="lazy"><span class="k">{KIND[o["kind"]][0]}</span><h3>{E(o["title"])}</h3><p>{E(o["desc"])}</p></a>'

# ======================================================= pages
# collages
for c in COLL.values():
    it = in_home(c['slug']); collage(c['slug'], it, 900, 900, c['slug']); collage(c['slug'], it, 1600, 700, c['slug'] + '-wide')
for g in GIFT.values():
    it = in_home(g['slug']); collage(g['slug'], it, 900, 900, g['slug']); collage(g['slug'], it, 1600, 700, g['slug'] + '-wide')
JTINT = {'list': (232, 228, 238), 'note': (243, 232, 222), 'idea': (226, 233, 226), 'bought': (238, 230, 218)}
for o in J:
    TINTS['j-' + o['slug']] = JTINT[o['kind']]
    prods = [SHOWN[x] for x in re.findall(r'\[\[([a-z0-9-]+)\]\]', o['body']) if x in SHOWN]
    if o['kind'] == 'note':
        from PIL import ImageDraw, ImageFont
        im = Image.new('RGB', (1200, 800), JTINT['note']); d = ImageDraw.Draw(im)
        try: fnt = ImageFont.truetype('static/lora.ttf', 60)
        except Exception: fnt = ImageFont.load_default()
        pull = re.sub(r'\s+', ' ', [l for l in o['body'].split('\n') if l.strip() and not l.startswith(('#', '-', '['))][0]).strip()
        if len(pull) > 90: pull = pull[:pull.rfind(' ', 0, 88)] + '...'
        words, lines, cur = ('\u201c' + pull + '\u201d').split(), [], ''
        for w_ in words:
            if d.textlength(cur + ' ' + w_, font=fnt) > 920: lines.append(cur); cur = w_
            else: cur = (cur + ' ' + w_).strip()
        lines.append(cur); y = 400 - len(lines) * 42
        for l in lines: d.text((140, y), l, font=fnt, fill=(60, 48, 40)); y += 84
        d.rectangle((140, y + 24, 220, y + 30), fill=(210, 100, 63))
        im.thumbnail((600, 400)); im.save(f'{OUT}/img/c/j-{o["slug"]}.jpg', quality=84)
    else:
        if not prods: prods = [p for p in SHOWN.values() if p['home'] == ('game-night' if 'playdate' in o['slug'] else 'fast-kitchen')][:3]
        collage('j-' + o['slug'], prods, 1200, 800, 'j-' + o['slug'])
        Image.open(f'{OUT}/img/c/j-{o["slug"]}.jpg').resize((600, 400)).save(f'{OUT}/img/c/j-{o["slug"]}.jpg', quality=84)

def live(g): return g['start'] <= TODAY <= g['end']
SEASON = sorted([g for g in GIFT.values() if live(g) and g['slug'] != 'party-favors'], key=lambda g: g['end'])

# ---- Home
FAV = ['smiggle-minecraft-lunch', 'yoto', 'train-of-thought', 'rose-mist', 'magnetic-tiles', 'jbl-junior', 'lego-advent-starwars', 'paniyaram-pan']
fav = [SHOWN[s] for s in FAV if s in SHOWN][:6]
TOPPOP, _seen = [], set()
for p in sorted([p for p in SHOWN.values() if p.get('pop') and p['home'] not in ('fast-kitchen', 'just-for-you', 'party-favors')], key=popn, reverse=True):
    if p['home'] in _seen or p in fav: continue
    TOPPOP.append(p); _seen.add(p['home'])
TOPPOP = TOPPOP[:6]
slides = ''.join(f'''<a class="slide{' on' if i == 0 else ''}" href="/gifts/{g['slug']}/" style="--w:url(/img/c/{g['slug']}-wide.jpg);--q:url(/img/c/{g['slug']}.jpg)"><div class="sc"><span class="k">{E(g['kicker'])}</span><h2>{E(g['banner'])}</h2><p>{E(g['role'])}</p><span class="go">Open the list <span aria-hidden="true">→</span></span></div></a>''' for i, g in enumerate(SEASON))
dots = ''.join(f'<button class="{"on" if i == 0 else ""}" aria-label="Show banner {i + 1}"></button>' for i in range(len(SEASON)))
START = ['quiet-hour', 'lunchbox', 'travel-day', 'game-night', 'fast-kitchen', 'just-for-you']
latest = [next(o for o in J if o['kind'] == k) for k in ('list', 'note', 'idea')]
home = head("Mom Tried These: The Short List for Busy Moms", "A short, honest list of things for kids, home and the mom running both. Every pick has a reason, and if we bought it, we say so.", "/",
            [{"@context": "https://schema.org", "@type": "WebSite", "name": "Mom Tried These", "url": SITE}]) + f'''<main>
<section class="hero"><div class="wrap"><p class="k">Hi. This is the short list.</p><h1>Fewer things, <em>better chosen.</em></h1><p class="lede">I research everything like it's a big decision, even the lunchbox. This is what made the cut, and why. If we bought it, it says so.</p></div></section>
<div class="wrap">{SLBAR}</div>
<section class="wrap"><div class="slides">{slides}<div class="dots">{dots}</div></div></section>
<section class="wrap sec"><div class="sh"><h2>Start with what you need</h2><a href="/collections/">All collections</a></div><div class="tiles">
{''.join(f'<a class="tile" href="/collections/{s}/"><img src="/img/c/{s}.jpg" alt="" width="900" height="900" loading="lazy"><span class="k">{E(COLL[s]["kicker"])}</span><h3>{E(COLL[s]["title"])}</h3></a>' for s in START)}</div></section>
<section class="wrap sec"><div class="sh"><h2>Where I'd start</h2><a href="/collections/">See every collection</a></div><p class="subf">The first thing I'd buy from each collection, and the problem it solves.</p><div class="grid g3">{''.join(card(p) for p in TOPPOP)}</div></section>
<section class="wrap sec"><div class="sh"><h2>Our favourites right now</h2></div><p class="subf">If you only look at six things, look at these.</p><div class="grid g3">{''.join(card(p) for p in fav)}</div></section>
<section class="wrap sec"><div class="sh"><h2>From the journal</h2><a href="/journal/">Read more</a></div><div class="jlist">{''.join(jcard(o) for o in latest)}</div></section>
</main>''' + FOOT
write('/', home)

# ---- Collections index + pages
ORDERED = [c for c in COLL.values() if in_home(c['slug'])]
write('/collections/', head("Collections | Mom Tried These", "Short, curated collections for everyday family life: quiet play, game night, lunchboxes, travel, kid-safe tech, the kitchen and you.", "/collections/") +
      f'''<main class="wrap"><section class="intro"><h1>Collections</h1><p class="lede">Each collection does one job. Every product lives in one place only, with the reason it's there.</p></section>
<div class="tiles all">{''.join(f'<a class="tile" href="/collections/{c["slug"]}/"><img src="/img/c/{c["slug"]}.jpg" alt="" width="900" height="900" loading="lazy"><span class="k">{E(c["kicker"])}</span><h3>{E(c["title"])}</h3><p>{E(c["role"])}</p></a>' for c in ORDERED)}</div></main>''' + FOOT)
for i, c in enumerate(ORDERED):
    it = in_home(c['slug'])
    hot = sorted([p for p in it if p.get('pop')], key=popn, reverse=True)[:6]; rest = [p for p in it if p not in hot]
    it = hot + rest
    nxt = [ORDERED[(i + 1) % len(ORDERED)], ORDERED[(i + 2) % len(ORDERED)]]
    ch, cld = crumbs([("Home", "/"), ("Collections", "/collections/"), (c['title'], f"/collections/{c['slug']}/")])
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": c['title'], "numberOfItems": len(it), "itemListElement": [{"@type": "ListItem", "position": k + 1, "name": p['name']} for k, p in enumerate(it)]}
    write(f"/collections/{c['slug']}/", head(f"{c['title']}: {c['kicker']} | Mom Tried These", f"{c['role']} {len(it)} picks, each with the reason it's here.", f"/collections/{c['slug']}/", [cld, il], img=f"/img/c/{c['slug']}-wide.jpg") +
          f'''<main><section class="chero" style="--w:url(/img/c/{c['slug']}-wide.jpg);--q:url(/img/c/{c['slug']}.jpg);background-color:rgb{TINTS.get(c['slug'])}"><div class="wrap"><div class="chbox">{ch}<span class="k">{E(c['kicker'])}</span><h1>{E(c['title'])}</h1><p class="lede">{E(c['role'])}</p></div></div></section>
<section class="wrap">{SLBAR}<div class="how"><p class="k">How we chose</p><p>{E(c['how'])}</p><p class="cnt">{len(it)} picks{f' · {nb} bought by us' if (nb := sum(p['bought'] for p in it)) else ''}</p></div>
{f'<h2 class="secth">Start with these</h2><p class="sectp">If you only get one or two things from this collection, make it these.</p><div class="grid g3">' + ''.join(card(p) for p in hot) + '</div>' if hot else ''}
<h2 class="secth">{'Our other picks' if hot else 'Our picks'}</h2><div class="grid g3">{''.join(card(p, k + 1) for k, p in enumerate(rest))}</div>
<div class="more"><p class="k">Next, maybe</p><div class="tiles two">{''.join(f'<a class="tile" href="/collections/{x["slug"]}/"><img src="/img/c/{x["slug"]}.jpg" alt="" width="900" height="900" loading="lazy"><span class="k">{E(x["kicker"])}</span><h3>{E(x["title"])}</h3></a>' for x in nxt)}</div></div></section></main>''' + FOOT)


SLF = '<form method="post" action="/subscribe.php" class="subf"><label class="vh" for="sle">Email</label><input id="sle" name="email" type="email" required placeholder="you@email.com" autocomplete="email"><input type="hidden" name="src" value="/shortlist/"><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button>Send me the list</button></form>'
SLCTA = f'<aside class="slcta"><img src="/shortlist/cover.jpg" alt="" width="300" height="424" loading="lazy"><div><p class="k">Free guide</p><h2>The Christmas Gift Shortlist, by Age</h2><p>Five picks for every age from 6 to 10, the reason each one is there, and two rules that stop the January pile. Eight pages. Free.</p>{SLF}<p class="fine">You also get our one-a-month short list. Unsubscribe in one click.</p></div></aside>'

# ---- Gifts
def gift_body(g, it):
    secs = SECTIONS.get(g['slug'])
    if not secs: return '<div class="grid g3 top">' + ''.join(card(p) for p in sorted(it, key=popn, reverse=True)) + '</div>'
    nav = '<nav class="gnav" aria-label="Sections">' + ''.join(f'<a href="#{k}">{E(t)}</a>' for k, t, _ in secs) + '</nav>'
    out = [nav]
    for k, t, d in secs:
        ps = sorted([p for p in it if p.get('sec') == k], key=popn, reverse=True)
        if not ps: continue
        out.append(f'<section class="gsec" id="{k}"><h2 class="secth">{E(t)}</h2><p class="sectp">{E(d)}</p><div class="grid g3">' + ''.join(card(p) for p in ps) + '</div></section>')
    left = [p for p in it if p.get('sec') not in [s[0] for s in secs]]
    if left: out.append('<section class="gsec"><h2 class="secth">More ideas</h2><div class="grid g3">' + ''.join(card(p) for p in left) + '</div></section>')
    return ''.join(out)
GL = [g for g in GIFT.values() if in_home(g['slug'])]
write('/gifts/', head("Gift Guides by Occasion | Mom Tried These", "Gift lists by occasion: Christmas picked early, Diwali far from home and party bags kids keep.", "/gifts/") +
      f'''<main class="wrap"><section class="intro"><h1>Gifts</h1><p class="lede">Lists for a moment, not for every day. Each one is its own short set of products.</p></section>
{''.join(f'<a class="gban" href="/gifts/{g["slug"]}/" style="--w:url(/img/c/{g["slug"]}-wide.jpg);--q:url(/img/c/{g["slug"]}.jpg)"><div class="sc"><span class="k">{E(g["kicker"])}</span><h2>{E(g["title"])}</h2><p>{E(g["role"])}</p><span class="go">Open the list →</span></div></a>' for g in GL)}</main>''' + FOOT)
for g in GL:
    it = in_home(g['slug'])
    ch, cld = crumbs([("Home", "/"), ("Gifts", "/gifts/"), (g['title'], f"/gifts/{g['slug']}/")])
    write(f"/gifts/{g['slug']}/", head(f"{g['title']} | Mom Tried These", f"{g['role']} {len(it)} picks.", f"/gifts/{g['slug']}/", [cld], img=f"/img/c/{g['slug']}-wide.jpg") +
          f'''<main><section class="chero" style="--w:url(/img/c/{g['slug']}-wide.jpg);--q:url(/img/c/{g['slug']}.jpg);background-color:rgb{TINTS.get(g['slug'])}"><div class="wrap"><div class="chbox">{ch}<span class="k">{E(g['kicker'])}</span><h1>{E(g['title'])}</h1><p class="lede">{E(g['role'])}</p></div></div></section>
<section class="wrap">{SLBAR}{gift_body(g, it)}{SLCTA if g['slug'] == 'christmas' else ''}</section></main>''' + FOOT)

# ---- Journal
write('/journal/', head("Journal | Mom Tried These", "Short notes for moms, ideas you can use today, and why we bought the things we bought.", "/journal/") +
      f'''<main class="wrap"><section class="intro"><h1>Journal</h1><p class="lede">Four kinds of writing, each with one job. Lists are for choosing. Notes are for you. Ideas are for today. Why we bought it is for when you're deciding.</p>
<div class="filt" role="group" aria-label="Filter"><button data-k="all" aria-pressed="true">All</button><button data-k="list" aria-pressed="false">Lists</button><button data-k="note" aria-pressed="false">Notes</button><button data-k="idea" aria-pressed="false">Ideas</button><button data-k="bought" aria-pressed="false">Why we bought it</button></div></section>
<div class="jlist">{''.join(jcard(o) for o in J)}</div></main>''' + FOOT)
for o in J:
    path = f"/journal/{o['slug']}/"
    ch, cld = crumbs([("Home", "/"), ("Journal", "/journal/"), (o['title'], path)])
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": o['title'], "description": o['desc'], "datePublished": o['date'], "dateModified": TODAY, "author": {"@type": "Organization", "name": "Mom Tried These"}, "image": SITE + f"/img/c/j-{o['slug']}.jpg", "mainEntityOfPage": SITE + path}
    others = [x for x in J if x['kind'] == o['kind'] and x is not o][:2]
    disc = '' if o['kind'] == 'note' or '[[' not in o['body'] else '<p class="disc">Links on this page go to Amazon. If you buy, we may earn a small commission at no cost to you.</p>'
    write(path, head(f"{o['title']} | Mom Tried These", o['desc'], path, [cld, art], img=f"/img/c/j-{o['slug']}.jpg") +
          f'''<main class="wrap"><article class="post {o['kind']}">{ch}<span class="k">{KIND[o['kind']][0]}</span><h1>{E(o['title'])}</h1><p class="lede">{E(o['desc'])}</p>{SLBAR if o['kind'] == 'list' else ''}{disc}<div class="body">{md(o['body'])}</div>{SLCTA if o['kind'] == 'list' else ''}</article>
<section class="sec"><div class="sh"><h2>More {KIND[o['kind']][1].lower()}</h2><a href="/journal/">All writing</a></div><div class="jlist">{''.join(jcard(x) for x in others)}</div></section></main>''' + FOOT)

# ---- Simple pages
PAGES = {
 "/about/": ("About", "About Mom Tried These: an independent, mom-run short list of things for kids, home and the mom running both.", """<h1>About</h1>
<p class="lede">Hi. I'm a working mom who researches everything like it's a big decision. Even the lunchbox. Especially the lunchbox.</p>
<p>Mom Tried These started as a list I kept for myself. What actually worked, what didn't, and what I'd tell a friend to buy if she asked me at the school gate.</p>
<p>There's a lot of noise out there. Hundred-item gift guides, "must-haves" that nobody needs, and the same ten products dressed up in different lists. This is the opposite. Fewer things, each with a reason.</p>
<h2>Two labels, always</h2><p><b>We bought this</b> means exactly that. We paid for it, it lives in our house.</p><p><b>Shortlisted</b> means I've researched it properly and would consider it, but I haven't bought it. I'll never blur the two.</p>
<h2>How the money works</h2><p>Some links go to Amazon, and if you buy, I may earn a small commission at no cost to you. That's what keeps this going. It never decides what goes on the list.</p>
<p>Questions, or a product you think belongs here? <a href="/contact/">Write to me</a>. I read everything.</p>"""),
 "/how-we-pick/": ("How We Pick", "How Mom Tried These chooses products: one job per collection, a reason for every pick, and honest labels.", """<h1>How we pick</h1><p class="lede">Every product has to answer one question: would I tell a friend to buy this?</p>
<h2>The rules</h2><ul><li>Every collection has one job. If a product doesn't help with that job, it doesn't go in.</li><li>Every product lives in one place only. No padding lists with the same things.</li><li>Every pick gets a reason. If I can't explain why in two lines, it's not good enough.</li><li>Bought or shortlisted, it says so. Always.</li><li>Fewer is better. A collection stops at around twelve.</li></ul>
<h2>What gets cut</h2><p>Things that need a 20-minute setup. Toys that are fun for one afternoon. Anything that's mostly packaging. And anything I wouldn't put in my own house.</p>"""),
 "/disclosure/": ("Affiliate Disclosure", "Mom Tried These affiliate disclosure.", """<h1>Affiliate disclosure</h1><p>Mom Tried These participates in the Amazon Services LLC Associates Program and the Amazon.ae Associates Program, affiliate advertising programs designed to provide a means for sites to earn fees by linking to Amazon.com and Amazon.ae.</p><p>As an Amazon Associate I earn from qualifying purchases. When you buy through a link on this site, I may earn a small commission at no extra cost to you.</p><p>Commissions never decide what goes on a list. Products are labelled <b>We bought this</b> only when we paid for them ourselves, and <b>Shortlisted</b> when they're researched but not bought.</p><p>Product images come from the brands or their retailers and remain the property of their owners. If you own an image and want it removed, <a href="/contact/">tell us</a> and it comes down the same day.</p>"""),
 "/privacy/": ("Privacy Policy", "Privacy policy for Mom Tried These.", """<h1>Privacy</h1><p>This site does not use advertising cookies or tracking scripts. Your store choice (UAE or US) is saved in your browser only.</p><p><b>Email list.</b> If you join the monthly email, your address is stored securely and used only to send that email. Unsubscribe any time.</p><p><b>Contact form.</b> Messages go to our inbox and are used only to reply.</p><p><b>Amazon links.</b> When you click through to Amazon, Amazon's own privacy policy and cookies apply.</p><p>Questions: <a href="/contact/">contact us</a>.</p>"""),
 "/contact/": ("Contact", "Contact Mom Tried These.", """<h1>Contact</h1><p class="lede">A question about a product, something you think belongs on a list, or a brand enquiry. I read every message.</p>
<form class="form" method="post" action="/contact.php"><label>Your name<input name="name" required maxlength="100" autocomplete="name"></label><label>Email<input name="email" type="email" required maxlength="200" autocomplete="email"></label><label>What's this about?<select name="topic"><option>A product question</option><option>Suggest a product</option><option>Brand or collaboration</option><option>Something else</option></select></label><label>Message<textarea name="message" required maxlength="4000" rows="6"></textarea></label><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn" type="submit">Send</button></form>"""),
 "/shortlist/": ("The Christmas Gift Shortlist, by Age", "A free 8-page guide: five gifts for every age from 6 to 10 that still get played with in January, and why each one is there.", f'''<p class="k">Free guide, 2026</p><h1>The Christmas Gift Shortlist, by Age</h1><p class="lede">Five gifts for every age from 6 to 10 that still get played with in January. The reason each one is there. And two rules that do most of the work.</p><img src="/shortlist/cover.jpg" alt="Cover of the Christmas Gift Shortlist" width="300" height="424" style="max-width:260px;margin:24px 0;border:1px solid var(--line);border-radius:10px"><p>Eight pages, made to read on your phone in the school pickup line. Pick two per child, and stop.</p>{SLF}<p class="fine">You also get our one-a-month short list. Nothing else. Unsubscribe in one click.</p>'''),
 "/shortlist/thanks/": ("Your shortlist", "Download the Christmas Gift Shortlist.", '<h1>Here it is</h1><p class="lede">Thank you. Your Christmas Gift Shortlist is ready.</p><p><a class="btn" href="/shortlist/mtt-christmas-shortlist-2026.pdf" download>Download the PDF</a></p><p>Every pick in the guide links to the full list on our site, with prices for the UAE and the US.</p><p><a href="/gifts/christmas/">Or go straight to the Christmas list</a></p>'),
 "/subscribed/": ("You're in", "Thanks for joining.", '<h1>You\'re in</h1><p class="lede">Thank you. The first short list lands at the start of next month.</p><p><a class="btn" href="/collections/">Browse the collections</a></p>'),
 "/contact/thanks/": ("Message sent", "Thanks for your message.", '<h1>Thank you</h1><p class="lede">Your message is on its way.</p><p><a class="btn" href="/">Back home</a></p>'),
}
for path, (t, d, b) in PAGES.items():
    write(path, head(f"{t} | Mom Tried These", d, path, noindex=path in ('/subscribed/', '/contact/thanks/', '/shortlist/thanks/')) + f'<main class="wrap"><div class="prose">{b}</div></main>' + FOOT)
URLS.remove('/subscribed/'); URLS.remove('/contact/thanks/'); URLS.remove('/shortlist/thanks/')
shutil.copytree('static/shortlist', f'{OUT}/shortlist', dirs_exist_ok=True)

# ---- redirects from old URLs
RED = {}
OLDMAP = {'/shop/': '/collections/', '/whats-selling/': '/', '/bought-by-us/': '/collections/', '/moms-life/': '/journal/', '/blog/': '/journal/', '/lists/': '/collections/',
 '/themes/': '/collections/', '/30-day-test/': '/how-we-pick/', '/christmas-gifts-for-kids-2026/': '/gifts/christmas/', '/stocking-stuffers-for-kids/': '/gifts/christmas/',
 '/birthday-return-gifts/': '/gifts/party-favors/', '/gifts-for-kids-who-build/': '/collections/little-makers/', '/travel-activities-for-kids/': '/collections/travel-day/'}
for a in range(5, 11): OLDMAP[f'/gifts-for-{a}-year-olds/'] = '/gifts/christmas/'
OLDPOST = {'diwali-away-from-home': '/gifts/diwali/', 'early-christmas-finds-2026': '/gifts/christmas/', 'lego-advent-calendars-2026': '/gifts/christmas/', 'minecraft-gifts-and-finds': '/collections/minecraft-kid/',
 'minecraft-t-shirts-and-keyrings': '/collections/minecraft-kid/', 'water-bottles-that-work-for-us': '/collections/lunchbox/', 'lunchboxes-i-love': '/collections/lunchbox/', '10-minute-school-lunchbox-system': '/collections/lunchbox/',
 'bentgo-vs-omiebox-vs-yumbox-vs-planetbox': '/collections/lunchbox/', 'long-haul-flight-with-kids-packing-list': '/collections/travel-day/', 'travel-friendly-products': '/collections/travel-day/', 'travel-games-we-bought': '/collections/travel-day/',
 'kid-safe-gadgets': '/collections/kid-tech/', 'gadgets-i-like': '/collections/kid-tech/', 'work-from-home-mom-tech': '/collections/kid-tech/', 'best-family-card-games': '/collections/game-night/',
 'kids-activities-that-hold-attention': '/collections/quiet-hour/', 'magnetic-tiles-worth-it': '/collections/quiet-hour/', 'magna-tiles-vs-cheaper-magnetic-tiles': '/collections/quiet-hour/', 'long-weekend-at-home-with-kids': '/collections/quiet-hour/',
 'stem-toys-for-8-to-12-year-olds': '/collections/little-makers/', 'natural-self-care-that-lifts-my-mood': '/collections/just-for-you/', 'make-home-smell-like-a-hotel': '/collections/calm-home/', 'no-drill-renters-toolkit': '/collections/calm-home/',
 'hallway-shoe-chaos-fix': '/collections/calm-home/', 'indoor-plants-ac-apartment-with-kids': '/collections/windowsill-garden/', 'kitchen-organizers-i-bought': '/collections/fast-kitchen/', 'instant-pot-weeknight-dinners': '/collections/fast-kitchen/',
 'paniyaram-pan-weekend-breakfast': '/journal/paniyaram-pan/', 'homemade-dahi-yogurt-maker': '/journal/electric-yogurt-maker/', 'the-squishy-shelf': '/gifts/christmas/', 'birthday-return-gifts-for-kids': '/gifts/party-favors/',
 'halloween-top-20-picks': '/gifts/', 'unique-thanksgiving-products': '/gifts/', 'sun-safe-kids-kit': '/collections/', 'school-small-stuff': '/collections/lunchbox/', 'school-morning-routine': '/journal/', 'moving-countries-with-kids-first-week-box': '/journal/',
 'playdate-ideas-when-you-have-to-work': '/journal/zero-setup-playdate-ideas/', 'playdate-snacks-everyone-eats': '/journal/after-school-snacks-not-biscuits/'}
JS = {o['slug'] for o in J}
for s in JS: OLDPOST.setdefault(s, f'/journal/{s}/')
for s, to in OLDPOST.items(): OLDMAP[f'/blog/{s}/'] = to
for a in os.listdir('data') if False else []: pass
ht = open('static/php/htaccess-base').read() + '\n' + ''.join(f'RedirectMatch 301 ^{re.escape(a)}?$ {SITE}{b}\n' for a, b in OLDMAP.items()) + 'RedirectMatch 301 ^/lists/(.*)$ https://momtriedthese.com/collections/\nRedirectMatch 301 ^/themes/(.*)$ https://momtriedthese.com/collections/\nRedirectMatch 301 ^/gifts-for-(.*)$ https://momtriedthese.com/gifts/christmas/\n'
open(f'{OUT}/.htaccess', 'w').write(ht)

# ---- extras
shutil.copy('static/php/subscribe.php', f'{OUT}/subscribe.php'); shutil.copy('static/php/contact.php', f'{OUT}/contact.php')
shutil.copy('static/og.jpg', f'{OUT}/og.jpg'); shutil.copy('style3.css', f'{OUT}/s3.css'); shutil.copytree('static/fonts', f'{OUT}/fonts', dirs_exist_ok=True)
if os.path.isdir('static/pins'): open(f'{OUT}/pinterest-23cb3.html','w').write('<!DOCTYPE html><html><head><meta name="p:domain_verify" content="23cb3eb23d3625355cafdcaa68082097"/></head><body></body></html>'); shutil.copytree('static/pins', f'{OUT}/pins', dirs_exist_ok=True)
open(f'{OUT}/favicon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#C8643F"/><text x="32" y="43" font-family="Georgia,serif" font-size="30" font-weight="700" fill="#FAF6F0" text-anchor="middle">M</text></svg>')
open(f'{OUT}/2f9c7b1e8a4d4c6b9e3f5a7d1c0b8e62.txt', 'w').write('2f9c7b1e8a4d4c6b9e3f5a7d1c0b8e62')
open(f'{OUT}/robots.txt', 'w').write(f"User-agent: *\nAllow: /\nDisallow: /contact.php\nDisallow: /subscribe.php\nDisallow: /shortlist/thanks/\nDisallow: /shortlist/mtt-christmas-shortlist-2026.pdf\nSitemap: {SITE}/sitemap.xml\n")
open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in URLS) + '</urlset>')
items = ''.join(f"<item><title>{E(o['title'])}</title><link>{SITE}/journal/{o['slug']}/</link><guid>{SITE}/journal/{o['slug']}/</guid><description>{E(o['desc'])}</description><pubDate>{email.utils.format_datetime(dt.datetime.fromisoformat(o['date'] + 'T08:00:00+00:00'))}</pubDate></item>" for o in J)
open(f'{OUT}/feed.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Mom Tried These</title><link>{SITE}/</link><description>The short list, from one busy mom to another.</description>{items}</channel></rss>')
open(f'{OUT}/404.html', 'w').write(head("Page not found | Mom Tried These", "Page not found.", "/404.html", noindex=True) + '<main class="wrap"><div class="prose"><h1>That page wandered off</h1><p class="lede">Like a sock in the wash. Try the <a href="/collections/">collections</a> instead.</p></div></main>' + FOOT)
# photo queue: products that have no image yet (for Aarti's shoot list)
missing = [p for p in PR.values() if not p['img']]
open(f'{OUT}/../photo-queue.txt', 'w').write('\n'.join(f"{p['home']}\t{p['name']}\t{'BOUGHT' if p['bought'] else ''}" for p in missing))
print(f"{len(URLS)} pages, {len(SHOWN)}/{len(PR)} products shown, {len(missing)} waiting for photos")
