# ListingGood — AI Recommendation Engine (Skills + MCP)

> **Make AI recommend your products.** ListingGood is the engine that helps Amazon's AI — Alexa for Shopping, the COSMO intent model, and agentic auto-buy — find, trust, and recommend your listings. It does this through three things: **compliance**, **AI writing**, and **appeal rescue**.

[![Website](https://img.shields.io/badge/website-listinggood.com-blue)](https://listinggood.com) [![MCP](https://img.shields.io/badge/MCP-server-green)](https://listinggood.com/developers) [![Free check](https://img.shields.io/badge/free%20check-no%20login-success)](https://listinggood.com/scan)

---

## Why this exists

Amazon's discovery front-door has moved to AI. A listing that is **not machine-readable and compliance-clean** is far less likely to be cited inside Alexa for Shopping, COSMO answers, or agentic buying flows. Traditional seller tools tell you *what to sell* — they don't tell you whether your listing will be *recommended*.

ListingGood closes that gap:

- **Compliance pre-check** — flags risky claims and category issues *before* you publish (free, no login).
- **AI readability** — scores how well Amazon's AI surfaces can parse and cite your listing.
- **AI writing** — generates compliant titles, bullets, and descriptions.
- **Appeal rescue** — drafts a Plan of Action (POA) when a listing is suppressed.

The combined result is an **AI Recommendation Readiness Score** = compliance × 0.55 + AI readability × 0.45.

## What's in this repo

This repository bundles ListingGood's **agent skills** and **MCP server** config so AI agents and power users can call ListingGood programmatically:

| Package | What it does |
|---|---|
| `listinggood-expert` | All-in-one Amazon listing expert: write · compliance pre-check · appeal rescue |
| `listinggood-amazon-listing-optimizer` | High-conversion listing generation (title + bullets + description) |
| `listinggood-amazon-compliance-auditor` | Compliance audit with Critical/Warning/Info grading |
| `listinggood-deep-compliance` | Deep, knowledge-base-backed compliance report |
| `listinggood-appeal-rescue` | POA drafting + negative-review root-cause analysis |
| `listinggood-amazon-title-optimizer` | A9/A10 title optimization |
| `listinggood-amazon-bullet-writer` | Benefit-led bullet points |
| `listinggood-amazon-eu-localization` | EU marketplace (DE/ES/FR/IT) localization |
| **MCP server** | 7 tools (free check, deep scan, AI generation, POA, …) + vertical MCPs (Electronics / Toys / Beauty / Home) |

## Quick start — connect the MCP

1. Get a free API key at **[listinggood.com/developers](https://listinggood.com/developers)**.
2. Add the server to your MCP client:

```json
{
  "mcpServers": {
    "listinggood": {
      "url": "https://listinggood.com/mcp?apikey=<YOUR_API_KEY>",
      "transport": "streamable-http"
    }
  }
}
```

3. Restart your client. ListingGood's tools appear as available MCP tools.

> This is a **remote Streamable HTTP MCP server** — no local install, Docker build, or `npx` command is required. The API key is passed as a URL query parameter (`?apikey=...`) exactly as shown above.

## Tools

The MCP server exposes the following tools:

| Tool | What it does | Cost |
|---|---|---|
| `ai_readiness_check` | **Score** — the only tool returning a combined AI-recommendation-readiness number (compliance ×0.55 + readability ×0.45), instant | Free, no API key |
| `compliance_check` | **Quick gate** — fast red-line-word + category-risk scan before you write; shallow and instant, not a full audit | Free with API key |
| `compliance_scan` | **Deep report** — knowledge-base-driven full compliance audit (prohibited words, IP, category, GPSR, image support); a written report, not a quick check | 2 credits |
| `generate_listing` | Generate optimized title + bullets + description for selected marketplaces | 1 credit per marketplace |
| `fill_from_sentence` | Turn a one-sentence product description into structured listing fields | Free with API key |
| `generate_poa` | Draft an appeal Plan of Action from an Amazon violation notice | 4 credits |
| `analyze_review` | Analyze a negative review for root cause and a suggested response | 2 credits |

> **Three compliance tiers** — pick by depth, not by name: `ai_readiness_check` returns a *score*, `compliance_check` is a *quick pre-publish gate*, and `compliance_scan` is a *deep async written report*.

All paid tools return a task ID and poll until completion. The free `ai_readiness_check` returns results immediately.

## Try it now (no account)

Run a free compliance + AI-readability check at **[listinggood.com/scan](https://listinggood.com/scan)** — paste your title and bullets, get a report in seconds.

## Links

- Website & free check: https://listinggood.com
- Developers / MCP config: https://listinggood.com/developers
- Changelog: https://listinggood.com/changelog

---

*ListingGood AI Recommendation Engine — make AI recommend your products.*
