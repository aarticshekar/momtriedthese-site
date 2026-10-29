import os, json, html, re, shutil, sys
sys.path.insert(0, 'data')
from posts import POSTS
from picks2 import P2
from picks3 import P3, BOUGHT_EXISTING
SITE = "https://momtriedthese.com"
TODAY = "2026-10-28"; TODAY_H = "28 October 2026"
US = "momtriedthese-20"; AE = "momtriedthese-21"
E = html.escape
LISTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','lists.json')))
ASIN = json.load(open('data/asin.json'))
ASIN['LEGO Large Creative Brick Box 10698']='B00NHQF6MG'; ASIN['LEGO Medium Creative Brick Box 10696']='B00NHQFA1I'
PICKS = json.load(open('data/picks.json'))
BLURB = json.load(open('data/blurbs.json'))
SKIP = {"IKEA Flisat children's table", "IKEA Trofast Storage System", "KiwiCo Monthly Subscription (Atlas or Tinker Crate)", "KiwiCo Kiwi Crate"}
USSP = [("colour", "color"), ("Colour", "Color"), ("jewellery", "jewelry"), ("tyre", "tire"), ("organiser", "organizer"), ("maths", "math"), ("favourite", "favorite"), ("neighbourhood", "neighborhood")]
def usp(s):
    for a, b in USSP: s = s.replace(a, b)
    return s

ORDER = ["kid-activities", "survival-box", "travel-day", "lunchbox", "playdates", "tech", "pantry"]
META = {
 "kid-activities": dict(short="Kid Activities", emoji="🧩", color="#E9D9C5", seo="Kids Activities That Hold Attention: 72 Screen-Free Picks", desc="72 screen-free kids activities that hold attention for 30 to 90 minutes: building toys, puzzles, crafts, pretend play and sensory toys. Shop on Amazon US or UAE."),
 "survival-box": dict(short="The Survival Box", emoji="🧊", color="#DCE4DD", seo="The Survival Box: What to Stock When Help Doesn't Show Up", desc="What a working mom keeps stocked for the day the help cancels: freezer prep, pantry staples, 15-minute kitchen tools, a kid distraction kit and a mom reset."),
 "travel-day": dict(short="Travel Day", emoji="✈️", color="#E3E7EC", seo="Travel With Kids Packing List: The Travel Day Survival Kit", desc="A travel with kids packing list for flights, hotels, road trips and beach days, plus the mom carry-on. Tested in transit. Shop on Amazon US or UAE."),
 "lunchbox": dict(short="The 10-Minute Lunchbox", emoji="🥪", color="#F2E3CF", seo="School Lunchbox Ideas: The 10-Minute Lunchbox System", desc="School lunchbox ideas and gear for fast mornings: bento boxes, prep tools, nut-free snacks and the small extras that save a sad lunch."),
 "playdates": dict(short="Playdates & Group Play", emoji="🎲", color="#EADBD3", seo="Playdate Ideas and Group Games for Kids", desc="Playdate ideas for busy parents: setup, group games that don't need a referee, educational screen time and parallel play."),
 "tech": dict(short="Tech & Gadgets", emoji="🔌", color="#E1E1DA", seo="Tech for Work-From-Home Moms: Gadgets I Don't Live Without", desc="Tech and gadgets for moms who work from home and travel: chargers, cables, smart home helpers and travel power."),
 "picks": dict(short="What's selling", emoji="📈", color="#E6E1EC", seo="", desc=""),
 "pantry": dict(short="The Pantry Edit", emoji="☕", color="#EFE0CC", seo="The Pantry Edit: Snacks, Drinks and Brands I Keep Stocked", desc="The snacks, drinks and pantry brands a busy mom keeps stocked and buys again. Shop on Amazon US or UAE."),
}
# Products
PROD = {}
for lk in ORDER:
    for sec, names in LISTS[lk]['sections'].items():
        for n in names:
            if n in SKIP or n not in BLURB: continue
            PROD.setdefault(n, dict(name=n, asin=ASIN.get(n), blurb=usp(BLURB[n]), lists=[], secs=[]))
            PROD[n]['lists'].append(lk); PROD[n]['secs'].append(sec)
for pk in PICKS:
    if pk['name'] in PROD: continue
    PROD[pk['name']] = dict(name=pk['name'], asin=pk.get('us'), aeasin=pk.get('ae'), blurb=pk['blurb'], lists=['picks'], secs=['Researched pick'], tags=pk['tags'], researched=True)
OWN = {"Smiggle Minecraft Trio Lunchbox", "Smiggle Spritz Spray Water Bottle"}
for row in P2:
    n, ua, aa, tg, bl = row[:5]
    if n in PROD: continue
    PROD[n] = dict(name=n, asin=ua, aeasin=aa, blurb=bl, lists=['picks'], secs=['Researched pick'], tags=tg, researched=n not in OWN, own=n in OWN, q=(row[5] if len(row) > 5 else None))
PROD['OmieBox Thermal Bento Box V2']['aeasin'] = 'B017SGIMV2'
for n, ua, aa, tg, bl, qq, bought in P3:
    if n in PROD: continue
    PROD[n] = dict(name=n, asin=ua, aeasin=aa, blurb=bl, lists=['picks'], secs=['Researched pick'], tags=tg, researched=not bought, bought=bought, q=qq)
for n in BOUGHT_EXISTING:
    if n in PROD: PROD[n]['bought'] = True
def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace("'", "")).strip('-')
for p in PROD.values(): p['id'] = slugify(p['name'])[:60]
def q(n): return re.sub(r'\s+', '+', re.sub(r"[()'&!:,]", ' ', n).strip())
def us(p): return f"https://www.amazon.com/dp/{p['asin']}?tag={US}" if p.get('asin') else f"https://www.amazon.com/s?k={q(p.get('q') or p['name'])}&tag={US}"
def ae(p): return f"https://www.amazon.ae/dp/{p['aeasin']}?tag={AE}" if p.get('aeasin') else f"https://www.amazon.ae/s?k={q(p.get('q') or p['name'])}&tag={AE}"
def tagged(t, extra=()): return [p for p in PROD.values() if t in p.get('tags', [])] + [PROD[n] for n in extra if n in PROD]

THEMES = [
 dict(slug="screen-free-activities-for-kids", name="Screen-free activities", emoji="📵", h1="Screen-free activities for kids that hold attention", desc="Screen-free activities for kids 3 to 10 that hold attention: building, puzzles, crafts and pretend play, picked by a busy mom.", secs=["The Quiet-Focus Crew", "The Makers & Creators", "The Storytellers & Pretenders"]),
 dict(slug="building-toys", name="Building toys", emoji="🧱", h1="Building toys for the kid who builds everything", desc="The best building toys for kids: Magna-Tiles, LEGO, marble runs, gears and engineering kits that hold attention.", secs=["The Builders & Engineers"]),
 dict(slug="sensory-toys-for-kids", name="Sensory & fidget", emoji="🫧", h1="Sensory and fidget toys kids actually use", desc="Sensory and fidget toys for kids: putty, squishies, NeeDoh, kinetic sand and bath play, for kids who need to squeeze or move to settle.", secs=["The Movers, Touchers & Splashers"]),
 dict(slug="family-board-games", name="Family games", emoji="🃏", h1="Family games the whole table can play", desc="Family card and board games for kids and adults: quick rounds, easy rules and travel-friendly picks.", names=["Catan: On the Road", "Skillmatics Train of Thought Card Game", "Sushi Go! Party Card Game", "Sleeping Queens Card Game", "Zingo! Bingo Game", "Spot It! Junior (Dobble)", "Shut the Box Dice Game (Travel Size)", "Melissa & Doug Suspend Balance Game", "GiiKER Tic-Tac-Toe Bolt", "Rory's Story Cubes Enchanted", "TableTopics Kids Question Cards", "Melissa & Doug Magnetic Travel Game Set"]),
 dict(slug="kitchen-gadgets-for-busy-moms", name="Kitchen shortcuts", emoji="🍲", h1="Kitchen gadgets for busy moms", desc="Kitchen gadgets and freezer prep tools that save time on weeknights: Instant Pot, air fryer, Souper Cubes, shears and more.", secs=["The Frozen Drawer", "The Emergency Shelf", "The 15-Minute Tools"]),
 dict(slug="travel-essentials-for-kids", name="Travel with kids", emoji="🧳", h1="Travel essentials for kids", desc="Travel essentials for kids: plane bag, hotel sleep help, road trip gear and beach day kit.", secs=["The Plane Bag", "The Hotel Comforts", "The Road Trip Kit", "The Beach or Pool Day", "The Mom Carry-On"]),
 dict(slug="lunchbox-ideas", name="Lunchbox", emoji="🍎", h1="Lunchbox gear and snacks for school", desc="Lunchbox gear and school snacks: bento boxes, prep tools, nut-free snacks and insulated bags.", secs=["The Box & Containers", "The Prep Tools", "The Snack Pantry", "The Sad-Lunch Saviors", "The Backpack Extras"]),
 dict(slug="self-care-gifts-for-moms", name="For mom", emoji="🌿", h1="Self-care gifts for moms (or for yourself)", desc="Self-care gifts for busy moms: good coffee, sleep help, hand cream, travel comfort and the small things that make a hard day lighter.", secs=["The Mom Reset", "The Mom Carry-On"]),
 dict(slug="smart-home-gadgets", name="Smart home & tech", emoji="💡", h1="Smart home gadgets and tech that help at home", desc="Smart home gadgets and tech for busy households: robot vacuum, smart lights, chargers and cable fixes.", secs=["Smart Home & Convenience", "Charging & Cables", "Travel Tech"]),
 dict(slug="diwali-decorations-and-essentials", name="Diwali", emoji="🪔", h1="Diwali essentials for celebrating away from home", desc="Diwali decorations, diyas, torans, puja essentials, mithai and kids' kurtas from Amazon.ae best sellers, for celebrating Diwali away from India.", tag="diwali", extra=["Amul Pure Cow Ghee", "MDH Chaat Masala", "Patak's Korma Paste"]),
 dict(slug="halloween-for-kids", name="Halloween", emoji="🎃", h1="Halloween for kids: costumes, glow and spooky books", desc="Easy Halloween costumes, glow sticks, LED masks, decor and spooky picture books for kids, from what's selling now.", tag="halloween"),
 dict(slug="thanksgiving-finds", name="Thanksgiving", emoji="🦃", h1="Thanksgiving finds for hosting a big table", desc="Thanksgiving hosting finds: food warming mat, meat thermometer, gravy separator, table decor and kids' Thanksgiving books.", tag="thanksgiving", extra=["Crock-Pot 7-Quart Slow Cooker", "TALES Conversation Cards Family Edition"]),
 dict(slug="minecraft-gifts", name="Minecraft", emoji="⛏️", h1="Minecraft gifts and finds for the obsessed kid", desc="Minecraft gifts kids love: LEGO Minecraft sets by age, plush, books, walkie talkies, a smartwatch and the Smiggle Minecraft lunchbox.", tag="minecraft"),
 dict(slug="kids-water-bottles", name="Water bottles", emoji="💧", h1="Water bottles for kids and moms that actually work", desc="Kids' and moms' water bottles: spray bottles, time-marker bottles, bottles with handles, football bottles, Owala, Hydro Flask and Stanley.", tag="bottles", extra=["Hydro Flask Kids 12 oz Wide Mouth Bottle", "Owala FreeSip Water Bottle 24 oz", "Stanley Quencher H2.0 Tumbler (40 oz)"]),
 dict(slug="kid-safe-gadgets", name="Kid-safe tech", emoji="🎧", h1="Kid-safe gadgets: no browsing, no ads, safe volume", desc="Kid-safe tech: Yoto, Tonies, volume-limited headphones, no-internet smartwatches, ok-to-wake clocks and kids' cameras.", tag="kidsafe", extra=["PuroQuiet Volume-Limited Kid Headphones", "Kindle Kids Edition", "Osmo Genius Starter Kit", "Kids Digital Camera (CIMELR)"]),
 dict(slug="natural-self-care", name="Natural self-care", emoji="🌸", h1="Natural-ingredient self-care for a two-minute reset", desc="Natural-ingredient self-care: rosewater and mogra mists, Ayurvedic oils, lavender roll-ons, shea hand cream and calming teas.", tag="calm", extra=["L'Occitane Shea Butter Hand Cream (75ml)", "Pukka Three Ginger Tea", "Alaska Bear Natural Silk Sleep Mask"]),
 dict(slug="home-organization", name="Home & organizing", emoji="🏠", h1="Home organizing finds for a busy family home", desc="Home organization finds: shoe stackers, storage ottomans, no-drill shelves and hooks, kitchen organizers and cable fixes. Many from our own orders.", tag="home"),
 dict(slug="indoor-plants", name="Indoor plants", emoji="🪴", h1="Indoor plant gear for AC apartments", desc="Indoor plant gear for air-conditioned apartments: propagation stations, LECA, self-watering pots, coco coir and potting soil.", tag="garden"),
 dict(slug="school-essentials", name="School essentials", emoji="🎒", h1="School essentials that save mornings", desc="Small school essentials: ID badge holders, school socks, light shoes, bag hooks, water bottles and lunch gear.", tag="school", extra=["Hydro Flask Kids 12 oz Wide Mouth Bottle", "Bentgo Kids Bento Box (5-compartment)", "PackIt Freezable Lunch Bag"]),
 dict(slug="sun-safe-kids", name="Sun safe", emoji="☀️", h1="Sun-safe gear for kids in hot climates", desc="Sun-safe gear for kids: UPF 50+ hats, rash guards, mineral sunscreen and insulated bottles.", tag="sun", extra=["Blue Lizard Sensitive Mineral SPF 50 Lotion", "UV Skinz UPF 50+ Kids Swim Shirt"]),
 dict(slug="pantry-favorites", name="Pantry", emoji="🫙", h1="Pantry favorites worth buying again", desc="Snacks, drinks and pantry staples worth buying again.", secs=["The Snack Edit", "The Drink Cabinet", "The Brands I'd Drive For"]),
]
def theme_items(t):
    if 'tag' in t: return [p for p in PROD.values() if t['tag'] in p.get('tags', [])] + [PROD[n] for n in t.get('extra', []) if n in PROD and t['tag'] not in PROD[n].get('tags', [])]
    if 'names' in t: return [PROD[n] for n in t['names'] if n in PROD]
    return [p for p in PROD.values() if any(s in t['secs'] for s in p['secs'])]

AGE = [
 dict(slug="gifts-for-8-year-olds", h1="Gifts for 8 year olds that actually get played with", title="Gifts for 8 Year Olds That Actually Get Played With", desc="Gift ideas for 8 year olds from a working mom: building, puzzles, science and games that hold attention. Shop on Amazon US or UAE.", lead="From our list of activities that kept the kids busy long enough for me to take a meeting or eat in peace.", names=["Snap Circuits Jr", "ThinkFun Gravity Maze", "Ravensburger GraviTrax Starter Set", "Gecko Kalimba 17-Key Thumb Piano", "Catan: On the Road", "Discovery Kids Illuminated Microscope", "SmartGames IQ Puzzler Pro", "Skillmatics Train of Thought Card Game", "Lego Architecture Skyline Series (age 8+)", "Klutz LEGO Chain Reactions", "Loog Mini Guitar (3-string)", "Fujifilm Instax Mini 12"]),
 dict(slug="stocking-stuffers-for-kids", h1="Stocking stuffers for kids that don't end up under the sofa", title="Stocking Stuffers for Kids: Small Gifts They Actually Use", desc="Small gifts and stocking stuffers for kids: NeeDoh, putty, squishies, travel games and more. Shop on Amazon US or UAE.", lead="Small gifts are where it usually goes wrong: plastic that breaks by lunch. These are the small things that keep getting used.", names=["Schylling NeeDoh Teenie", "Crazy Aaron's Thinking Putty", "Mochi Squishy 32-pack", "Slow Rebound Butter Squeeze Stress Balls", "Kinetic Sand 2lb Tub", "Crayola Model Magic", "Melissa & Doug Reusable Sticker Pads", "Mad Libs Junior Travel Pack", "Rory's Story Cubes Enchanted", "Shut the Box Dice Game (Travel Size)", "Crayola Bath Drop Color Tablets"]),
 dict(slug="gifts-for-kids-who-build", h1="Gifts for the kid who turns every table into a construction site", title="Gifts for Kids Who Build Everything", desc="Building toy gift ideas: Magna-Tiles, LEGO, marble runs, gears and circuits that hold attention. Shop on Amazon US or UAE.", lead="For the kid who builds before breakfast.", names=["Magna-Tiles Classic 100-piece", "LEGO Classic 11030 (1000 pieces)", "Ravensburger GraviTrax Starter Set", "Learning Resources Gears! Gears! Gears! Set", "ThinkFun Gravity Maze", "Snap Circuits Jr", "Thames & Kosmos Kids First Robot Engineer Kit", "LEGO Creator 3-in-1 Plane", "National Geographic Glowing Marble Run"]),
 dict(slug="travel-activities-for-kids", h1="Travel activities for kids that survive a long-haul flight", title="Travel Activities for Kids: What Survives a Long Flight", desc="Screen-free travel activities for kids that fit in a carry-on: travel games, mess-free markers, reusable stickers and puzzles.", lead="Long-haul flights are normal for us. These are the screen-free things that fit in a carry-on.", names=["Catan: On the Road", "Melissa & Doug Reusable Sticker Pads", "Crayola Color Wonder Mess-Free Markers", "SmartGames IQ Puzzler Pro", "Melissa & Doug Water Wow Reusable Activity Books", "YPLUS Magnetic Tangrams Puzzle", "Mad Libs Junior Travel Pack", "Melissa & Doug Magnetic Travel Game Set", "Cra-Z-Art Magna Doodle Travel Pro"]),
]
START = ["Magna-Tiles Classic 100-piece", "Instant Pot Duo 7-in-1 (6-Quart)", "PuroQuiet Volume-Limited Kid Headphones", "Bentgo Kids Bento Box (5-compartment)", "ThinkFun Gravity Maze", "Stanley Quencher H2.0 Tumbler (40 oz)", "Schylling NeeDoh Teenie", "Sushi Go! Party Card Game"]

CSS = open('style2.css').read()
JS = """<script>(function(){var d=document.documentElement,s;try{s=localStorage.getItem('mtt-store')}catch(e){}if(!s){var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}s=/Dubai|Muscat/.test(tz)||/-AE/i.test(navigator.language||'')?'ae':'us'}d.dataset.store=s;
document.addEventListener('click',function(e){var b=e.target.closest('[data-set-store]');if(!b)return;d.dataset.store=b.dataset.setStore;try{localStorage.setItem('mtt-store',b.dataset.setStore)}catch(e){}});})();</script>"""

def nav():
    return f"""<header class="top"><div class="wrap bar"><a class="logo" href="/" aria-label="Mom Tried These home">Mom Tried These</a>
<div class="store" role="group" aria-label="Choose your Amazon store">Shop in <button data-set-store="us" class="s-us">US</button><button data-set-store="ae" class="s-ae">UAE</button></div></div>
<nav class="wrap mainnav" aria-label="Main"><a href="/shop/">Shop all</a><a href="/whats-selling/">What&#39;s selling</a><a href="/lists/">Lists</a><a href="/themes/">Themes</a><a href="/gifts/">Gifts</a><a href="/moms-life/">Mom life</a><a href="/blog/">Blog</a><a href="/about/">About</a></nav></header>"""

def head(title, desc, path, ld=None, ogtype="website"):
    url = SITE + path
    if len(title) > 62 and title.endswith(" | Mom Tried These"): title = title[:-len(" | Mom Tried These")]
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="Mom Tried These"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="alternate" type="application/rss+xml" title="Mom Tried These" href="/feed.xml"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#FAF6F0">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap">
<style>{CSS}</style>{JS}{lds}</head><body>{nav()}"""

SIGNUP = """<section class="wrap signup" id="keepers"><div><p class="k">✉️ The Keepers</p><h2>One email a month. Only the good stuff.</h2><p>My monthly roundup of what we loved, what we returned and what's worth buying this month. No spam, unsubscribe any time.</p></div>
<form class="sform" method="post" action="/subscribe.php"><label class="sr" for="se">Email</label><input id="se" name="email" type="email" required placeholder="Your email" autocomplete="email"><label class="sr" for="sn">First name</label><input id="sn" name="name" placeholder="First name (optional)" autocomplete="given-name" maxlength="60"><label class="hp" aria-hidden="true">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label><input type="hidden" name="src" value=""><button class="btn" type="submit">Join The Keepers</button><p class="fine2">By joining you agree to get the monthly email. See <a href="/privacy/">privacy</a>.</p></form></section>
<script>document.querySelectorAll('.sform input[name=src]').forEach(function(i){i.value=location.pathname})</script>"""
FOOT = SIGNUP + f"""<section class="wrap follow"><div><h2>Follow along</h2><p>New finds land on Pinterest and Instagram first.</p></div><p class="row"><a class="btn" href="https://www.pinterest.com/momtriedthese/">Pinterest</a><a class="btn ghost" href="https://www.instagram.com/momtriedthese/">Instagram</a><a class="btn ghost" href="https://www.youtube.com/@MomTriedThese">YouTube</a></p></section>
<footer class="foot"><div class="wrap cols"><div><a class="logo" href="/">Mom Tried These</a><p>Only the ones I kept. An independent, mom-run site about the things that actually work in a busy house.</p></div>
<div><h3>Shop</h3><a href="/shop/">All products</a><a href="/lists/">By list</a><a href="/themes/">By theme</a><a href="/gifts/">Gift guides</a><a href="/bought-by-us/">Bought by us</a><a href="/whats-selling/">What's selling</a></div>
<div><h3>Read</h3><a href="/blog/">Blog</a><a href="/moms-life/">Mom life</a><a href="/30-day-test/">How I pick</a></div>
<div><h3>About</h3><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/disclosure/">Disclosure</a><a href="/privacy/">Privacy</a></div></div>
<p class="wrap fine">As an Amazon Associate I earn from qualifying purchases. Links to Amazon.com and Amazon.ae are affiliate links; buying through them costs you nothing extra. Prices and availability change, so check Amazon before you buy. &copy; 2026 Mom Tried These</p></footer></body></html>"""
NOTE = '<p class="note">Links go to Amazon. I may earn a small commission at no cost to you. <a href="/disclosure/">Details</a></p>'

def card(p, n=None, star=False):
    lk = p['lists'][0]; m = META[lk]
    initial = E(p['name'].split()[0].strip("'"))
    tag = f'<span class="tag start">Start here</span>' if star else ''
    num = f'<span class="n">{n}</span>' if n else ''
    if p.get('bought') and p['lists'][0] == 'picks':
        lab = '<span class="lab kept" title="In our own Amazon orders this year.">Bought by us</span>'
        frm = '<a class="from" href="/bought-by-us/">From our 2026 orders</a>'
    elif p.get('bought'):
        lab = '<span class="lab kept">On my list</span><span class="lab kept" title="In our own Amazon orders this year.">Bought by us</span>'
        frm = f'<a class="from" href="/lists/{lk}/">{E(m["short"])} · {E(p["secs"][0].replace("The ", ""))}</a>'
    elif p.get('own'):
        lab = '<span class="lab kept" title="We own and use this.">On my list</span>'
        frm = '<span class="from">Ours right now</span>'
    elif p.get('researched'):
        lab = '<span class="lab res" title="Picked from Amazon best-seller data. Not tested in our house yet.">Researched pick</span>'
        frm = '<a class="from" href="/whats-selling/">Trending on Amazon · Oct 2026</a>'
    else:
        lab = '<span class="lab kept" title="On my own list.">On my list</span>'
        frm = f'<a class="from" href="/lists/{lk}/">{E(m["short"])} · {E(p["secs"][0].replace("The ", ""))}</a>'
    return f"""<article class="card" id="{p['id']}" data-lists="{' '.join(p['lists'])}" data-name="{E(p['name'].lower())}"><div class="vis" style="background:{m['color']}">{num}<span class="em" aria-hidden="true">{m['emoji']}</span><span class="init">{initial}</span></div>
<div class="cb"><div class="labs">{tag}{lab}</div>{frm}<h3>{E(p['name'])}</h3><p>{E(p['blurb'])}</p>
<div class="buy"><a class="btn us" rel="sponsored nofollow noopener" target="_blank" href="{us(p)}">Check price on Amazon</a><a class="btn ae" rel="sponsored nofollow noopener" target="_blank" href="{ae(p)}">Check price on Amazon.ae</a><a class="alt us" rel="sponsored nofollow noopener" target="_blank" href="{ae(p)}">In the UAE? Amazon.ae</a><a class="alt ae" rel="sponsored nofollow noopener" target="_blank" href="{us(p)}">In the US? Amazon.com</a></div></div></article>"""

def crumbs(path, items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
    h = '<nav class="crumb" aria-label="Breadcrumb">' + ' / '.join(f'<a href="{u}">{E(n)}</a>' if i < len(items) - 1 else E(n) for i, (n, u) in enumerate(items)) + '</nav>'
    return h, ld
def itemlist(ps, path): return {"@context": "https://schema.org", "@type": "ItemList", "numberOfItems": len(ps), "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p['name'], "url": f"{SITE}{path}#{p['id']}"} for i, p in enumerate(ps)]}
URLS = []
def write(path, content):
    assert '—' not in content, path
    d = 'out2' + path; os.makedirs(d, exist_ok=True); open(d + 'index.html', 'w').write(content); URLS.append(path)

shutil.rmtree('out2', ignore_errors=True)
# ---- List pages
for lk in ORDER:
    L = LISTS[lk]; m = META[lk]; path = f"/lists/{lk}/"
    secs = [(s, [PROD[n] for n in ns if n in PROD]) for s, ns in L['sections'].items()]
    allp = [p for _, ps in secs for p in ps]
    ch, cld = crumbs(path, [("Home", "/"), ("Lists", "/lists/"), (m['short'], path)])
    jump = ''.join(f'<a href="#{slugify(s)}">{E(s.replace("The ", ""))} <span>{len(ps)}</span></a>' for s, ps in secs)
    body = f"""<main class="wrap">{ch}<header class="phead"><p class="k">{m['emoji']} The list · {len(allp)} picks</p><h1>{E(L['title'])}</h1><p class="lead">{E(L['intro'])}</p><p class="upd">Updated {TODAY_H}</p></header>
<nav class="jump" aria-label="Sections">{jump}</nav>{NOTE}"""
    for s, ps in secs:
        body += f'<section class="sec" id="{slugify(s)}"><h2>{E(s)}</h2><div class="cards">' + ''.join(card(p, star=(i == 0)) for i, p in enumerate(ps)) + '</div></section>'
    others = ''.join(f'<a class="mini" href="/lists/{o}/">{META[o]["emoji"]} {E(META[o]["short"])}</a>' for o in ORDER if o != lk)
    body += f'<section class="sec"><h2>More lists</h2><div class="minis">{others}</div></section></main>'
    write(path, head(m['seo'] + " | Mom Tried These", m['desc'], path, [cld, itemlist(allp, path)]) + body + FOOT)
# Lists hub
path = "/lists/"; ch, cld = crumbs(path, [("Home", "/"), ("Lists", path)])
tiles = ''.join(f'<a class="tile" href="/lists/{lk}/" style="--c:{META[lk]["color"]}"><span class="em">{META[lk]["emoji"]}</span><span class="k">{sum(len([n for n in v if n in PROD]) for v in LISTS[lk]["sections"].values())} picks</span><h2>{E(LISTS[lk]["title"])}</h2><p>{E(LISTS[lk]["intro"][:140].rsplit(" ",1)[0])}...</p></a>' for lk in ORDER)
write(path, head("Shop by List: Every Mom Tried These List | Mom Tried These", "Every Mom Tried These list in one place: kid activities, the survival box, travel day, the 10-minute lunchbox, playdates, tech and the pantry edit.", path, [cld]) + f'<main class="wrap">{ch}<header class="phead"><h1>Shop by list</h1><p class="lead">Each list solves one real problem in a busy house. Start with the one that matches your week.</p></header><div class="tiles">{tiles}</div></main>' + FOOT)
# ---- Theme pages
for t in THEMES:
    path = f"/themes/{t['slug']}/"; ps = theme_items(t)
    ch, cld = crumbs(path, [("Home", "/"), ("Themes", "/themes/"), (t['name'], path)])
    body = f'<main class="wrap">{ch}<header class="phead"><p class="k">{t["emoji"]} Theme · {len(ps)} picks</p><h1>{E(t["h1"])}</h1><p class="lead">{E(t["desc"])}</p><p class="upd">Updated {TODAY_H}</p></header>{NOTE}<div class="cards">' + ''.join(card(p, i + 1) for i, p in enumerate(ps)) + '</div>'
    body += '<section class="sec"><h2>More themes</h2><div class="minis">' + ''.join(f'<a class="mini" href="/themes/{o["slug"]}/">{o["emoji"]} {E(o["name"])}</a>' for o in THEMES if o is not t) + '</div></section></main>'
    write(path, head(t['h1'][0].upper() + t['h1'][1:] + " | Mom Tried These", t['desc'], path, [cld, itemlist(ps, path)]) + body + FOOT)
path = "/themes/"; ch, cld = crumbs(path, [("Home", "/"), ("Themes", path)])
write(path, head("Shop by Theme | Mom Tried These", "Shop Mom Tried These by theme: screen-free activities, building toys, sensory toys, family games, kitchen shortcuts, travel, lunchbox, self-care and more.", path, [cld]) + f'<main class="wrap">{ch}<header class="phead"><h1>Shop by theme</h1><p class="lead">The same picks, sorted by what you need them for.</p></header><div class="tiles">' + ''.join(f'<a class="tile" href="/themes/{t["slug"]}/"><span class="em">{t["emoji"]}</span><span class="k">{len(theme_items(t))} picks</span><h2>{E(t["name"])}</h2><p>{E(t["desc"][:120].rsplit(" ",1)[0])}...</p></a>' for t in THEMES) + '</div></main>' + FOOT)

def age_names(a, base, cap=16):
    out=[n for n in base if n in PROD]
    for p in PROD.values():
        if a in p.get('tags',[]) and p['name'] not in out: out.append(p['name'])
    return out[:cap]
for g in AGE:
    if g['slug']=='gifts-for-8-year-olds': g['names']=age_names('8', g['names'], 20)
    if g['slug']=='stocking-stuffers-for-kids': g['names']=age_names('stocking', g['names'], 22)
AGEX = [
 ('5', ["Magna-Tiles Classic 100-piece","Kinetic Sand 2lb Tub","Melissa & Doug Water Wow Reusable Activity Books","Zingo! Bingo Game","Spot It! Junior (Dobble)","Play-Doh Fun Factory Mega Set","Crayola Color Wonder Mess-Free Markers","Insect Lore Live Butterfly Garden","LEGO Medium Creative Brick Box 10696","Folkmanis Tyrannosaurus Rex Hand Puppet"], "Gifts for 5 year olds that hold attention", "Gift ideas for 5 year olds that hold attention: magnetic tiles, mess-free art, first games and pretend play. Shop on Amazon US or UAE."),
 ('6', ["LEGO Creator 3-in-1 Plane","ThinkFun Rush Hour","Sleeping Queens Card Game","Crayola Ultimate Light Board","Calico Critters Family Set","Micro Maxi Kids Kickboard Scooter","Spirograph Deluxe Design Set","Magna-Tiles Classic 100-piece"], "Gifts for 6 year olds they won't outgrow by spring", "Gift ideas for 6 year olds: first LEGO sets, logic puzzles, card games and creative kits. Shop on Amazon US or UAE."),
 ('7', ["Catan: On the Road","Gecko Kalimba 17-Key Thumb Piano","The Klutz Book of Paper Airplanes","SmartGames IQ Puzzler Pro","Friendship Bracelet Making Kit","LEGO City Express Passenger Train","Rory's Story Cubes Enchanted"], "Gifts for 7 year olds that keep them busy", "Gift ideas for 7 year olds: building sets, travel games, music, crafts and puzzles. Shop on Amazon US or UAE."),
 ('9', ["Snap Circuits Jr","ThinkFun Gravity Maze","Lego Architecture Skyline Series (age 8+)","Fujifilm Instax Mini 12","Loog Mini Guitar (3-string)","Klutz LEGO Chain Reactions"], "Gifts for 9 year olds who think they're too old for toys", "Gift ideas for 9 year olds: STEM kits, strategy card games, cameras, music and big LEGO builds. Shop on Amazon US or UAE."),
 ('10', ["Lego Architecture Skyline Series (age 8+)","Fujifilm Instax Mini 12","Perler Beads Mega Activity Bucket","Catan: On the Road","Tektalk 2000 Piece Foldable Puzzle Board","Snap Circuits Jr"], "Gifts for 10 year olds that aren't another screen", "Gift ideas for 10 year olds: strategy games, STEM builds, cameras and creative kits that aren't another screen. Shop on Amazon US or UAE."),
]
for a, base, h1, desc in AGEX:
    AGE.insert(0 if a=='5' else len(AGE), dict(slug=f"gifts-for-{a}-year-olds", h1=h1, title=h1[0].upper()+h1[1:], desc=desc, lead=f"A mix of things from my own lists and what's selling right now for {a} year olds. Each card says which is which.", names=age_names(a, base)))
AGE.sort(key=lambda g: (0, int(re.search(r'(\d+)', g['slug']).group(1))) if re.search(r'gifts-for-\d+', g['slug']) else (1, 0))
AGE.append(dict(slug="christmas-gifts-for-kids-2026", h1="Christmas gifts for kids 2026: what's actually selling", title="Christmas Gifts for Kids 2026: What's Actually Selling", desc="Christmas gift ideas for kids 2026 from Amazon US and UAE best sellers plus a mom's own list: LEGO advent calendars, STEM kits, games and books.", lead="Built from what's climbing Amazon's charts this month plus the things that earned a place in our house. Advent calendars sell out first.", names=age_names('xmas', ["Magna-Tiles Classic 100-piece","Snap Circuits Jr","Ravensburger GraviTrax Starter Set","Fujifilm Instax Mini 12"], 24)))
AGE.append(dict(slug="birthday-return-gifts", h1="Birthday return gifts and party favors kids actually keep", title="Birthday Return Gifts and Party Favors Kids Actually Keep", desc="Return gifts and party favor ideas for kids' birthday parties: squishies, Play-Doh, sticker books, bracelet kits and small card games.", lead="Small things kids use after the party, not plastic that breaks in the car.", names=age_names('party', ["Schylling NeeDoh Teenie","Mochi Squishy 32-pack","Slow Rebound Butter Squeeze Stress Balls","Melissa & Doug Reusable Sticker Pads"], 18)))
# ---- Gift guides
for g in AGE:
    path = f"/{g['slug']}/"; ps = [PROD[n] for n in g['names'] if n in PROD]
    ch, cld = crumbs(path, [("Home", "/"), ("Gifts", "/gifts/"), (g['title'], path)])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g['h1'], "datePublished": "2026-10-27", "dateModified": TODAY, "author": {"@type": "Organization", "name": "Mom Tried These", "url": SITE + "/about/"}, "publisher": {"@type": "Organization", "name": "Mom Tried These"}, "image": SITE + "/og.jpg"}
    body = f'<main class="wrap">{ch}<header class="phead"><p class="k">🎁 Gift guide · {len(ps)} picks</p><h1>{E(g["h1"])}</h1><p class="lead">{E(g["lead"])}</p><p class="upd">Updated {TODAY_H}</p></header>{NOTE}<div class="cards">' + ''.join(card(p, i + 1) for i, p in enumerate(ps)) + '</div>'
    body += '<section class="sec"><h2>More gift guides</h2><div class="minis">' + ''.join(f'<a class="mini" href="/{o["slug"]}/">🎁 {E(o["title"])}</a>' for o in AGE if o is not g) + '</div></section></main>'
    write(path, head(g['title'] + " | Mom Tried These", g['desc'], path, [cld, art, itemlist(ps, path)], "article") + body + FOOT)
path = "/gifts/"; ch, cld = crumbs(path, [("Home", "/"), ("Gifts", path)])
write(path, head("Gift Guides for Kids and Moms | Mom Tried These", "Gift guides from a busy mom: gifts for 8 year olds, stocking stuffers, gifts for kids who build, travel activities and self-care gifts for moms.", path, [cld]) + f'<main class="wrap">{ch}<header class="phead"><h1>Gift guides</h1><p class="lead">Gifts that get used after the wrapping paper is gone.</p></header><div class="tiles">' + ''.join(f'<a class="tile" href="/{g["slug"]}/"><span class="em">🎁</span><span class="k">{len(g["names"])} picks</span><h2>{E(g["title"])}</h2><p>{E(g["lead"])}</p></a>' for g in AGE) + f'<a class="tile" href="/themes/self-care-gifts-for-moms/"><span class="em">🌿</span><span class="k">For mom</span><h2>Self-care gifts for moms</h2><p>The small things that make a hard day lighter.</p></a></div></main>' + FOOT)
# ---- Blog
def render_post_body(b):
    def rep(mo):
        n = mo.group(1); return card(PROD[n]) if n in PROD else ''
    return usp(re.sub(r'\[\[(.+?)\]\]', rep, b))
for po in POSTS:
    path = f"/blog/{po['slug']}/"; ch, cld = crumbs(path, [("Home", "/"), ("Blog", "/blog/"), (po['title'], path)])
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": po['title'], "description": po['desc'], "datePublished": po['date'], "dateModified": TODAY, "author": {"@type": "Organization", "name": "Mom Tried These", "url": SITE + "/about/"}, "publisher": {"@type": "Organization", "name": "Mom Tried These"}, "image": SITE + "/og.jpg", "mainEntityOfPage": SITE + path}
    rel = ''.join(f'<a class="post" href="/blog/{o["slug"]}/"><span class="k">{o["cat"]}</span><h3>{E(o["title"])}</h3></a>' for o in ([x for x in POSTS if x["cat"]==po["cat"] and x is not po][:3] + [x for x in POSTS[::-1] if x["cat"]!=po["cat"]][:3]))
    body = f'<main class="wrap"><article class="prose post-body">{ch}<p class="k">{po["cat"]} · {TODAY_H}</p><h1>{E(po["title"])}</h1><p class="lead">{E(usp(po["lead"]))}</p>{NOTE if "[[" in po["body"] else ""}{render_post_body(po["body"])}</article><section class="sec"><h2>Keep reading</h2><div class="posts">{rel}</div></section></main>'
    write(path, head(po['title'] + " | Mom Tried These", po['desc'], path, [cld, art], "article") + body + FOOT)
path = "/blog/"; ch, cld = crumbs(path, [("Home", "/"), ("Blog", path)])
postcards = lambda ps: ''.join(f'<a class="post" href="/blog/{o["slug"]}/"><span class="k">{o["cat"]}</span><h3>{E(o["title"])}</h3><p>{E(usp(o["lead"])[:130].rsplit(" ",1)[0])}...</p><span class="more">Read</span></a>' for o in ps)
write(path, head("The Blog: Real Fixes for a Busy House | Mom Tried These", "Practical posts from a working mom: school lunches, travel with kids, playdates, kitchen shortcuts and the tech that helps.", path, [cld]) + f'<main class="wrap">{ch}<header class="phead"><h1>The blog</h1><p class="lead">Short, practical posts. One problem, the fix, the things that help.</p></header><div class="chips" id="bc">' + '<button class="chip on" data-c="all">All</button>' + ''.join(f'<button class="chip" data-c="{c}">{c}</button>' for c in sorted(set(o["cat"] for o in POSTS))) + f'</div><div class="posts" id="bp">{postcards(POSTS[::-1])}</div></main><script>(function(){{var b=document.querySelectorAll("#bc .chip"),p=document.querySelectorAll("#bp .post");b.forEach(function(x){{x.onclick=function(){{b.forEach(function(y){{y.classList.toggle("on",y===x)}});p.forEach(function(q){{q.hidden=!(x.dataset.c=="all"||q.querySelector(".k").textContent==x.dataset.c)}})}}}})}})();</script>' + FOOT)
# ---- Mom life hub
path = "/moms-life/"; ch, cld = crumbs(path, [("Home", "/"), ("Mom life", path)])
mom = [p for p in PROD.values() if any(s in ("The Mom Reset", "The Mom Carry-On") for s in p['secs'])]
kit = [p for p in PROD.values() if any(s in ("The 15-Minute Tools", "The Frozen Drawer") for s in p['secs'])]
body = f"""<main class="wrap">{ch}<header class="phead"><p class="k">🌿 Mom life</p><h1>For the mom running the whole show</h1><p class="lead">The kids get most of this site. This corner is for you: the coffee, the sleep, the kitchen shortcuts and the backup plans that make the week work.</p></header>
<section class="sec"><h2>Read first</h2><div class="posts">{postcards([p for p in POSTS if p['cat'] == 'Mom life'] + [POSTS[1]] + [p for p in POSTS if p['slug']=='diwali-away-from-home'])}</div></section>{NOTE}
<section class="sec"><h2>The mom reset</h2><div class="cards">{''.join(card(p) for p in mom)}</div></section>
<section class="sec"><h2>Kitchen shortcuts</h2><div class="cards">{''.join(card(p) for p in kit)}</div></section>
<section class="sec"><h2>More for the house</h2><div class="minis"><a class="mini" href="/lists/survival-box/">🧊 The Survival Box</a><a class="mini" href="/lists/pantry/">☕ The Pantry Edit</a><a class="mini" href="/lists/tech/">🔌 Tech &amp; Gadgets</a><a class="mini" href="/themes/self-care-gifts-for-moms/">🌿 Self-care gifts</a></div></section></main>"""
write(path, head("Mom Life: Self-Care, Kitchen Shortcuts and Backup Plans | Mom Tried These", "For busy moms: self-care picks, kitchen shortcuts, freezer prep and the backup plans that keep the week running.", path, [cld, itemlist(mom + kit, path)]) + body + FOOT)
# ---- Shop all
path = "/shop/"; ch, cld = crumbs(path, [("Home", "/"), ("Shop all", path)])
allp = sorted(PROD.values(), key=lambda p: p['name'].lower())
chips = '<button class="chip on" data-f="all">All <span>' + str(len(allp)) + '</span></button>' + ''.join(f'<button class="chip" data-f="{lk}">{META[lk]["emoji"]} {E(META[lk]["short"])}</button>' for lk in ['picks']+ORDER)
filt = """<script>(function(){var q=document.getElementById('q'),f='all',cs=[].slice.call(document.querySelectorAll('.card')),c=document.getElementById('count');function run(){var t=(q.value||'').toLowerCase().trim(),n=0;cs.forEach(function(x){var ok=(f=='all'||x.dataset.lists.split(' ').indexOf(f)>-1)&&(!t||x.dataset.name.indexOf(t)>-1);x.hidden=!ok;if(ok)n++});c.textContent=n+' products'}q.addEventListener('input',run);try{var u=new URLSearchParams(location.search).get('q');if(u){q.value=u;run()}}catch(e){}[].forEach.call(document.querySelectorAll('.chip'),function(b){b.addEventListener('click',function(){f=b.dataset.f;[].forEach.call(document.querySelectorAll('.chip'),function(o){o.classList.toggle('on',o===b)});run()})});})();</script>"""
body = f'<main class="wrap">{ch}<header class="phead"><h1>Shop everything</h1><p class="lead">Every product from every list, A to Z. Search by name or filter by list.</p></header><div class="filters"><label class="search"><span class="sr">Search products</span><input id="q" type="search" placeholder="Search: LEGO, lunchbox, kettle..." autocomplete="off"></label><div class="chips">{chips}</div><p id="count" class="upd">{len(allp)} products</p></div>{NOTE}<div class="cards">' + ''.join(card(p) for p in allp) + f'</div></main>{filt}'
write(path, head(f"Shop All {len(allp)} Picks | Mom Tried These", f"All {len(allp)} Mom Tried These picks in one place: kids activities, travel, lunchbox, kitchen, tech and pantry. Search and filter, then shop on Amazon US or UAE.", path, [cld]) + body + FOOT)

# ---- What's selling
path = "/whats-selling/"; ch, cld = crumbs(path, [("Home", "/"), ("What's selling", path)])
GROUPS=[("games","🃏 Family games"),("build","🧱 Building"),("stem","🔬 STEM and puzzles"),("art","🎨 Art and craft"),("sensory","🫧 Sensory and fidget"),("tech","📷 Kids' tech"),("books","📚 Books"),("mom","🌿 For mom"),("kitchen","🍲 Kitchen"),("minecraft","⛏️ Minecraft"),("bottles","💧 Water bottles"),("kidsafe","🎧 Kid-safe tech"),("travel","🧳 Travel"),("calm","🌸 Natural self-care")]
seen=set(); body=f'<main class="wrap">{ch}<header class="phead"><p class="k">📈 Updated {TODAY_H}</p><h1>What\'s selling right now</h1><p class="lead">What other parents are buying this month, pulled from the Amazon US and Amazon.ae best-seller charts and filtered for kids 5 to 10 and busy moms. These are researched picks, not things I\'ve tested. Anything from my own lists says so.</p></header>{NOTE}'
body += '<nav class="jump">' + ''.join(f'<a href="#{t}">{n}</a>' for t,n in GROUPS) + '</nav>'
for t,n in GROUPS:
    ps=[p for p in PROD.values() if p.get('researched') and t in p.get('tags',[]) and p['name'] not in seen]
    seen.update(p['name'] for p in ps)
    if ps: body += f'<section class="sec" id="{t}"><h2>{n}</h2><div class="cards">' + ''.join(card(p) for p in ps) + '</div></section>'
body += '<section class="sec"><h2>Read next</h2><div class="minis"><a class="mini" href="/christmas-gifts-for-kids-2026/">🎄 Christmas gifts 2026</a><a class="mini" href="/blog/lego-advent-calendars-2026/">LEGO advent calendars 2026</a><a class="mini" href="/blog/best-family-card-games/">Best family card games</a><a class="mini" href="/birthday-return-gifts/">🎈 Return gifts</a></div></section></main>'
allres=[p for p in PROD.values() if p.get('researched')]
write(path, head("What's Selling Now: Trending Kids Gifts and Mom Finds | Mom Tried These", "What parents are buying this month on Amazon US and UAE, filtered for kids 5 to 10 and busy moms: games, LEGO, STEM, art, books and mom finds.", path, [cld, itemlist(allres, path)]) + body + FOOT)
# ---- Bought by us
path = "/bought-by-us/"; ch, cld = crumbs(path, [("Home", "/"), ("Bought by us", path)])
bps = [p for p in PROD.values() if p.get('bought')]
write(path, head("Things We Actually Bought (2026) | Mom Tried These", "The real list: kids' toys, school stuff, kitchen and home finds from our own Amazon orders in 2026. No sponsored picks.", path, [cld, itemlist(bps, path)]) + f'<main class="wrap">{ch}<header class="phead"><p class="k">🧾 From our own orders</p><h1>Things we actually bought this year</h1><p class="lead">Straight from our 2026 Amazon orders. Toys, school stuff, the kitchen, the home. If it\'s here, we paid for it. Full reviews are coming as we live with them.</p></header>{NOTE}<div class="cards">' + ''.join(card(p) for p in bps) + '</div></main>' + FOOT)
# ---- Home
sp = [PROD[n] for n in START]
ld_org = {"@context": "https://schema.org", "@type": "Organization", "name": "Mom Tried These", "url": SITE, "logo": SITE + "/favicon.svg", "sameAs": ["https://www.pinterest.com/momtriedthese/", "https://www.instagram.com/momtriedthese/", "https://www.youtube.com/@MomTriedThese", "https://benable.com/momtriedthese"]}
ld_site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Mom Tried These", "url": SITE, "potentialAction": {"@type": "SearchAction", "target": SITE + "/shop/?q={search_term_string}", "query-input": "required name=search_term_string"}}
ltiles = ''.join(f'<a class="tile" href="/lists/{lk}/" style="--c:{META[lk]["color"]}"><span class="em">{META[lk]["emoji"]}</span><span class="k">{sum(len([n for n in v if n in PROD]) for v in LISTS[lk]["sections"].values())} picks</span><h3>{E(META[lk]["short"])}</h3></a>' for lk in ORDER)
tchips = ''.join(f'<a class="mini" href="/themes/{t["slug"]}/">{t["emoji"]} {E(t["name"])}</a>' for t in THEMES)
home = f"""<main><section class="hero"><div class="wrap"><p class="k">Only the ones I kept</p><h1>The things that actually work in a busy house.</h1><p class="lead">I'm a working mom who travels, cooks and runs a house that runs on backup plans. These are the products that stayed: for the kids, the kitchen, the trip and for me.</p>
<p class="row"><a class="btn" href="/shop/">Shop all {len(PROD)} picks</a><a class="btn ghost" href="/blog/">Read the blog</a></p>
<ul class="trust"><li>{len(PROD)} picks across 7 lists</li><li>Shop Amazon US or UAE</li><li>No paid placements</li></ul></div></section>
<div class="wrap"><section class="sec"><div class="sh"><h2>Shop by list</h2><a href="/lists/">All lists</a></div><div class="tiles small">{ltiles}</div></section>
<section class="sec"><div class="sh"><h2>Shop by theme</h2><a href="/themes/">All themes</a></div><div class="minis">{tchips}</div></section>
<section class="sec"><div class="sh"><h2>Start here</h2><a href="/shop/">Shop all</a></div><p class="sub">One pick from each corner of the house. If you only buy one thing this month, look here first.</p>{NOTE}<div class="cards">{''.join(card(p, i+1) for i, p in enumerate(sp))}</div></section>
<section class="sec"><div class="sh"><h2>Coming up</h2><a href="/blog/">All posts</a></div><div class="seasons">
<a class="season" href="/blog/diwali-away-from-home/" style="--c:#F6E2C6"><span class="em">🪔</span><span class="k">Diwali · 8 Nov</span><h3>Feel at home this Diwali, even far away</h3><p>30 top sellers: diyas, torans, mithai, kurtas.</p></a>
<a class="season" href="/blog/halloween-top-20-picks/" style="--c:#EFE0D2"><span class="em">🎃</span><span class="k">Halloween · 31 Oct</span><h3>My top 20 Halloween picks</h3><p>Glow, easy costumes, spooky books.</p></a>
<a class="season" href="/christmas-gifts-for-kids-2026/" style="--c:#E3EADF"><span class="em">🎄</span><span class="k">Christmas 2026</span><h3>Christmas gifts that are actually selling</h3><p>Advent calendars sell out first.</p></a>
<a class="season" href="/blog/unique-thanksgiving-products/" style="--c:#EDE3D5"><span class="em">🦃</span><span class="k">Thanksgiving · 26 Nov</span><h3>Unique Thanksgiving finds</h3><p>Clever things for a big table.</p></a></div></section>
<section class="sec"><div class="sh"><h2>What's selling now</h2><a href="/whats-selling/">See all</a></div><p class="sub">Trending on Amazon US and UAE this month, filtered for kids 5 to 10. Researched, not tested.</p><div class="cards">{''.join(card(PROD[n]) for n in ["UNO Card Game","Flip 7 Card Game","Klutz LEGO Gear Bots","CrunchLabs Crunchinator by Mark Rober","Air Dry Clay Set, 36 Colors","Diary of a Wimpy Kid: Fight or Flight (Book 21)","Kids Karaoke Machine with 2 Mics","Owala FreeSip Water Bottle 24 oz"])}</div></section>
<section class="sec"><div class="sh"><h2>Gifts by age</h2><a href="/gifts/">All gift guides</a></div><div class="minis">{''.join(f'<a class="mini" href="/gifts-for-{a}-year-olds/">🎁 Age {a}</a>' for a in [5,6,7,8,9,10])}<a class="mini" href="/stocking-stuffers-for-kids/">🧦 Stocking stuffers</a><a class="mini" href="/birthday-return-gifts/">🎈 Return gifts</a></div></section>
<section class="sec"><div class="sh"><h2>Bought by us</h2><a href="/bought-by-us/">See all</a></div><p class="sub">From our own 2026 orders. We paid for these.</p><div class="cards">{''.join(card(PROD[n]) for n in ["Cast Iron Paniyaram (Appe) Pan","GiiKER Tic-Tac-Toe Bolt","TOYBY Storage Ottoman Cube","Hotel-Inspired Scent Diffuser Oil Refill (2 x 500ml)"])}</div></section>
<section class="sec"><div class="sh"><h2>Notes for moms</h2><a href="/blog/">All posts</a></div><div class="posts">{postcards([o for o in POSTS if o["cat"]=="Mom notes"][:3])}</div></section>
<section class="sec band"><div><p class="k">🌿 Mom life</p><h2>For the mom running the whole show</h2><p>Coffee, sleep, kitchen shortcuts and the backup plan for the day help doesn't show up.</p><a class="btn" href="/moms-life/">Go to Mom life</a></div></section>
<section class="sec"><div class="sh"><h2>From the blog</h2><a href="/blog/">All posts</a></div><div class="posts">{postcards(POSTS[::-1][:6])}</div></section>
<section class="sec"><div class="sh"><h2>Gift guides</h2><a href="/gifts/">All gift guides</a></div><div class="minis">{''.join(f'<a class="mini" href="/{g["slug"]}/">🎁 {E(g["title"])}</a>' for g in AGE)}</div></section></div></main>"""
write("/", head("Mom Tried These: Only the Ones I Kept", f"A working mom's picks for kids activities, travel, school lunches, kitchen shortcuts and self-care. {len(PROD)} products that stayed. Shop on Amazon US or UAE.", "/", [ld_org, ld_site]) + home + FOOT)
# ---- Simple pages
CONTACT = """<form class="form" method="post" action="/contact.php"><label>Your name<input name="name" required maxlength="100" autocomplete="name"></label><label>Email<input name="email" type="email" required maxlength="200" autocomplete="email"></label>
<label>What's this about?<select name="topic"><option>A product question</option><option>Suggest a product</option><option>Brand or collaboration</option><option>Something else</option></select></label><label>Message<textarea name="message" required rows="6" maxlength="4000"></textarea></label>
<label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label><button class="btn" type="submit">Send message</button><p class="upd">I read every message. Replies usually within a few days.</p></form>"""
SIMPLE = {
 "/about/": ("About the Mom Behind Mom Tried These", "About Mom Tried These: an independent, mom-run site of products that earned a place in a busy house.", """<h1>About</h1><p class="lead">Hi. I'm the mom behind Mom Tried These.</p><p>I work from home. I travel for work. I parent. Some days all three before lunch.</p><p>I run the house a bit like a project. Milestones, checkpoints, a running list of what worked and what didn't. Crazy, I know. But hey, here I am!</p><p>This site is that list, made public. The activities that bought me a meeting. The lunchbox system that ended the morning panic. The travel kit we actually fly with. The coffee and the hand cream that make me feel human again.</p><p>The rule is simple: <strong>only the ones I kept</strong>. If it stopped getting used, it's off the list. No exceptions, no sentimental keeping. Read more on <a href="/30-day-test/">how I pick</a>.</p><h2>How this site makes money</h2><p>When you buy through a link here, Amazon may pay me a small commission. It costs you nothing extra, and it never decides what goes on a list. No brand pays for a spot. Ever. <a href="/disclosure/">Full disclosure</a>.</p><h2>Say hello</h2><p>Questions, a product you think I should try, or a brand enquiry: <a href="/contact/">write to me here</a>, or find me on <a href="https://www.instagram.com/momtriedthese/">Instagram</a> and <a href="https://www.pinterest.com/momtriedthese/">Pinterest</a>.</p>"""),
 "/contact/": ("Contact", "Contact Mom Tried These with a product question, a suggestion or a brand enquiry.", "<h1>Contact</h1><p class=\"lead\">Have a question about a product, something you think belongs on a list, or a brand enquiry? Send it here.</p>" + CONTACT),
 "/subscribed/": ("You're in | Mom Tried These", "Thanks for joining The Keepers.", '<h1>You\'re in</h1><p class="lead">Welcome to The Keepers. The first roundup lands at the start of next month.</p><p class="row"><a class="btn" href="/whats-selling/">See what\'s selling now</a><a class="btn ghost" href="/blog/">Read the blog</a></p>'),
 "/contact/thanks/": ("Message sent | Mom Tried These", "Thanks for your message.", '<h1>Thank you</h1><p class="lead">Your message is on its way. I read every one.</p><p><a class="btn" href="/shop/">Back to the picks</a></p>'),
 "/30-day-test/": ("How I Pick: The 30-Day Test | Mom Tried These", "How Mom Tried These picks products: it has to keep earning its place in a real house.", """<h1>How I pick</h1><p class="lead">A product stays on this site only if it keeps earning its place in our house.</p><p>It has to do at least one of three things: save time, end a daily fight, or give real relief. Looks don't count. Hype doesn't count. If the kids stop reaching for it, or I stop using it, it comes off the list.</p><p>The goal is the 30-Day Test: a thing has to survive a month of normal life before I'll tell you it works.</p><h2>Two labels, so you always know</h2><ul><li><strong>On my list:</strong> it lives in our house and earned its place.</li><li><strong>Researched pick:</strong> chosen from what other parents are buying (Amazon US and UAE best-seller charts), with ratings and reviews checked. Not tested by me yet. If it passes, it gets promoted to my list. If it doesn't, I'll say so.</li></ul><h2>What I don't do</h2><ul><li>No brand pays to be on a list.</li><li>No made-up reviews or testimonials.</li><li>Product descriptions say what a thing is and what it's for. Personal notes are mine.</li></ul><p>Amazon prices and stock change often, so always check the product page before you buy.</p>"""),
 "/disclosure/": ("Affiliate Disclosure | Mom Tried These", "Mom Tried These affiliate disclosure: we earn from qualifying Amazon purchases.", """<h1>Affiliate disclosure</h1><p>Mom Tried These participates in the Amazon Services LLC Associates Program and the Amazon.ae Associates Program, affiliate advertising programs designed to provide a means for sites to earn fees by linking to Amazon.com and Amazon.ae.</p><p><strong>As an Amazon Associate I earn from qualifying purchases.</strong> When you click a link and buy, I may earn a small commission at no extra cost to you. This never changes which products are recommended.</p><p>Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.</p>"""),
 "/privacy/": ("Privacy Policy | Mom Tried These", "Privacy policy for Mom Tried These: what we store, cookies, Amazon links, the contact form and The Keepers email list.", """<h1>Privacy</h1><p>This site does not set its own tracking cookies. It remembers your store choice (US or UAE) in your own browser only.</p><p>Amazon may set cookies when you click through to Amazon.com or Amazon.ae. See Amazon's privacy notice for how they use them.</p><p>If you use the contact form, your name, email and message are sent to our inbox and used only to reply to you. They are never sold or shared.</p><p>If you join The Keepers, we store your email (and first name if you give it) to send the monthly email. You can unsubscribe any time from any email, or ask us to delete your details through the <a href="/contact/">contact page</a>.</p><p>Questions: <a href="/contact/">contact us</a>.</p>"""),
}
for path, (t, d, b) in SIMPLE.items():
    ch, cld = crumbs(path, [("Home", "/"), (t.split(' | ')[0], path)])
    write(path, head(t if '|' in t else t + " | Mom Tried These", d, path, [cld]) + f'<main class="wrap"><div class="prose">{ch}{b}</div></main>' + FOOT)
URLS.remove("/contact/thanks/"); URLS.remove("/subscribed/")
# ---- extras
os.makedirs('out2', exist_ok=True)
open('out2/subscribe.php','w').write(open('/tmp/claude-0/-home-claude/e5dc4931-8ec0-508e-88d9-aa0e375c6ba6/scratchpad/sub.php').read())
import email.utils, datetime as _dt
_items = ''.join(f"<item><title>{E(o['title'])}</title><link>{SITE}/blog/{o['slug']}/</link><guid>{SITE}/blog/{o['slug']}/</guid><pubDate>{email.utils.format_datetime(_dt.datetime(2026,10,28,8,0,tzinfo=_dt.timezone.utc))}</pubDate><description>{E(o['desc'])}</description><category>{E(o['cat'])}</category></item>" for o in POSTS[::-1])
open('out2/feed.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Mom Tried These</title><link>{SITE}/</link><description>Only the ones I kept. A working mom\'s finds for kids, home and life.</description><language>en</language>{_items}</channel></rss>')
open('out2/2f9c7b1e8a4d4c6b9e3f5a7d1c0b8e62.txt', 'w').write('2f9c7b1e8a4d4c6b9e3f5a7d1c0b8e62')
open('out2/robots.txt', 'w').write(f"User-agent: *\nAllow: /\nDisallow: /contact.php\nDisallow: /subscribe.php\nSitemap: {SITE}/sitemap.xml\n")
open('out2/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in URLS) + '</urlset>\n')
open('out2/404.html', 'w').write(head("Page not found | Mom Tried These", "Page not found.", "/404.html") + '<main class="wrap"><div class="prose"><h1>That page wandered off</h1><p class="lead">Like a sock in the wash. Try one of these instead.</p><p class="row"><a class="btn" href="/shop/">Shop all picks</a><a class="btn ghost" href="/blog/">Read the blog</a></p></div></main>' + FOOT)
shutil.copy('static/og.jpg', 'out2/og.jpg')
shutil.copytree('static/pins', 'out2/pins')
shutil.copytree('static/social', 'out2/social')
open('out2/favicon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#BF6B52"/><text x="32" y="43" font-family="Georgia,serif" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">MT</text></svg>')
open('out2/.htaccess', 'w').write("""ErrorDocument 404 /404.html
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\\. [NC]
RewriteRule ^(.*)$ https://momtriedthese.com/$1 [L,R=301]
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/html "access plus 1 hour"
ExpiresByType image/jpeg "access plus 30 days"
ExpiresByType image/svg+xml "access plus 30 days"
</IfModule>
""")
open('out2/contact.php', 'w').write(r"""<?php
// Mom Tried These contact form. Sends to the MTT inbox. Honeypot + basic validation.
$to = 'momtriedthese@gmail.com';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/'); exit; }
if (!empty($_POST['website'])) { header('Location: /contact/thanks/'); exit; }
$name = trim(strip_tags($_POST['name'] ?? ''));
$email = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$topic = trim(strip_tags($_POST['topic'] ?? 'Message'));
$msg = trim(strip_tags($_POST['message'] ?? ''));
if (!$name || !$email || !$msg || strlen($msg) > 4000) { header('Location: /contact/?error=1'); exit; }
$name = str_replace(["\r", "\n"], ' ', $name); $topic = str_replace(["\r", "\n"], ' ', $topic);
$subject = 'Mom Tried These: ' . $topic . ' from ' . $name;
$body = "Name: $name\nEmail: $email\nTopic: $topic\n\n$msg\n";
$headers = "From: Mom Tried These <hello@momtriedthese.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8\r\n";
@mail($to, $subject, $body, $headers);
header('Location: /contact/thanks/'); exit;
""")
print("built", len(URLS), "pages,", len(PROD), "products")
