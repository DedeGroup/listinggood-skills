# Amazon Listing Rules Reference — By Marketplace

Quick reference for character limits, algorithm notes, and compliance red lines.

## Character Limits

| Element | US/CA | DE/UK/EU | JP | IN |
|---------|-------|----------|-----|-----|
| Title | 200 | 200 | 250 | 200 |
| Bullet Points | 500 each (×5) | 500 each (×5) | 500 each (×5) | 500 each (×5) |
| Description (plain text) | 2000 | 2000 | 2000 | 2000 |
| Search Terms (backend) | 249 bytes total | 249 bytes total | 249 bytes total | 249 bytes |

## A9/A10 Algorithm Factors

### Ranking Signals (A10, current)
1. **Sales velocity** — conversion rate × unit sales (dominant factor)
2. **Text relevance** — title/bullets/description/search terms matching query
3. **Price** — competitive pricing wins (but not race-to-bottom)
4. **Availability / stock** — in-stock items rank higher
5. **Customer satisfaction** — reviews, ratings, return rate
6. **Click-through rate** — main image + title combo in search results

### Conversion Signals
- Main image quality and compliance (white background, 85%+ fill, min 1000px)
- Title clarity (what is it + why buy it in first glance)
- Bullet point scannability (bold headers, benefit-first)
- Price positioning vs competitors
- Review count and rating (above 4.0 threshold matters)

## Compliance Red Lines (Will Get Listing Suppressed)

### Absolute Prohibitions (enforced by Amazon automated + manual review)
- **Misleading claims**: "best seller", "#1", "guaranteed", "FDA approved" (without proof)
- **Fake urgency**: "limited time", "last chance", "only 3 left"
- **Competitor brand names**: never mention in title or bullets
- **Incentivized reviews language**: any hint of "review for refund"
- **ALL CAPS abuse**: occasional emphasis word OK, entire phrases NOT OK
- **HTML in description** (plain text only unless registered for A+/EBC)
- **Phone numbers, email, URLs** in listing content
- **Claims requiring substantiation**: medical cures, anti-aging guarantees, etc.
- **Category-specific**: apparel cannot claim "waterproof" without certification; supplements cannot make disease-treatment claims

### Category-Specific Red Flags

| Category | Common Trap | Correct Approach |
|----------|------------|------------------|
| Apparel | "waterproof", "sweat-proof" | Use "water-resistant" with test standard citation |
| Supplements | "cures X", "prevents Y" | Use "supports" with disclaimer structure |
| Electronics | False certifications ("FCC certified" when not) | Only claim if certificate number available |
| Beauty | "dermatologist recommended" (without proof) | "dermatologist-tested" with lab name if true |
| Home/Kitchen | "food-grade" without material spec | Cite specific standard (e.g., "BPA-free, FDA CFR 21 compliant") |

## Mobile Optimization Notes

- **Title**: first ~80 characters visible before "..." on mobile app
- **Bullets**: first line (bold header) must convey the full benefit — many mobile users only read headers
- **Images**: first 3 images get ~90% of mobile clicks; ensure hero image is crystal clear at small size
- **Above-the-fold**: on mobile, user sees main image + title + price + rating before scrolling

## Multi-Marketplace Adaptation Tips

When adapting a US listing to DE/UK/JP:

1. **Translate meaning, not words** — idioms don't carry; rewrite for local phrasing
2. **Adjust keyword order** — DE puts noun compounds first; JP uses different search behavior
3. **Check cultural norms** — colors/sizes have different connotations
4. **Verify claims legality** — EU has stricter advertising law than US
5. **Localize units** — inches → cm, lbs → kg, Fahrenheit → Celsius
6. **Brand name consistency** — keep brand recognizable across locales
