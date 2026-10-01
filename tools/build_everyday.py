"""Build everyday.html (Everyday Moje: Corbel × Majhe Moje) from structured data.

Story bundles are curated by hand below. The full catalogue is read from
data/corbel-products.json (Corbel's public products.json) and sorted into
shelves using data/corbel-collections.json (Corbel's own collections).

Prices, compare-at prices and "% off" are computed here so every card on the
page stays consistent. Corbel SKU prices mirror mycorbel.com (price parity);
bundle compare-at = the sum of the Corbel prices of what's inside.

Run from the repo root:  python3 tools/build_everyday.py
"""

import html
import json

CDN = "https://cdn.shopify.com/s/files/1/0987/3978/1944/files/"

# Corbel SKUs used on the page: name, handle, price, compare-at, image, options, pairs
SKUS = {
    "professional": ("Men Bamboo Professional Set", "the-bamboo-professional-set", 549, 1299,
                     "Corbel_Bamboo_Professional_Set_1_f609704c-68fe-4b21-bb7d-7b971ecde7e9.webp?v=1785196966", [], 3),
    "signature":    ("Men Bamboo Signature Set", "the-bamboo-signature-set", 549, 1299,
                     "Corbel_Men_Corbel_Bamboo_Signature_Set.webp?v=1785195835", [], 3),
    "flame":        ("Flame Strike Cotton Crew, pack of 3", "corbel-flame-strike-cotton-crew-socks-pack-of-3", 699, None,
                     "Packof2-21.png?v=1789643533", [], 3),
    "retropop":     ("RetroPop Cotton Crew", "corbel-retropop-bamboo-crew", 499, None,
                     "WhatsAppImage2026-09-17at1.32.09PM.jpg?v=1789632626", [], 1),
    "ochre_m":      ("Men Cotton Earth & Ochre Set", "the-cotton-earth-ochre-set", 399, 799,
                     "CottonEarth_Ochre_2.webp?v=1785205921", [], 3),
    "ochre_w":      ("Women Cotton Earth & Ochre Edit", "the-cotton-earth-ochre-edit", 399, 799,
                     "CottonEarth_Ochre_2.webp?v=1785205921", [], 3),
    "core_white":   ("Men Bamboo Core White Set", "the-bamboo-core-white-set", 499, 999,
                     "Corbel_White_ankle_socks_1.webp?v=1785199640", [], 3),
    "core_black":   ("Men Bamboo Core Black Set", "the-bamboo-core-black-set", 499, 999,
                     "Corbel_Black_ankle_socks_1.webp?v=1785199618", [], 3),
    "sport_crew":   ("Bamboo Sports Socks, Crew", "bamboo-active-crew-socks-pack-of-1", 399, None,
                     "10.webp?v=1782948339", ["Gray", "White", "Navy", "Black", "Light grey"], 1),
    "perf_pro":     ("Bamboo Performance PRO", "bamboo-performance-pro-socks-pack-of-1", 499, None,
                     "CorbelBambooperformancePro_9.webp?v=1782772531", ["White", "Navy", "Black", "Gray", "Khaki"], 1),
    "low_ankle":    ("Bamboo Sports Socks, Low Ankle", "bamboo-active-low-ankle-socks-pack-of-1", 299, None,
                     "CorbelBambooLowAnkleSocks_1.webp?v=1782967365", ["Black", "Gray", "Navy", "Khaki", "White"], 1),
    "varsity":      ("Bamboo Varsity Duo, pack of 2", "corbel-bamboo-varsity-duo-pack-of-2", 999, None,
                     "WhatsAppImage2026-09-17at1.32.10PM_e201d987-949c-42b4-ae80-d80d352798e7.jpg?v=1789664350", [], 2),
    "street":       ("Street Stripe Socks", "corbel-street-stripe-socks", 499, None,
                     "WhatsAppImage2026-09-17at1.32.10PM_469bb5aa-e999-4111-a57f-db0f99a22934.jpg?v=1789636772", [], 1),
    "office":       ("Men Cotton Office Set", "the-cotton-office-set", 499, 999,
                     "MenCottonOfficeSet_2ff4ab90-0973-4b7f-a597-316a629922f1.webp?v=1785204911", [], 3),
    "biker":        ("Bamboo Biker Socks, pack of 2", "bamboo-biker-socks-pack-of-2", 699, 1299,
                     "CORBEL-BIKER.webp?v=1786657169", [], 2),
    "pilates":      ("Bamboo Pilates Grip Socks, pack of 2", "bamboo-pilates-grip-socks-pack-of-2", 549, 1199,
                     "CORBEL-SPORTS-PILATES-PK2-GRY-BLK-PT04.png?v=1786774659", [], 2),
    "twilight":     ("Men Cotton Twilight Forest Set", "the-cotton-twilight-forest-set", 399, 799,
                     "CottonTwilightForestSet.webp?v=1785205330", [], 3),
    "tessella":     ("Women Bamboo Tessella Edit", "the-bamboo-tessella-edit", 499, 999,
                     "Bamboo_Tessella_Set_1.webp?v=1785200261", [], 3),
    "football":     ("Bamboo Football Socks, Aero-Knit", "corbel-bamboo-football-aero-knit-socks", 599, None,
                     "CorbalBambooFootballSocks_8.webp?v=1782844349", ["Black", "Navy", "Light grey", "White"], 1),
}

FRAMES = {
    "firsts":   ("firsts", "#E56412"),
    "ghar-se":  ("ghar se", "#166349"),
    "becoming": ("becoming", "#D9589F"),
}

# story bundles: id, title, frame, for-line, story, note, skus, bundle price, persona
BUNDLES = [
    ("first-salary", "First Salary", "firsts", "for the first-jobber",
     "You bought your mom something. Now buy yourself six pairs of grown-up socks.",
     "adulting, sorted", ["professional", "signature"], 949, "experiential explorer"),
    ("fit-check", "Fit Check", "firsts", "for the first fit pic that went viral (to 14 people)",
     "The pants are cropped for a reason. Let the socks do the talking.",
     "hem? cropped.", ["flame", "retropop"], 999, "streetwear & hype"),
    ("sunday-chai", "Sunday Chai", "ghar-se", "for the day with nothing on the calendar",
     "No plans. One playlist. Both feet up on the good chair. One set for you, one for whoever stole the other.",
     "his + hers", ["ochre_m", "ochre_w"], 699, "sensory curationist"),
    ("mom-packed-these", "Mom Packed These", "ghar-se", "for the flight back to the city",
     "She put them in your bag ‘just in case’. She was right. She’s always right.",
     "just in case", ["core_black", "core_white"], 849, "experiential explorer"),
    ("run-club", "The Run Club", "becoming", "for the 6 a.m. version of you",
     "You said you’d go. You went. Twice, even. The socks noticed.",
     "streak: 2 days", ["sport_crew", "perf_pro", "low_ankle"], 999, "experiential explorer"),
    ("the-rotation", "The Rotation", "becoming", "for the shoe rack that needs its own room",
     "Every grail deserves a base layer. Three looks, zero clashing with the Dunks.",
     "grail-approved", ["varsity", "street"], 1249, "sneakerhead"),
]

SINGLES = ["professional", "office", "biker", "pilates", "twilight", "tessella", "sport_crew", "football"]


def rupees(n):
    return "₹{:,}".format(n)


def img_url(key, width=600):
    return f"{CDN}{SKUS[key][4]}&width={width}"


def pct(price, compare):
    return round((1 - price / compare) * 100) if compare and compare > price else 0


def badge(price, compare, fallback="new"):
    p = pct(price, compare)
    if p:
        return f'<span class="mm-hd__badge mm-hd__badge--sale">{p}%<br>off</span>'
    return f'<span class="mm-hd__badge mm-hd__badge--new">{fallback}</span>'


def price_row(price, compare):
    p = pct(price, compare)
    row = f'<span class="mm-hd__price">{rupees(price)}</span>'
    if p:
        row += f' <span class="mm-hd__compare">{rupees(compare)}</span> <span class="mm-hd__pct">{p}% off</span>'
    return f'<div class="mm-hd__prices">{row}</div>'


def bundle_card(b):
    bid, title, frame, for_line, story, note, keys, price, persona = b
    fname, colour = FRAMES[frame]
    compare = sum(SKUS[k][2] for k in keys)
    pairs = sum(SKUS[k][6] for k in keys)
    inside = " + ".join(f"<b>{html.escape(SKUS[k][0])}</b>" for k in keys)
    options = sorted({o for k in keys for o in SKUS[k][5]})
    data = html.escape(json.dumps({"name": title, "price": rupees(price), "options": options, "label": "pick a colour" if options else ""}))
    return f'''
        <article class="cx-story mm-reveal" id="{bid}" data-frame="{frame}" style="--c:{colour}">
          <div class="mm-hd__img mm-hd__img--packshot">
            {badge(price, compare, "story")}
            <span class="cx-story__note" aria-hidden="true">{html.escape(note)}</span>
            <img src="{img_url(keys[0])}" alt="{html.escape(title)}: {html.escape(SKUS[keys[0]][0])}" loading="lazy">
            <span class="cx-story__pairs">{pairs} pairs</span>
          </div>
          <p class="cx-story__tag"><i></i>{fname}</p>
          <h3 class="mm-hd__name">{html.escape(title)}</h3>
          <p class="cx-story__for">{html.escape(for_line)}</p>
          <p class="cx-story__line">{html.escape(story)}</p>
          <p class="cx-story__inside">inside: {inside}</p>
          {price_row(price, compare)}
          <button class="mm-hd__atc" type="button" data-product="{data}">add to bag</button>
        </article>'''


def single_card(key):
    name, handle, price, compare, _, options, pairs = SKUS[key]
    data = html.escape(json.dumps({"name": name, "price": rupees(price), "options": options, "label": "pick a colour" if options else ""}))
    pack = f"pack of {pairs}" if pairs > 1 else "single pair"
    return f'''
          <div class="mm-hd__card">
            <div class="mm-hd__img mm-hd__img--packshot">
              {badge(price, compare)}
              <img src="{img_url(key, 500)}" alt="{html.escape(name)}" loading="lazy">
            </div>
            <div class="mm-hd__body">
              <p class="mm-hd__chapter">corbel × moje · {pack}</p>
              <h3 class="mm-hd__name">{html.escape(name)}</h3>
              {price_row(price, compare)}
              <button class="mm-hd__atc" type="button" data-product="{data}">add to bag</button>
            </div>
          </div>'''


def marquee(items, cls=""):
    row = "".join(f"<span>{i}</span><span class=\"mm-dot\">◆</span>" for i in items)
    return f'<div class="mm-mq {cls}" aria-hidden="true"><div class="mm-mq__inner">{row}{row}</div></div>'



# ---------------------------------------------------------------------------
# full catalogue: every live Corbel product, sorted into shelves and story frames
# ---------------------------------------------------------------------------

import re

PRODUCTS = json.load(open("data/corbel-products.json"))["products"]
COLLECTIONS = json.load(open("data/corbel-collections.json"))

SHELF_FROM_COLLECTION = {
    "sportwear": "sports", "formalwear": "office", "casualwear": "casual",
    "womens-socks-range": "her", "mens-sock-range": "him",
    "bamboo-socks": "bamboo", "cotton-socks": "cotton",
}
TYPE_SHELF = {"Sports Socks": "sports", "Football Socks": "sports", "Performance Socks": "sports",
              "Pilates Socks": "sports", "Biker Socks": "sports", "Formal Socks": "office", "Casual Socks": "casual"}
FRAME_OF_SHELF = {"sports": "becoming", "office": "firsts", "casual": "ghar-se"}


def clean_name(t):
    t = re.sub(r"^Corbel\s+", "", t)
    t = re.sub(r"\s*[–—|-]\s*Pack of \d+\s*$", "", t)
    t = re.sub(r"\s*\|\s*Pack of \d+\s*$", "", t)
    t = re.sub(r"\s*\(Pack of \d+\)\s*$", "", t)
    t = re.sub(r"\s+Pack of \d+$", "", t)
    return t.strip()


def pack_size(t):
    m = re.search(r"Pack of (\d+)", t)
    if m:
        return int(m.group(1))
    if "Duo" in t:
        return 2
    if "Trio" in t or re.search(r"\b(Set|Edit)\b", t):
        return 3
    return 1


def catalogue_item(p):
    v = p["variants"][0]
    price = round(float(v["price"]))
    compare = round(float(v["compare_at_price"])) if v.get("compare_at_price") else None
    tags = {SHELF_FROM_COLLECTION[c] for c, hs in COLLECTIONS.items() if c in SHELF_FROM_COLLECTION and p["handle"] in hs}
    tags.add(TYPE_SHELF.get(p["product_type"], "casual"))
    title = p["title"]
    if "bamboo" in title.lower():
        tags.add("bamboo")
    if "cotton" in title.lower():
        tags.add("cotton")
    if title.startswith("Women"):
        tags.add("her"); tags.discard("him")
    if title.startswith("Men"):
        tags.add("him")
    if p["title"] in ("Hearts & Spades", "Sweetheart Stripe", "Strawberry Blossom", "Kitten & Hearts"):
        tags.add("her")
    shelf = TYPE_SHELF.get(p["product_type"], "casual")
    options = [x["title"] for x in p["variants"] if x["title"] != "Default Title"]
    return {
        "handle": p["handle"], "name": clean_name(title), "price": price, "compare": compare,
        "img": p["images"][0]["src"], "tags": sorted(tags), "frame": FRAME_OF_SHELF[shelf],
        "pairs": pack_size(title), "options": options,
        "material": "bamboo" if "bamboo" in tags else "cotton" if "cotton" in tags else "",
    }


CATALOGUE = [catalogue_item(p) for p in PRODUCTS if float(p["variants"][0]["price"]) > 0 and p["images"]]
BY_HANDLE = {c["handle"]: c for c in CATALOGUE}
BESTSELLERS = [BY_HANDLE[h] for h in COLLECTIONS["corbel-featured-collection"] if h in BY_HANDLE]


def sized(url, w):
    return url + ("&" if "?" in url else "?") + f"width={w}"


def catalogue_card(c, cls="mm-hd__card"):
    data = html.escape(json.dumps({"name": c["name"], "price": rupees(c["price"]), "options": c["options"],
                                   "label": "pick a colour" if c["options"] else ""}))
    bits = [c["material"], f"pack of {c['pairs']}" if c["pairs"] > 1 else "single pair"]
    if "her" in c["tags"]:
        bits.append("for her")
    meta = " · ".join(b for b in bits if b)
    return f'''
          <div class="{cls}" data-tags="{' '.join(c['tags'] + [c['frame']])}">
            <div class="mm-hd__img mm-hd__img--packshot">
              {badge(c["price"], c["compare"])}
              <img src="{sized(c["img"], 500)}" alt="{html.escape(c["name"])}" loading="lazy">
            </div>
            <div class="mm-hd__body">
              <p class="mm-hd__chapter">{meta}</p>
              <h3 class="mm-hd__name">{html.escape(c["name"])}</h3>
              {price_row(c["price"], c["compare"])}
              <button class="mm-hd__atc" type="button" data-product="{data}">add to bag</button>
            </div>
          </div>'''


def carousel(section_id, eyebrow, title, sub, items, colour="#E56412", link=("see all in the catalogue →", "#catalogue")):
    return f'''
    <section class="mm-hd cx-shelf" id="{section_id}" style="--c:{colour}">
      <div class="mm-hd__head">
        <div>
          <p class="mm-eyebrow" style="color:{colour}">{eyebrow}</p>
          <h2 class="mm-title">{title}</h2>
          <p class="mm-sub">{sub}</p>
        </div>
        <a class="mm-hd__va" href="{link[1]}" data-jump="{section_id}">{link[0]}</a>
      </div>
      <div class="mm-hd__scroll">{"".join(catalogue_card(c) for c in items)}
      </div>
      <div class="mm-hd__nav"><button class="mm-hd__nav-btn" type="button" data-dir="-1" aria-label="scroll left">←</button><button class="mm-hd__nav-btn" type="button" data-dir="1" aria-label="scroll right">→</button></div>
    </section>'''


def in_frame(f):
    return [c for c in CATALOGUE if c["frame"] == f]


def tagged(t):
    return [c for c in CATALOGUE if t in c["tags"]]


LANGS = ["എന്റെ സോക്സ്", "ನನ್ನ ಮೊಜೆಗಳು", "আমার মোজা", "Majhe Moje", "ਮੇਰੇ ਮੋਜ਼ੇ", "મારા મોજાં", "माझे मोजे"]
STRIP = ["everyday moje", "corbel × majhe moje", "firsts", "ghar se", "becoming", "bamboo &amp; cotton", "knitted by corbel"]

SHOP_BY = [
    ("bestsellers", "bestsellers", len(BESTSELLERS), "#E56412"),
    ("stories", "the six stories", len(BUNDLES), "#441F03"),
    ("firsts", "firsts", len(in_frame("firsts")), "#E56412"),
    ("ghar-se", "ghar se", len(in_frame("ghar-se")), "#166349"),
    ("becoming", "becoming", len(in_frame("becoming")), "#D9589F"),
    ("for-her", "for her", len(tagged("her")), "#FF92CE"),
    ("catalogue", "everything", len(CATALOGUE), "#441F03"),
]
shop_by = "".join(f'<a class="cx-tile-link" href="#{i}" style="--c:{c}"><b>{n}</b><span>{k} {"stories" if i == "stories" else "pairs" if i != "catalogue" else "products"}</span></a>' for i, n, k, c in SHOP_BY)

CHIPS = [("all", "all"), ("sports", "sports"), ("office", "office &amp; formal"), ("casual", "casual &amp; colour"),
         ("her", "for her"), ("him", "for him"), ("bamboo", "bamboo"), ("cotton", "cotton"),
         ("firsts", "firsts"), ("ghar-se", "ghar se"), ("becoming", "becoming")]
chips = "".join(f'<button class="cx-frame-pill{" is-on" if k == "all" else ""}" type="button" data-cat="{k}">{n} <small>{len(CATALOGUE) if k == "all" else sum(1 for c in CATALOGUE if k in c["tags"] or k == c["frame"])}</small></button>' for k, n in CHIPS)

frame_pills = '<button class="cx-frame-pill is-on" type="button" data-filter="all" style="--c:#441F03"><i></i>all stories</button>' + "".join(
    f'<button class="cx-frame-pill" type="button" data-filter="{k}" style="--c:{c}"><i></i>{n}</button>' for k, (n, c) in FRAMES.items())
which_links = "".join(f'<a href="#{b[0]}">{html.escape(b[1])}</a>' for b in BUNDLES)

hero_tiles = [BY_HANDLE.get(h) for h in ["the-bamboo-signature-set", "the-cotton-earth-ochre-set", "corbel-bamboo-varsity-duo-pack-of-2",
                                         "the-cotton-sundowner-set", "bamboo-active-crew-socks-pack-of-1"]]
hero_tiles = "".join(f'<figure class="cx-fan cx-fan--{i}"><img src="{sized(c["img"], 500)}" alt=""></figure>' for i, c in enumerate(t for t in hero_tiles if t))

page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Everyday Moje | Corbel × Majhe Moje</title>
  <meta name="description" content="Everyday Moje: Corbel × Majhe Moje. {len(CATALOGUE)} everyday socks by Corbel, chosen and storied by Majhe Moje: bestsellers, six story bundles, firsts, ghar se, becoming and the full catalogue.">
  <link rel="stylesheet" href="assets/css/fonts.css">
  <link rel="stylesheet" href="assets/css/live.css">
  <link rel="stylesheet" href="assets/css/corbel.css">
</head>
<body>

  {marquee(LANGS)}

  <header class="mm-head">
    <div class="mm-head__bar">
      <a class="mm-head__logo" href="https://majhemoje.in/" aria-label="Majhe Moje home"><img src="assets/img/mm-logo.png" alt="Majhe Moje"></a>
      <div class="mm-head__icons"><a href="https://majhemoje.in/search">search</a><a class="mm-head__bag" href="https://majhemoje.in/cart">bag<b id="bag-count">0</b></a></div>
    </div>
    <nav class="mm-nav-strip" aria-label="main">
      <a href="https://majhemoje.in/collections/drops">All Drops</a>
      <a href="https://majhemoje.in/#chapters">Chapters</a>
      <a class="is-active" href="#top" aria-current="page">Everyday Moje</a>
      <a href="https://majhemoje.in/pages/our-mission">Our Story</a>
      <a href="https://majhemoje.in/pages/the-mark">The Mark</a>
      <a href="https://majhemoje.in/#studio">The Studio</a>
    </nav>
  </header>

  <main id="top">

    <!-- 1 · the creative -->
    <section class="cx-poster">
      <div class="cx-poster__inner">
        <div class="cx-poster__text">
          <p class="cx-poster__eyebrow">introducing <b>everyday moje</b></p>
          <h1 class="cx-poster__lock">Corbel<span>×</span><br>Majhe Moje</h1>
          <p class="cx-poster__body">Majhe moje means my socks, so they should show up on every day of your week, not just the drop days. {len(CATALOGUE)} everyday pairs knitted by Corbel, chosen and storied by us.</p>
          <div class="cx-hero__actions">
            <a class="mm-btn mm-btn--orange" href="#bestsellers">shop bestsellers →</a>
            <a class="mm-btn mm-btn--ghost" href="#stories">the six stories</a>
          </div>
          <p class="cx-hero__hand">chapters for the drops. these for the days in between ↷</p>
        </div>
        <div class="cx-poster__fan" aria-hidden="true">{hero_tiles}<span class="cx-poster__x">×</span></div>
      </div>
      <ul class="cx-poster__facts">
        <li><b>{len(CATALOGUE)}</b>everyday pairs</li>
        <li><b>bamboo</b>&amp; long-staple cotton</li>
        <li><b>48 hrs</b>to dispatch</li>
        <li><b>made</b>in india</li>
      </ul>
    </section>

    {marquee(STRIP)}

    <!-- shop by -->
    <nav class="cx-shopby" aria-label="shop everyday moje by">{shop_by}</nav>

    <!-- 2 · bestsellers -->
    {carousel("bestsellers", "bestsellers · corbel × moje", "start with the favourites.", "The pairs people come back for. A good first everyday moje.", BESTSELLERS)}

    <!-- 3 · the six stories -->
    <section class="cx-stories" id="stories">
      <div class="cx-stories__head">
        <p class="mm-eyebrow">the six stories · only on majhe moje</p>
        <h2 class="mm-title">the everyday stories.</h2>
        <p class="mm-sub">Bundles we put together from Corbel&rsquo;s best everyday pairs, each with a story card inside.</p>
      </div>
      <div class="cx-frames" role="group" aria-label="filter stories">{frame_pills}</div>
      <div class="cx-grid">{"".join(bundle_card(b) for b in BUNDLES)}
      </div>
    </section>

    <!-- 4 · three kinds of everyday -->
    <section class="mm-manifesto">
      <span class="mm-manifesto__deco" aria-hidden="true">×</span>
      <div class="mm-manifesto__inner">
        <div class="mm-reveal">
          <p class="mm-eyebrow">three kinds of everyday</p>
          <p class="mm-manifesto__quote">&ldquo;Not every story needs a limited edition. Some just need a clean pair and a good morning.&rdquo;</p>
          <span class="mm-manifesto__attr">— the studio</span>
        </div>
        <div class="mm-manifesto__values mm-reveal">
          <a class="mm-manifesto__value" href="#firsts"><p class="mm-manifesto__value-word">firsts</p><p class="mm-manifesto__value-sub">first job, first interview, first flat. {len(in_frame("firsts"))} pairs that dress up.</p></a>
          <a class="mm-manifesto__value" href="#ghar-se"><p class="mm-manifesto__value-word">ghar se</p><p class="mm-manifesto__value-sub">sunday chai, the bag mom packed. {len(in_frame("ghar-se"))} pairs for easy days.</p></a>
          <a class="mm-manifesto__value" href="#becoming"><p class="mm-manifesto__value-word">becoming</p><p class="mm-manifesto__value-sub">6 a.m. runs, pilates, the turf. {len(in_frame("becoming"))} pairs that move.</p></a>
          <a class="mm-manifesto__value" href="#catalogue"><p class="mm-manifesto__value-word">everything</p><p class="mm-manifesto__value-sub">all {len(CATALOGUE)} pairs, knitted by corbel in bamboo &amp; cotton.</p></a>
        </div>
      </div>
    </section>

    <!-- 5 · story frames -->
    {carousel("firsts", "firsts", "for the first job, and every one after.", "Office crews and formal sets in bamboo and cotton. The grown-up drawer, sorted.", in_frame("firsts"), "#E56412")}
    {carousel("ghar-se", "ghar se", "for the days that feel like home.", "Colour, pattern and soft cotton for Sundays, chai and doing nothing at all.", in_frame("ghar-se"), "#166349")}
    {carousel("becoming", "becoming", "for whoever you&rsquo;re turning into.", "Sports, pilates, biker and football pairs. Built for the 6 a.m. version of you.", in_frame("becoming"), "#D9589F")}
    {carousel("for-her", "for her", "for her, every day.", "Edits for women across formal, casual and colour.", tagged("her"), "#E0559E")}

    <!-- 6 · the full catalogue -->
    <section class="cx-cat" id="catalogue">
      <div class="cx-stories__head">
        <p class="mm-eyebrow">the full catalogue</p>
        <h2 class="mm-title">every everyday moje.</h2>
        <p class="mm-sub">All {len(CATALOGUE)} pairs from Corbel, at Corbel&rsquo;s own prices. Filter by what your day needs.</p>
      </div>
      <div class="cx-frames cx-cat__chips" role="group" aria-label="filter the catalogue">{chips}</div>
      <p class="cx-cat__count" role="status"><b id="cat-count">{len(CATALOGUE)}</b> pairs</p>
      <div class="cx-cat__grid">{"".join(catalogue_card(c, "mm-hd__card cx-cat-card") for c in CATALOGUE)}
      </div>
    </section>

    <!-- 7 · how it works -->
    <section class="cx-how" id="how">
      <div class="cx-how__inner">
        <p class="mm-eyebrow">how it works</p>
        <h2 class="mm-title">chosen by us. knitted by corbel.</h2>
        <ol class="cx-how__steps">
          <li><h3>we pick</h3><p>We choose the Corbel pairs that earn a place on the everyday shelf, and build the stories around them.</p></li>
          <li><h3>corbel knits &amp; ships</h3><p>Straight from Corbel, packed with our story card, usually out in 48 hours.</p></li>
          <li><h3>you scan</h3><p>The card&rsquo;s QR shows your story, how to size and care for your pairs, and a code for next time.</p></li>
          <li><h3>you tell us</h3><p>Rate your pair. Your reviews decide which stories stay on the shelf.</p></li>
        </ol>
      </div>
    </section>

    <!-- 8 · found a card? (QR landing) -->
    <section class="cx-card" id="card">
      <div class="cx-card__inner">
        <div class="cx-card__visual" aria-hidden="true">
          <img src="assets/img/corbel/card-front.png" alt="">
          <img src="assets/img/corbel/card-back.png" alt="">
        </div>
        <div>
          <p class="mm-eyebrow">found a card in your box?</p>
          <h2 class="mm-title">hi. you&rsquo;ve got moje.</h2>
          <p class="mm-sub">Thanks for picking everyday moje. Here&rsquo;s everything the card promised.</p>
          <div class="cx-card__actions">
            <a class="cx-card__action" href="https://majhemoje.in/pages/reviews"><b>rate your pair →</b><span>two taps, and it really does decide what stays.</span></a>
            <a class="cx-card__action" href="#how"><b>size &amp; care →</b><span>cold wash, inside out, dry in the shade.</span></a>
            <a class="cx-card__action" href="#catalogue"><b>go again →</b><span>{len(CATALOGUE)} more pairs, right here.</span></a>
          </div>
          <div class="cx-code"><b>MOREMOJE</b><span>10% off your next order<br>at majhemoje.in</span></div>
          <div class="cx-card__which"><p>which story came home with you?</p><div>{which_links}</div></div>
        </div>
      </div>
    </section>

    <section class="cx-credit">
      <p class="cx-credit__lock">Corbel <span>×</span> Majhe Moje</p>
      <p>Everyday Moje is knitted by Corbel, an Indian sock maker working in bamboo and cotton, and chosen, bundled and storied by the Majhe Moje studio, Mumbai. Chapters stay ours alone; this shelf is where we meet.</p>
    </section>

  </main>

  <footer class="mm-footer">
    {marquee(["your moje, your story", "everyday moje", "corbel × majhe moje"])}
    <div class="mm-footer__main">
      <div class="mm-footer__brand">
        <img class="mm-footer__logo" src="assets/img/mm-logo.png" alt="Majhe Moje">
        <p class="mm-footer__tagline">your moje, your story.</p>
        <p class="mm-footer__contact"><a href="mailto:studio@majhemoje.in">studio@majhemoje.in</a><br><a href="tel:+919513373052">+91 95133 73052</a></p>
        <p class="mm-footer__est">est. 2025 · mumbai</p>
      </div>
      <div><p class="mm-footer__col-head">the drop</p><a class="mm-footer__link" href="https://majhemoje.in/collections/drops">current</a><a class="mm-footer__link" href="#top">everyday moje</a><a class="mm-footer__link" href="https://majhemoje.in/pages/size-guide">size guide</a></div>
      <div><p class="mm-footer__col-head">studio</p><a class="mm-footer__link" href="https://majhemoje.in/#studio">custom socks</a><a class="mm-footer__link" href="https://majhemoje.in/#studio">past collabs</a><a class="mm-footer__link" href="mailto:studio@majhemoje.in">studio@majhemoje.in</a></div>
      <div><p class="mm-footer__col-head">the story</p><a class="mm-footer__link" href="https://majhemoje.in/pages/our-mission">origin</a><a class="mm-footer__link" href="https://majhemoje.in/pages/the-mark">the mark</a></div>
    </div>
    <div class="mm-footer__bottom"><span>© majhe moje · everyday moje pairs are knitted and shipped by corbel</span><span>shipping · returns · privacy · terms</span></div>
  </footer>

  <div class="mm-hd-overlay" id="atc" aria-hidden="true">
    <div class="mm-hd-drawer" role="dialog" aria-modal="true" aria-labelledby="atc-name">
      <div class="mm-hd-drawer__drag"></div>
      <div class="mm-hd-drawer__head">
        <div><p class="mm-hd-drawer__name" id="atc-name"></p><p class="mm-hd-drawer__price" id="atc-price"></p></div>
        <button class="mm-hd-drawer__close" type="button" aria-label="close">✕</button>
      </div>
      <p class="mm-hd-drawer__label" id="atc-label"></p>
      <div class="mm-hd-drawer__sizes" id="atc-options"></div>
      <p class="mm-hd-drawer__ship">knitted &amp; shipped by corbel · usually dispatched in 48 hours · COD available</p>
      <button class="mm-hd-drawer__add" type="button" id="atc-add">add to bag</button>
      <p class="mm-hd-drawer__msg" id="atc-msg" role="status"></p>
    </div>
  </div>

  <script src="assets/js/corbel.js"></script>
</body>
</html>
'''

open("everyday.html", "w").write(page)
print(f"everyday.html: {len(BESTSELLERS)} bestsellers, {len(BUNDLES)} stories, "
      f"firsts {len(in_frame('firsts'))} / ghar se {len(in_frame('ghar-se'))} / becoming {len(in_frame('becoming'))}, "
      f"for her {len(tagged('her'))}, catalogue {len(CATALOGUE)}")
