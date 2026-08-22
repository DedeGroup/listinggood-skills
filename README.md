# ListingGood — AI Recommendation Engine (Skills + MCP)

> **Make AI recommend your products.** ListingGood is the engine that helps Amazon's AI — Rufus, COSMO, and agentic shopping agents — find, trust, and recommend your listings. It does this through three things: **compliance**, **AI writing**, and **appeal rescue**.

[![Website](https://img.shields.io/badge/website-listinggood.com-blue)](https://listinggood.com) [![MCP](https://img.shields.io/badge/MCP-server-green)](https://listinggood.com/developers) [![Free check](https://img.shields.io/badge/free%20check-no%20login-success)](https://listinggood.com/scan)

---

## Installation

ListingGood runs as a **hosted, remote Streamable HTTP MCP server** — there is nothing to install locally. Just point your MCP client at the endpoint with your API key.

**Endpoint:**

```
https://listinggood.com/mcp?apikey=YOUR_API_KEY
```

Get your free API key at **[listinggood.com/developers](https://listinggood.com/developers)** (signup grants 10 permanent stars).

### Claude Desktop / Cursor / VS Code / Windsurf / Cline

```json
{
  "mcpServers": {
    "listinggood": {
      "type": "streamable-http",
      "url": "https://listinggood.com/mcp?apikey=YOUR_API_KEY"
    }
  }
}
```

> No Docker build, no `npx` command, no local Python runtime — the API key is passed as a URL query parameter (`?apikey=...`) exactly as shown above.

---

## Why this exists

Amazon's discovery front-door has moved to AI. A listing that is **not machine-readable and compliance-clean** is far less likely to be cited inside Rufus answers, COSMO-driven recommendations, or agentic buying flows. Traditional seller tools tell you *what to sell* — they don't tell you whether your listing will be *recommended*.

ListingGood closes that gap:

- **Compliance pre-check** — flags risky claims and category issues *before* you publish (free, no login).
- **AI readability** — scores how well Amazon's AI surfaces can parse and cite your listing.
- **AI writing** — generates compliant titles, bullets, and descriptions.
- **Appeal rescue** — drafts a Plan of Action (POA) when a listing is suppressed.

The combined result is an **AI Recommendation Readiness Score** = compliance × 0.55 + AI readability × 0.45.

---

## Available Tools

### `ai_readiness_check`
Score how likely Amazon's AI (Rufus, COSMO) is to recommend a listing. Returns a combined AI Recommendation Readiness Score with actionable fixes. **Free, no API key required.**

### `compliance_check`
Fast pre-publish compliance gate: scans for red-line words and category risks before you generate or publish. **Free with API key.**

### `compliance_scan`
Deep, knowledge-base-driven compliance audit across prohibited terms, IP risk, category rules, and GPSR. Returns a written report. **2 credits.**

### `generate_listing`
Generate optimized title + bullets + description for selected marketplaces. **1 credit per marketplace.**

### `fill_from_sentence`
Turn a one-sentence product description into structured listing fields. **Free with API key.**

### `generate_poa`
Draft a submission-ready Plan of Action from an Amazon violation or suspension notice. **4 credits.**

### `analyze_review`
Analyze a negative review for root cause and a suggested response or POA angle. **2 credits.**

---

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

---

## Quick start

1. Get a free API key at **[listinggood.com/developers](https://listinggood.com/developers)**.
2. Add the server to your MCP client using the config block in [Installation](#installation).
3. Restart your client. ListingGood's tools appear as available MCP tools.

---

## Try it now (no account)

Run a free compliance + AI-readability check at **[listinggood.com/scan](https://listinggood.com/scan)** — paste your title and bullets, get a report in seconds.

---

## Links

- Website & free check: https://listinggood.com
- Developers / MCP config: https://listinggood.com/developers
- Changelog: https://listinggood.com/changelog

---

*ListingGood AI Recommendation Engine — make AI recommend your products.*
