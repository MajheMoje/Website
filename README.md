# majhe moje — UI redesign: "every pair is a page"

A proposed new UI for [majhemoje.in](https://majhemoje.in), designed around one idea:
**a brand of stories should read like a book, not like a store.**

Open `index.html` in a browser — the prototype is fully self-contained (fonts and
imagery are vendored into `assets/`), so it also works on GitHub Pages as-is.

---

## 1. Brand study

Everything below was gathered from the live site (homepage, `/pages/our-mission`,
`/pages/the-mark`, `/collections/all`, `/products.json`).

### What Majhe Moje is

- A **story-driven sock label** from Mumbai, est. 2025. "Majhe moje" (माझे मोजे)
  means "my socks" — a phrase that lands across Marathi, Hindi, Bengali,
  Punjabi and Gujarati.
- Founded by **Naval Agarwal** ("Sock's have always been meaningless, so we hope
  Moje's give you a way, to be free, to express"), with **Vedika** as the designer
  who "draws the magic."
- The founding question: *"Why does everything in India have a story — except
  what's on your feet?"*

### How the brand actually behaves

- **Releases are chapters, not collections.** Chapter One is "Stories of
  Christmas" — five designs forming one connected narrative (The Calm Before
  Christmas → The Presents → The Santa → The Morning Before Christmas → The
  Evergreen Tree), plus interludes (The Other Side, Perfectly Mismatched).
- **Chapters close permanently.** "Limited always. No restocks." Scarcity is a
  narrative device, not a marketing trick.
- **Every product description is a short story** — genuinely written, with a
  protagonist and a turn ("The hardest part of giving isn't the effort — it's
  the release.").
- **The Mark**: the emblem spells MOJE but reads as a face (M — the form,
  O — the eye, J — the journey, E — the expression), placed at the *sole*:
  "The mark stays low because we believe in being rooted."
- **Values**: story over mass production · emotion over trends · culture not
  costume · 320 GSM cotton · fully made in India.
- **Voice**: lowercase, warm, confident, a little handwritten.

### The gap the redesign closes

The current site says all of this *in the copy*, but the UI is still shaped like
an e-commerce theme: hero → product grid → reviews → newsletter. The storytelling
lives in words while the interface stays transactional. For a brand whose entire
moat is narrative, the **structure** of the site should be the story.

---

## 2. The concept: the site is a book

Every UI decision maps a bookmaking convention onto a commerce need:

| Book convention | UI element | Commerce job |
|---|---|---|
| Prologue | Hero: "not socks. moje." with a drop cap and polaroids | Positioning + first CTA |
| Table of contents (dotted leaders) | `#contents` — chapters listed with page numbers; open chapters get a green **OPEN** stamp; "chapter two — untitled … in the making" | Navigation + drop anticipation |
| Chapter heading + epigraph | "Chapter One — Stories of Christmas" | Collection page header |
| Numbered stories | Product cards as "story № 01–05," each with a one-line synopsis from the real product copy | Product grid |
| The complete volume | "Collect the chapter" boxed-set band | Bundle upsell |
| Interludes | The Other Side + Perfectly Mismatched | Non-chapter products |
| A letter, footnotes | Founder's letter on taped paper; values as footnotes ¹ ² ³; signed in handwriting | About / mission / trust |
| Bookmark ribbon | Thin orange reading-progress bar at the top | Scroll orientation |
| Epilogue | "We'll let you know." — email capture, "save my page" | Newsletter |
| Colophon | Footer: "set in sansita, lora & dm sans · mumbai, est. mmxxv" | Footer/legal |

Other story-first moves:

- **A multilingual marquee** (माझे मोजे · ਮੇਰੇ ਮੌਜੇ · আমার মোজা · મારા મોજા ·
  मेरे मोज़े) makes the pan-Indian name part of the visual rhythm.
- **The Mark gets a full dark chapter** — M · O · J · E with their meanings and
  the smile drawn as an actual arc: "the smile at the bottom isn't decoration.
  it's the whole point."
- **The manifesto is typeset, not badged** — "story over mass production /
  emotion over trends / culture, not costume" as large editorial lines.
- **Reviews become "readers"** — ★ 4.8 from 124 readers of chapter one.

### Competitive positioning (vs. "joywear")

Benchmarked against [biglittlepeople.com](https://www.biglittlepeople.com/)
("India's first joywear brand" — childish socks for adults, ~₹378–1,349,
discount-led merchandising, playful GIF-heavy Shopify layout). The two brands
share a category but not a position, and this UI leans into the difference:

- **They sell joy; we sell meaning.** BLP's frame is silliness and whimsy;
  Majhe Moje's frame is narrative, craft and permanence. The UI therefore reads
  like a first edition, not a toy store: paper grain, double-rule dividers,
  Roman numerals, an inked FIRST EDITION stamp.
- **They discount; we number printings.** BLP leads with "LOWEST IT'LL EVER
  BE" and struck-through prices. Here the price stands alone and the compare-at
  price is a quiet small-caps "list ₹750" — the urgency comes from scarcity
  ("one printing, ever"), not markdowns.
- **They bundle; we bind volumes.** Their "Joy Bundle" maps to our "collect
  the chapter" boxed set — a collector's object, not a deal.
- **Craft receipts.** The Hallmarks section (320 GSM combed cotton, fully made
  in India, one printing, the hidden mark) gives the premium claim evidence;
  BLP has no equivalent.

### What was deliberately kept

The redesign is a re-architecture, not a rebrand. Palette (cream `#FFFCE8`,
ink brown `#441F03`, orange `#E56412`, evergreen `#166349`, pink `#FF92CE`),
type system (Sansita display / Lora narrative / DM Sans UI / Caveat hand),
lowercase voice, and all product copy, prices and photography are the brand's
own, taken from the live site.

---

## 3. Repo layout

```
index.html            the whole redesigned page
assets/css/style.css  design system + layout (custom properties up top)
assets/css/fonts.css  self-hosted @font-face (Sansita, Lora, DM Sans, Caveat)
assets/fonts/         woff2 files (latin + latin-ext)
assets/img/           product photography from the live store, for the prototype
assets/js/main.js     dependency-free: reading ribbon, scroll reveal, mobile nav
```

Notes for productionizing:

- Product cards link to the real Shopify product URLs, so the prototype is
  shoppable today; the layout maps 1:1 onto Shopify sections (TOC = collection
  list, stories = featured collection, letter = page content) if rebuilt as a
  theme.
- Scroll-reveal is progressive enhancement (content is fully visible without
  JS) and honors `prefers-reduced-motion`.
- Marquee scripts (Devanagari, Gurmukhi, Bengali, Gujarati) render via system
  fonts; add Noto subsets if pixel-consistency matters.
