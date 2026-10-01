# Corbel × Majhe Moje: strategy

*The agreed approach from the September 2026 strategy Q&A. It replaces the
earlier "Rojnishi" everyday-line concept.*

---

## 1. The idea

*Majhe moje* means "my socks", so the brand should show up on every day of a
customer's week, not only on drop days. Chapters remain the limited,
collectible drops. **Corbel × Majhe Moje** is the everyday shelf: Corbel's
socks, chosen and storied by us, for the days in between the drops.

## 2. Who it's for

The same four ICPs as the rest of the brand (see the *MajheMojeStrategy*
deck), in their **everyday** lives rather than their collector moments:

| ICP | Their everyday | Story |
|---|---|---|
| Experiential Explorer (23–33) | first job, travel home, run club | First Salary · Mom Packed These · The Run Club |
| Sensory Curationist (22–30) | slow Sundays, gifting a partner | Sunday Chai |
| Streetwear & Hype (21–32) | fit checks, creator culture | Fit Check |
| Sneakerhead (20–32) | the rotation, matching the grail | The Rotation |

## 3. The narrative

Three story frames, in a **playful and light** tone. They're chosen because
they evoke warmth, nostalgia or aspiration, not hardship:

- **Firsts**: first salary, first fit pic, first flat.
- **Ghar se**: Sunday chai, the bag mom packed. Home, wherever you're wearing it.
- **Becoming**: the 6 a.m. run, the growing shoe rack.

## 4. The business model

| | Agreed |
|---|---|
| Products | Corbel's **existing SKUs**; no new manufacturing |
| Selling | **Bestsellers** (Corbel's featured six), **6 exclusive story bundles**, and the **full catalogue** of 66 Corbel products |
| Fulfilment | **Corbel dropships** in its own pack, with our insert card |
| Money | Customer pays Majhe Moje; **60% to Corbel / 40% to Majhe Moje** of net sale |
| Pricing | Singles at **Corbel's listed price** (parity); bundles priced by us below the sum of parts; **"% off" badges** match the live site |
| Returns | Corbel covers defects, damage and wrong items; we cover change of mind and failed COD |
| Customer | **We own it.** Corbel only ships |
| Display | We show selected Corbel SKUs; **Corbel never shows our Moje** (its store isn't premium enough for Chapters) |

**Why bundles lead.** The live store's average order is ₹1,114 (deck:
55 orders, 0.30% conversion). Corbel singles at ₹299–₹699 would pull that down.
Bundles land at ₹699–₹1,249, can't be price-compared on Corbel's site, and are
where our story adds the most value.

## 5. On the site

An **"Everyday Moje" item in the main nav** and its own page, opening with a Corbel × Majhe Moje creative and layered as: bestsellers → the six stories → Firsts / Ghar se / Becoming / For her shelves → the full filterable catalogue (66 products). It's, built from the
live theme's existing components: language marquee, green header, brown nav
strip, drops cards with round badges, the manifesto band and the footer. Plus
a strip on the homepage. Prototype: [`everyday.html`](everyday.html).

**Images:** Corbel's product photos, AI-restyled into our look (with Corbel's
written permission). The restyle must never change the product itself. Until
then, the prototype blends the packshots onto cream and crops Corbel's
caption bar in CSS.

## 6. The insert card

One **universal** A6 card for every order ([`card.html`](card.html)):
- **Front:** "hi. you've got moje." plus a QR code for the story, ratings and the site.
- **Back:** size, care, a *tick your story* list, and the **MOREMOJE** next-order code.
- The QR opens the page's *found a card?* section (`/pages/everyday-moje?src=card#card`),
  so it works for every product and can be tracked in analytics. This is the deck's
  "Trojan horse" loop: Corbel's parcel becomes our CRM entry point.

## 7. The pitch

Goal: **agree the partnership.** Walk in with the prototype, the card and the
one-page term sheet ([`termsheet.html`](termsheet.html)). Our asks:
- price-parity notice
- a 48-hour dispatch SLA
- exclusive bundles
- free samples
- photo and restyle permission

## 8. To confirm

- The size ranges per SKU (the card says UK 6–10 as a placeholder).
- Whether payment-gateway fees are shared 60/40.
- The order hand-off format (shared sheet or Shopify app).
- Create the `everyday-moje` page and the MOREMOJE discount in Shopify.
