"""Build corbel.html from structured bundle and SKU data.

Prices, compare-at prices and "% off" are computed here so every card on the
page stays consistent. Corbel SKU prices mirror mycorbel.com (price parity);
bundle compare-at = the sum of the Corbel prices of what's inside.

Run from the repo root:  python3 tools/build_corbel.py
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


LANGS = ["എന്റെ സോക്സ്", "ನನ್ನ ಮೊಜೆಗಳು", "আমার মোজা", "Majhe Moje", "ਮੇਰੇ ਮੋਜ਼ੇ", "મારા મોજાં", "माझे मोजे"]
STRIP = ["firsts", "ghar se", "becoming", "knitted by corbel", "storied by majhe moje", "bamboo &amp; cotton", "everyday, upgraded"]

frame_pills = '<button class="cx-frame-pill is-on" type="button" data-filter="all" style="--c:#441F03"><i></i>all stories</button>' + "".join(
    f'<button class="cx-frame-pill" type="button" data-filter="{k}" style="--c:{c}"><i></i>{n}</button>' for k, (n, c) in FRAMES.items())

which_links = "".join(f'<a href="#{b[0]}">{html.escape(b[1])}</a>' for b in BUNDLES)

page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Corbel × Majhe Moje | Everyday Socks With a Story</title>
  <meta name="description" content="Everyday socks by Corbel, chosen and storied by Majhe Moje. Firsts, ghar se and becoming: six story bundles for the days in between the drops.">
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
      <a class="is-active" href="corbel.html" aria-current="page">Corbel <span class="x">×</span> Moje</a>
      <a href="https://majhemoje.in/pages/our-mission">Our Story</a>
      <a href="https://majhemoje.in/pages/the-mark">The Mark</a>
      <a href="https://majhemoje.in/#studio">The Studio</a>
    </nav>
  </header>

  <main>

    <section class="cx-hero">
      <div class="cx-hero__inner">
        <div>
          <p class="cx-hero__lockup">Corbel <span>×</span> Majhe Moje</p>
          <h1>everyday.<br><em>still moje.</em></h1>
          <p class="cx-hero__body">Majhe moje means my socks, so they should show up on every day of your week, not just the drop days. Everyday essentials knitted by Corbel, chosen and storied by us. For your firsts, your ghar se moments, and whoever you&rsquo;re becoming.</p>
          <div class="cx-hero__actions">
            <a class="mm-btn mm-btn--orange" href="#stories">shop the stories →</a>
            <a class="mm-btn mm-btn--ghost" href="#how">how it works</a>
          </div>
          <p class="cx-hero__hand">chapters for the drops. these for the days in between ↷</p>
        </div>
        <div class="cx-hero__stack" aria-hidden="true">
          <figure class="cx-tile cx-tile--a"><img src="{img_url("professional")}" alt=""><figcaption>first salary</figcaption></figure>
          <figure class="cx-tile cx-tile--b"><img src="{img_url("varsity")}" alt=""><figcaption>the rotation</figcaption></figure>
          <figure class="cx-tile cx-tile--c"><img src="{img_url("ochre_m")}" alt=""><figcaption>sunday chai</figcaption></figure>
        </div>
      </div>
    </section>

    {marquee(STRIP)}

    <section class="cx-stories" id="stories">
      <div class="cx-stories__head">
        <p class="mm-eyebrow">six stories · corbel × moje</p>
        <h2 class="mm-title">the everyday stories.</h2>
        <p class="mm-sub">Each one is a bundle we put together from Corbel&rsquo;s best everyday pairs, with a story card inside. Only here.</p>
      </div>
      <div class="cx-frames" role="group" aria-label="filter stories">{frame_pills}</div>
      <div class="cx-grid">{"".join(bundle_card(b) for b in BUNDLES)}
      </div>
    </section>

    <section class="mm-manifesto">
      <span class="mm-manifesto__deco" aria-hidden="true">×</span>
      <div class="mm-manifesto__inner">
        <div class="mm-reveal">
          <p class="mm-eyebrow">three kinds of everyday</p>
          <p class="mm-manifesto__quote">&ldquo;Not every story needs a limited edition. Some just need a clean pair and a good morning.&rdquo;</p>
          <span class="mm-manifesto__attr">— the studio</span>
        </div>
        <div class="mm-manifesto__values mm-reveal">
          <div class="mm-manifesto__value"><p class="mm-manifesto__value-word">firsts</p><p class="mm-manifesto__value-sub">first salary, first fit pic, first flat. the ones you&rsquo;ll brag about later.</p></div>
          <div class="mm-manifesto__value"><p class="mm-manifesto__value-word">ghar se</p><p class="mm-manifesto__value-sub">sunday chai, the bag mom packed. home, wherever you&rsquo;re wearing it.</p></div>
          <div class="mm-manifesto__value"><p class="mm-manifesto__value-word">becoming</p><p class="mm-manifesto__value-sub">6 a.m. runs, the growing shoe rack. whoever you&rsquo;re turning into.</p></div>
          <div class="mm-manifesto__value"><p class="mm-manifesto__value-word">knitted</p><p class="mm-manifesto__value-sub">by corbel, in bamboo &amp; cotton. storied by us.</p></div>
        </div>
      </div>
    </section>

    <section class="mm-hd" id="shelf" style="padding-top:56px">
      <div class="mm-hd__head">
        <h2 class="mm-title">the everyday shelf.</h2>
        <a class="mm-hd__va" href="#stories">see the stories →</a>
      </div>
      <div class="mm-hd__scroll">{"".join(single_card(k) for k in SINGLES)}
      </div>
    </section>

    <section class="cx-how" id="how">
      <div class="cx-how__inner">
        <p class="mm-eyebrow">how it works</p>
        <h2 class="mm-title">chosen by us. knitted by corbel.</h2>
        <ol class="cx-how__steps">
          <li><h3>we pick</h3><p>We choose the pairs from Corbel that earn a place in a story. Most don&rsquo;t make the cut.</p></li>
          <li><h3>corbel knits &amp; ships</h3><p>Straight from Corbel, packed with our story card, usually out in 48 hours.</p></li>
          <li><h3>you scan</h3><p>The card&rsquo;s QR shows your story, how to size and care for your pairs, and a code for next time.</p></li>
          <li><h3>you tell us</h3><p>Rate your pair. Your reviews decide which stories stay on the shelf.</p></li>
        </ol>
      </div>
    </section>

    <section class="cx-card" id="card">
      <div class="cx-card__inner">
        <div class="cx-card__visual" aria-hidden="true">
          <img src="assets/img/corbel/card-front.png" alt="">
          <img src="assets/img/corbel/card-back.png" alt="">
        </div>
        <div>
          <p class="mm-eyebrow">found a card in your box?</p>
          <h2 class="mm-title">hi. you&rsquo;ve got moje.</h2>
          <p class="mm-sub">Thanks for picking one of our everyday stories. Here&rsquo;s everything the card promised.</p>
          <div class="cx-card__actions">
            <a class="cx-card__action" href="https://majhemoje.in/pages/reviews"><b>rate your pair →</b><span>two taps, and it really does decide what stays.</span></a>
            <a class="cx-card__action" href="#how"><b>size &amp; care →</b><span>cold wash, inside out, dry in the shade.</span></a>
            <a class="cx-card__action" href="#stories"><b>go again →</b><span>the other five stories are right here.</span></a>
          </div>
          <div class="cx-code"><b>MOREMOJE</b><span>10% off your next order<br>at majhemoje.in</span></div>
          <div class="cx-card__which"><p>which story came home with you?</p><div>{which_links}</div></div>
        </div>
      </div>
    </section>

    <section class="cx-credit">
      <p class="cx-credit__lock">Corbel <span>×</span> Majhe Moje</p>
      <p>Knitted by Corbel, an Indian sock maker working in bamboo and cotton. Chosen, bundled and storied by the Majhe Moje studio, Mumbai. Chapters stay ours alone; this shelf is where we meet.</p>
    </section>

  </main>

  <footer class="mm-footer">
    {marquee(["your moje, your story", "corbel × majhe moje", "everyday, still moje"])}
    <div class="mm-footer__main">
      <div class="mm-footer__brand">
        <img class="mm-footer__logo" src="assets/img/mm-logo.png" alt="Majhe Moje">
        <p class="mm-footer__tagline">your moje, your story.</p>
        <p class="mm-footer__contact"><a href="mailto:studio@majhemoje.in">studio@majhemoje.in</a><br><a href="tel:+919513373052">+91 95133 73052</a></p>
        <p class="mm-footer__est">est. 2025 · mumbai</p>
      </div>
      <div><p class="mm-footer__col-head">the drop</p><a class="mm-footer__link" href="https://majhemoje.in/collections/drops">current</a><a class="mm-footer__link" href="corbel.html">corbel × moje</a><a class="mm-footer__link" href="https://majhemoje.in/pages/size-guide">size guide</a></div>
      <div><p class="mm-footer__col-head">studio</p><a class="mm-footer__link" href="https://majhemoje.in/#studio">custom socks</a><a class="mm-footer__link" href="https://majhemoje.in/#studio">past collabs</a><a class="mm-footer__link" href="mailto:studio@majhemoje.in">studio@majhemoje.in</a></div>
      <div><p class="mm-footer__col-head">the story</p><a class="mm-footer__link" href="https://majhemoje.in/pages/our-mission">origin</a><a class="mm-footer__link" href="https://majhemoje.in/pages/the-mark">the mark</a></div>
    </div>
    <div class="mm-footer__bottom"><span>© majhe moje · corbel × majhe moje pairs are knitted and shipped by corbel</span><span>shipping · returns · privacy · terms</span></div>
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

open("corbel.html", "w").write(page)
print("corbel.html written:", len(BUNDLES), "bundles,", len(SINGLES), "singles")
