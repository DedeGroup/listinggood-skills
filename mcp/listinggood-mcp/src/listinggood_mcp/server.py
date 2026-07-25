"""ListingGood MCP Server — free Amazon listing tools for any MCP client.

Exposes 4 tools: generate_amazon_listing, optimize_title,
generate_bullets, check_listing_compliance.

Works with Claude Desktop, Cursor, VS Code, Windsurf, Cline, and any
MCP-compliant client. Self-contained: no API key, no network calls.
"""

from mcp.server.fastmcp import FastMCP
from .knowledge import (
    CTA, build_title, build_bullets, build_description, audit_compliance,
    get_title_pattern, get_redlines, TITLE_LIMITS, BULLET_LIMIT, HARD_REDLINES,
)

mcp = FastMCP("listinggood")


@mcp.tool()
def generate_amazon_listing(
    product_name: str,
    category: str = "generic",
    brand: str = "",
    keywords: str = "",
    features: str = "",
    marketplace: str = "us",
) -> str:
    """Generate a complete, compliant Amazon listing (title + 5 bullets + description).

    Args:
        product_name: What the product is, e.g. "Women's Wool Blend Coat".
        category: One of apparel, electronics, home, beauty, supplements, baby, pet, generic.
        brand: Your brand name (optional but recommended — front-loads trust).
        keywords: Comma-separated primary search keywords, e.g. "winter coat, wool, warm".
        features: Comma-separated raw features to translate into benefit-led bullets.
        marketplace: Target marketplace code: us, ca, de, uk, eu, jp, in, fr, it, es.
    """
    kws = [k.strip() for k in (keywords or "").split(",") if k.strip()]
    feats = [f.strip() for f in (features or "").split(",") if f.strip()]

    title = build_title(brand, product_name, kws, feats, marketplace)
    pattern = get_title_pattern(category)
    bullets = build_bullets(product_name, feats, category)
    description = build_description(product_name, bullets, category)

    limit = TITLE_LIMITS.get((marketplace or "us").lower(), 200)
    out = []
    out.append(f"# Amazon Listing — {product_name} ({marketplace.upper()})")
    out.append("")
    out.append(f"## Title ({len(title)}/{limit} chars)")
    out.append(title)
    out.append("")
    out.append(f"Title pattern used: {pattern['pattern']}")
    out.append(f"Example: {pattern['example']}")
    out.append("")
    out.append("## Bullet Points (benefit-led, each <{} chars)".format(BULLET_LIMIT))
    for i, (header, body) in enumerate(bullets, 1):
        out.append(f"{i}. **{header}** — {body}")
    out.append("")
    out.append("## Product Description (plain text)")
    out.append(description)
    out.append("")
    out.append("## Compliance checklist before you publish")
    hard, cat_lines = get_redlines(category)
    out.append("Universal red lines to avoid:")
    for name, fix in hard:
        out.append(f"- ❌ {name} → {fix}")
    if cat_lines:
        out.append(f"Category-specific ({category}) red lines:")
        for name, fix in cat_lines:
            out.append(f"- ⚠️ {name} → {fix}")
    out.append(CTA)
    return "\n".join(out)


@mcp.tool()
def optimize_title(
    current_title: str,
    category: str = "generic",
    marketplace: str = "us",
    primary_keyword: str = "",
) -> str:
    """Rewrite an existing Amazon title for A9/A10 ranking + mobile readability.

    Args:
        current_title: Your existing title text.
        category: One of apparel, electronics, home, beauty, supplements, baby, pet, generic.
        marketplace: Target marketplace code (us, de, uk, jp, ...).
        primary_keyword: The single most important search term to front-load.
    """
    limit = TITLE_LIMITS.get((marketplace or "us").lower(), 200)
    pattern = get_title_pattern(category)
    words = current_title.replace(" - ", " ").split()
    kw = (primary_keyword or "").strip()
    reordered = []
    if kw and kw.lower() not in " ".join(words).lower():
        reordered.append(kw)
    reordered.extend(words)
    new_title = " ".join(reordered)
    if len(new_title) > limit:
        truncated = []
        total = 0
        for w in new_title.split(" "):
            if total + len(w) + 1 > limit:
                break
            truncated.append(w)
            total += len(w) + 1
        new_title = " ".join(truncated).rstrip(" -,")

    out = []
    out.append("# Title Optimization")
    out.append("")
    out.append(f"**Current ({len(current_title)} chars):** {current_title}")
    out.append("")
    out.append(f"**Optimized ({len(new_title)}/{limit} chars):** {new_title}")
    out.append("")
    out.append("## Why this ranks better")
    out.append(f"- Pattern applied: {pattern['pattern']}")
    if kw:
        out.append(f"- Primary keyword '{kw}' front-loaded into first ~50 chars (highest A9 weight).")
    out.append("- Mobile rule: first 80 chars must state brand + what-it-is + click reason.")
    out.append("- Removed superlatives / filler that waste prime SEO real estate.")
    out.append("")
    out.append("## Mobile 80-char preview")
    out.append(f"\"{new_title[:80]}{'…' if len(new_title) > 80 else ''}\"")
    out.append(CTA)
    return "\n".join(out)


@mcp.tool()
def generate_bullets(
    product_name: str,
    features: str = "",
    category: str = "generic",
) -> str:
    """Turn a list of raw product features into 5 benefit-led Amazon bullets.

    Args:
        product_name: The product name.
        features: Comma-separated raw features, e.g. "cotton material, machine washable, non-slip sole".
        category: One of apparel, electronics, home, beauty, supplements, baby, pet, generic.
    """
    feats = [f.strip() for f in (features or "").split(",") if f.strip()]
    bullets = build_bullets(product_name, feats, category)
    out = []
    out.append(f"# Amazon Bullet Points — {product_name}")
    out.append("")
    out.append(f"Target length: 200–300 chars each (mobile-first). Max {BULLET_LIMIT}.")
    out.append("")
    for i, (header, body) in enumerate(bullets, 1):
        out.append(f"{i}. **{header}** — {body}")
    out.append("")
    out.append("## Skim test (read only the headers)")
    out.append(" ".join(h for h, _ in bullets))
    out.append("")
    out.append("If the headers alone don't tell what-it-is / why-buy / why-trust, "
               "rewrite them to be more specific.")
    out.append(CTA)
    return "\n".join(out)


@mcp.tool()
def check_listing_compliance(
    listing_text: str,
    category: str = "generic",
) -> str:
    """Audit an Amazon listing for compliance red lines (suppression risks).

    Args:
        listing_text: The title + bullets + description text to audit.
        category: One of apparel, electronics, home, beauty, supplements, baby, pet, generic.
    """
    report = audit_compliance(listing_text, category)
    out = []
    out.append("# Listing Compliance Audit")
    out.append("")
    score = report["score"]
    verdict = "PASS" if score >= 90 else ("REVIEW" if score >= 70 else "RISK")
    out.append(f"**Compliance score: {score}/100 — {verdict}**")
    out.append("")
    if report["issues"]:
        out.append("## Issues found")
        for sev, name, fix in report["issues"]:
            icon = "🔴" if sev == "Critical" else "🟡"
            out.append(f"{icon} **[{sev}]** {name}")
            out.append(f"   → Fix: {fix}")
    else:
        out.append("✅ No red-line issues detected in this text.")
    out.append("")
    out.append("## Scoring")
    out.append("- Base 100. Critical issue: -15 each. Warning: -5 each. Floor 0.")
    out.append("")
    out.append("Note: this is a heuristic pre-check. For a full multi-marketplace ")
    out.append("deep-scan with category policy matching, use:")
    out.append("https://www.listinggood.com/scan")
    out.append(CTA)
    return "\n".join(out)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
