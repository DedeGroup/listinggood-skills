# Amazon Compliance Rules Reference — Detailed Audit Checklist

Comprehensive rule reference for auditing Amazon listings. Organized by violation type and category.

## Universal Text Violations (All Categories)

### Will Trigger Automated Suppression
| Violation | Example | Amazon Policy Reference |
|-----------|---------|------------------------|
| Competitor brand name | "Better than Nike's running shoes" | Prohibited comparison |
| Incentivized review | "Free product for honest review" | Manipulated rankings |
| Contact information | "Call us at 555-1234" | External redirect prohibition |
| HTML in description (non-EBC) | `<b>Bold text</b>` | Formatting policy |
| URL in listing body | "Visit our site at..." | External link policy |

### Will Trigger Manual Review / Potential Suppression
| Violation | Example | Risk Level |
|-----------|---------|------------|
| Misleading superlatives | "#1 best seller", "world's best" | High |
| False urgency | "Only 2 left!", "Sale ends today!" | High |
| ALL CAPS abuse | "PREMIUM QUALITY GUARANTEED SHIPS FAST" | Medium-High |
| Unsupported certification | "FCC Certified" (no cert number) | High |
| Medical/health claims (non-medical cat) | "Cures back pain" (for a pillow) | Critical |
| Price claims | "Lowest price on Amazon" | Medium |
| Keyword stuffing | Same keyword in title + all 5 bullets | Medium |

## Category-Specific Rules

### Apparel / Fashion
- **"Waterproof"**: Requires verifiable test standard (AATCC 22, ISO 4920). Use "water-resistant" otherwise.
- **"Sweat-proof" / "Stain-proof"**: Same — needs lab test citation.
- **Origin claims**: "Made in Italy" must be factual and provable.
- **Size claims**: "True to size" must match measurements; "runs small" is subjective but acceptable if honest.
- **Material claims**: "100% cotton" must be accurate; "organic" requires certification.

### Supplements, Diet & Health (High-Enforcement Category)
- **Structure/Function claims**: Allowed ("supports immune health") with proper disclaimer.
- **Disease treatment claims**: Absolutely prohibited ("cures diabetes", "prevents cancer").
- **"FDA approved"**: FDA does not "approve" supplements — only "registered". This misuse is a common suppression trigger.
- **Required disclaimer structure**: "This statement has not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease."
- **Dosage claims**: Must be within safe limits; excessive dosage suggestions flagged.

### Electronics
- **Safety certifications**: CE, FCC, UL — only claim if certificate exists and number can be provided.
- **Compatibility claims**: "Works with iPhone" — must actually work; Apple MFi program required for certain connector types.
- **Wireless claims**: Bluetooth/WiFi versions must be accurate.

### Beauty & Personal Care
- **"Dermatologist tested/recommended"**: Need actual study or dermatologist name.
- **"Hypoallergenic"**: Must have testing to support; vague without specifics.
- **"Anti-aging" / "wrinkle reduction"**: Structure/function OK with disclaimer; cure claims prohibited.
- **Organic/natural claims**: Must meet regulatory definition (USDA Organic, etc.).

### Baby Products
- **Sleep position claims**: "Prevents SIDS" — absolutely prohibited.
- **Age appropriateness**: Must match CPSC/CPSIA guidelines.
- **Safety certifications**: Required for most categories (carriers, cribs, toys).

### Home & Kitchen
- **"Food-grade"**: Must cite specific standard (FDA CFR 21, BPA-free, LFGB for EU).
- **"Dishwasher/microwave safe"**: Must be true under normal use conditions.
- **Heat resistance claims**: Specific temperature ratings required ("up to 400°F").

### Pet Supplies
- **Health/treatment claims**: "Treats fleas" — requires EPA registration for such claims.
- **Feeding amount guarantees**: Must be based on nutritional analysis.
- **"Vet recommended"**: Needs substantiation.

## Image Compliance Rules

### Main Image Requirements (Strictly Enforced)
- Background: Pure white (RGB 255,255,255) only
- Product fill: ≥85% of image frame
- No text, logo, watermark, or inset on main image
- No additional objects (props, scenery)
- Professional lighting, sharp focus
- Minimum 1000px × 1000px (for zoom)
- Product must be real (no illustrations/renderings unless category allows)

### Secondary Images Rules
- Lifestyle/context images allowed but must accurately represent product
- Infographic text overlay: ≤20% of image area
- Size charts: allowed as secondary images
- Comparison charts: allowed if factual and non-misleading
- All images: min 1000px longest side, no borders

## Common Suppression Reasons & Fixes

| Suppression Reason | What It Means | How to Fix |
|--------------------|---------------|-----------|
| "Misleading product title" | Title doesn't match product | Rewrite to accurately describe |
| "Used item sold as new" | Condition mismatch | Check condition details |
| "Inaccurate product description" | Description doesn't match | Align text with actual product |
| "Image quality issues" | Main image fails white bg/fill check | Retake per requirements |
| "Restricted product" | Category requires approval | Apply for ungating |
| "Intellectual property complaint" | Brand owner reported | Submit Plan of Action |

## Scoring Weight Reference

For compliance score calculation:
- Critical issue: -15 points each
- Warning: -5 points each
- Base: 100 points
- Floor: 0 points
