"""Embedded Amazon listing knowledge base + generation logic.

All content is self-contained (no external calls). The CTA footer points
users to https://www.listinggood.com for the full SaaS (multi-marketplace
optimization + compliance deep-scan).
"""

CTA = (
    "\n\n---\n"
    "Need the full version? ListingGood does this across 8 marketplaces with "
    "live compliance deep-scan, A/B title testing, and bulk generation.\n"
    "Try free: https://www.listinggood.com/scan\n"
    "Full SaaS: https://www.listinggood.com\n"
)

# Title character limits by marketplace
TITLE_LIMITS = {
    "us": 200, "ca": 200, "de": 200, "uk": 200, "eu": 200,
    "jp": 250, "in": 200, "fr": 200, "it": 200, "es": 200,
}

BULLET_LIMIT = 500  # per bullet, all marketplaces

# Category -> title pattern + example
TITLE_PATTERNS = {
    "apparel": {
        "pattern": "Brand + Gender/Age + Item Type + Material/Feature + Occasion/Style + Size + Color",
        "example": "Zara Women's Wool Blend Coat Belted Midi Length Winter Elegant Black M",
    },
    "electronics": {
        "pattern": "Brand + Product Name + Key Spec (Capacity/Power) + Compatibility + Color",
        "example": "Anker PowerCore 26800mAh Portable Charger 3-Port USB-C for iPhone iPad Samsung - Black",
    },
    "home": {
        "pattern": "Brand + Product Name + Material/Feature + Size/Dims + Use Case + Set Count",
        "example": "Pyrex Glass Baking Dish Set 6-Piece Oven Safe Borosilicate Bakeware - Clear",
    },
    "beauty": {
        "pattern": "Brand + Product Type + Key Ingredient + Skin/Hair Type + Size + Benefit",
        "example": "CeraVe Moisturizing Cream for Dry Skin with Hyaluronic Acid 19 oz - Fragrance Free",
    },
    "supplements": {
        "pattern": "Brand + Supplement Name + Primary Benefit + Key Ingredient + Dosage + Count + Format",
        "example": "Nature's Bounty Vitamin D3 5000 IU Softgels Immune Support 240 Softgels",
    },
    "generic": {
        "pattern": "Brand + Product Name + Primary Feature + Secondary Feature + Use Case + Size/Color",
        "example": "Acme Widget Pro Heavy-Duty Stainless Steel for Home Workshop - Silver",
    },
}

# Universal compliance red lines (automated suppression triggers)
HARD_REDLINES = [
    ("Competitor brand name in title/bullets", "Never mention competitor brands."),
    ("Incentivized review language", "No 'review for refund' or similar hints."),
    ("Phone / email / URL in listing", "External contact info is prohibited."),
    ("HTML tags in plain description", "Plain text only unless registered for A+ content."),
    ("ALL CAPS abuse", "Occasional emphasis word OK, entire phrases NOT."),
    ("Fake urgency", "'limited time', 'only 3 left', 'last chance' are violations."),
    ("Misleading superlatives", "'#1', 'best seller', 'guaranteed' without proof."),
    ("Unsupported certification claims", "'FCC certified' only if certificate number exists."),
]

# Category-specific red lines
CATEGORY_REDLINES = {
    "apparel": [
        ("'Waterproof' without test standard", "Use 'water-resistant' with AATCC 22 / ISO 4920 citation."),
        ("'Made in Italy' unverifiable", "Origin claims must be factual and provable."),
    ],
    "supplements": [
        ("Disease treatment claims", "'cures', 'prevents cancer' — absolutely prohibited."),
        ("'FDA approved' for supplements", "FDA does not 'approve' supplements; use 'registered'."),
    ],
    "electronics": [
        ("False safety certifications", "CE/FCC/UL only if certificate exists."),
        ("Unverified compatibility", "'Works with iPhone' must be true; MFi for some connectors."),
    ],
    "beauty": [
        ("'Dermatologist recommended' without proof", "Need actual study or dermatologist name."),
        ("Unqualified 'hypoallergenic'", "Must have testing to support the claim."),
    ],
    "home": [
        ("'Food-grade' without material spec", "Cite standard: 'BPA-free, FDA CFR 21 compliant'."),
        ("Unsubstantiated heat resistance", "Give specific temp: 'up to 400 F / 204 C'."),
    ],
    "baby": [
        ("'Prevents SIDS'", "Absolutely prohibited sleep-position claims."),
    ],
    "pet": [
        ("'Treats fleas' without EPA registration", "Pesticide claims need EPA registration."),
    ],
}

# Header formula library (benefit-led)
HEADER_TEMPLATES = {
    "comfort": ["ALL-DAY COMFORT", "CUSTOMIZABLE FIT", "FEELS LIKE A SECOND SKIN"],
    "quality": ["BUILT TO LAST", "PREMIUM CRAFTSMANSHIP", "3X THE LONGEVITY"],
    "versatile": ["DESIGNED FOR EVERYDAY USE", "ONE ITEM, MANY USES", "FROM HOME TO OUTDOORS"],
    "unique": ["EXCLUSIVE DESIGN", "PROPRIETARY TECHNOLOGY", "THE ONLY ONE THAT"],
    "trust": ["BUY WITH CONFIDENCE", "BACKED BY WARRANTY", "OUR PROMISE"],
}

# Proof-point guidance
PROOF_GUIDANCE = [
    ("Number", "e.g. 'lasts 3x longer' — specific = credible"),
    ("Material", "e.g. 'full-grain leather' — tangible quality"),
    ("Certification", "e.g. 'OEKO-TEX Standard 100' — third-party proof"),
    ("Time duration", "e.g. 'keeps drinks cold 24h' — sets expectation"),
    ("Result", "e.g. 'charges to 50% in 30 min' — visualizable"),
    ("Guarantee", "e.g. '2-year warranty' — removes risk"),
]


def get_title_pattern(category: str) -> dict:
    cat = (category or "").lower()
    for key in TITLE_PATTERNS:
        if key in cat or cat in key:
            return TITLE_PATTERNS[key]
    return TITLE_PATTERNS["generic"]


def get_redlines(category: str):
    """Return (hard_redlines, category_redlines) for a category."""
    cat = (category or "").lower()
    cat_lines = []
    for key, lines in CATEGORY_REDLINES.items():
        if key in cat or cat in key:
            cat_lines.extend(lines)
    return HARD_REDLINES, cat_lines


def build_title(brand: str, product: str, keywords: list, features: list,
                marketplace: str = "us") -> str:
    """Build an optimized title from components, within char limit."""
    limit = TITLE_LIMITS.get((marketplace or "us").lower(), 200)
    parts = []
    if brand:
        parts.append(brand.strip())
    if product:
        parts.append(product.strip())
    # primary differentiator from keywords
    for kw in (keywords or []):
        kw = kw.strip()
        if kw and kw not in " ".join(parts).lower():
            parts.append(kw)
    # a feature or two as secondary
    for f in (features or [])[:2]:
        f = f.strip()
        if f and f.lower() not in " ".join(parts).lower():
            parts.append(f)
    title = " ".join(parts)
    # trim to limit at word boundary
    if len(title) > limit:
        truncated = []
        total = 0
        for w in title.split(" "):
            if total + len(w) + 1 > limit:
                break
            truncated.append(w)
            total += len(w) + 1
        title = " ".join(truncated).rstrip(" -,")
    return title


def build_bullets(product: str, features: list, category: str) -> list:
    """Generate 5 benefit-led bullets from a feature list."""
    bullets = []
    headers_cycle = (
        HEADER_TEMPLATES["comfort"] + HEADER_TEMPLATES["quality"]
        + HEADER_TEMPLATES["versatile"] + HEADER_TEMPLATES["trust"]
    )
    feats = features or []
    for i, feat in enumerate(feats[:5]):
        feat = feat.strip()
        if not feat:
            continue
        header = headers_cycle[i % len(headers_cycle)]
        # basic feature -> benefit rewrite
        benefit = _feature_to_benefit(feat, category)
        bullets.append((header, benefit))
    # pad to 5 if short
    while len(bullets) < 5:
        bullets.append((
            HEADER_TEMPLATES["trust"][len(bullets) % len(HEADER_TEMPLATES["trust"])],
            f"Backed by our quality promise — buy {product} with confidence, "
            "risk-free, from a brand that stands behind every order.",
        ))
    return bullets


def _feature_to_benefit(feature: str, category: str) -> str:
    """Translate a raw feature sentence into a benefit-led body."""
    f = feature.lower()
    if any(w in f for w in ["cotton", "wool", "linen", "bamboo"]):
        return (f"{feature} keeps you cool, dry, and comfortable all day — "
                "no sticky discomfort in warm weather, and breathable for all-day wear.")
    if any(w in f for w in ["battery", "mah", "charge"]):
        return (f"{feature} means you're never caught hunting for an outlet — "
                "reliable power when you need it most, at home or on the go.")
    if any(w in f for w in ["waterproof", "water-resistant", "water proof"]):
        return (f"{feature} beads away rain and spills so you arrive dry and "
                "protected through unexpected weather.")
    if any(w in f for w in ["dishwasher", "machine wash", "easy clean", "washable"]):
        return (f"{feature} — pop it in and forget it, no scrubbing or soaking, "
                "more time for what matters.")
    if any(w in f for w in ["non-slip", "grip", "anti-slip"]):
        return (f"{feature} gives you stable, confident footing on wet and uneven "
                "surfaces from daily commute to weekend adventure.")
    # default generic benefit translation
    return (f"{feature} — thoughtfully designed to make your everyday easier, "
            "with the quality and detail you expect from a premium product.")


def build_description(product: str, bullets: list, category: str) -> str:
    """Compose a plain-text description from bullets + category intro."""
    intro = (
        f"Discover the {product} — engineered for sellers and shoppers who "
        f"refuse to compromise. Every detail is considered, every claim substantiated."
    )
    lines = [intro, ""]
    for header, body in bullets:
        lines.append(f"- {header}: {body}")
    lines += [
        "",
        "Order with confidence. Our commitment to quality means you get a product "
        "that performs as described, every time.",
    ]
    return "\n".join(lines)


def audit_compliance(text: str, category: str) -> dict:
    """Scan listing text for red-line issues. Returns scored report."""
    import re
    t = (text or "").lower()
    issues = []
    hard, cat_lines = get_redlines(category)
    for name, fix in hard:
        if _matches_redline(t, name):
            issues.append(("Critical", name, fix))
    for name, fix in cat_lines:
        if _matches_redline(t, name):
            issues.append(("Warning", name, fix))
    # heuristic extra checks
    if re.search(r"[A-Z]{6,}", text or ""):
        issues.append(("Warning", "Excessive ALL CAPS detected",
                       "Use sentence case; occasional emphasis word is fine."))
    if re.search(r"(http|www\.|https://)", text or ""):
        issues.append(("Critical", "URL detected in content",
                       "Remove all URLs; external links are prohibited."))
    if re.search(r"(\d{3}[-\s]?\d{3}[-\s]?\d{4}|\bemail\b|@)", text or ""):
        issues.append(("Critical", "Possible phone/email/contact info",
                       "Remove contact details from listing content."))
    # score
    score = 100
    for sev, _, _ in issues:
        if sev == "Critical":
            score -= 15
        elif sev == "Warning":
            score -= 5
    score = max(0, score)
    return {"score": score, "issues": issues}


def _matches_redline(text: str, name: str) -> bool:
    """Lightweight heuristic match for a red-line description."""
    keywords = {
        "Competitor brand name in title/bullets": ["better than", "vs ", "competitor"],
        "Incentivized review language": ["review for", "free product for review", "refund for review"],
        "Phone / email / URL in listing": ["call us", "email us", "contact us at"],
        "HTML tags in plain description": ["<b>", "<br>", "<p>", "<img"],
        "ALL CAPS abuse": [],  # handled separately
        "Fake urgency": ["limited time", "last chance", "only 3 left", "sale ends today"],
        "Misleading superlatives": ["#1", "best seller", "world's best", "guaranteed"],
        "Unsupported certification claims": ["fcc certified", "ce certified", "ul certified"],
        "'Waterproof' without test standard": ["waterproof"],
        "'Made in Italy' unverifiable": ["made in italy"],
        "Disease treatment claims": ["cures", "prevents cancer", "treats diabetes"],
        "'FDA approved' for supplements": ["fda approved"],
        "False safety certifications": [],
        "Unverified compatibility": [],
        "'Dermatologist recommended' without proof": ["dermatologist recommended"],
        "Unqualified 'hypoallergenic'": ["hypoallergenic"],
        "'Food-grade' without material spec": ["food-grade", "food grade"],
        "Unsubstantiated heat resistance": [],
        "'Prevents SIDS'": ["prevents sids", "sids"],
        "'Treats fleas' without EPA registration": ["treats fleas", "flea treatment"],
    }
    for kw in keywords.get(name, []):
        if kw in text:
            return True
    return False
