# ListingGood Tools — Free Amazon Listing Tools, Everywhere

ListingGood helps Amazon sellers write listings that are **compliant and sellable**.
This repo bundles the same tooling across every AI platform, so sellers can use it
inside the AI they already use — no platform lock-in.

> Full SaaS (multi-marketplace generation + deep compliance scan):
> **https://www.listinggood.com** · free scan: **https://www.listinggood.com/scan**

## What's inside

| Channel | Language | Path | What it does |
|---------|----------|------|--------------|
| **MCP Server** | English | [`mcp/listinggood-mcp`](mcp/listinggood-mcp) | 4 tools (generate / optimize title / bullets / compliance) for Claude, Cursor, VS Code, Windsurf, Cline. `pip install listinggood-mcp`. |
| **WorkBuddy Skills** | 中文 + English | [`skills/`](skills) | 4 ready-to-import skills (writer / compliance / title / bullets). Import the zip in WorkBuddy. |
| **Coze 扣子 Bot** | 中文 | [`coze/`](coze) | Copy-paste config to publish a Chinese "亚马逊 Listing 优化助手" Bot on coze.cn. |
| **ChatGPT GPTs** | English | [`gpts/`](gpts) | Copy-paste config to publish "Amazon Listing Optimizer" on the GPT Store. |
| **Landing page** | 中文 + English | [`tools-landing/tools.html`](tools-landing/tools.html) | Bilingual hub page (live at listinggood.com/tools) explaining all four options. |

## The distribution strategy

```
English world (overseas)              Chinese world (domestic)
─────────────────────────            ─────────────────────────
MCP Server  ← highest leverage        Coze 扣子 Bot  ← highest leverage
GPTs Store  (ChatGPT)                 WorkBuddy Skills (中英)
GitHub open source                    listinggood.com/tools (中文版)
listinggood.com/tools (英文版)
```

Every tool is **free, useful on its own**, and ends with a pointer to the full
SaaS. The flywheel: a seller finds a free tool in their AI → gets value →
upgrades to ListingGood for 8-marketplace generation + deep compliance scan.

## Quick start by channel

### MCP (recommended for developers)
```bash
pip install listinggood-mcp
```
Add to your client's `mcpServers` config, restart, done. See
[`mcp/listinggood-mcp/README.md`](mcp/listinggood-mcp/README.md).

### WorkBuddy Skills
Import each skill's folder (or zip) in WorkBuddy → Skills → Import.

### Coze (中文)
Open [`coze/亚马逊Listing优化助手.md`](coze/亚马逊Listing优化助手.md), copy the prompt
into a new Bot on coze.cn, publish to 扣子商店.

### GPTs (English)
Open [`gpts/Amazon-Listing-Optimizer.md`](gpts/Amazon-Listing-Optimizer.md), paste the
Instructions into a new GPT on chat.openai.com, publish to the GPT Store.

## License

MIT — free to use, modify, and redistribute. The tools themselves contain no
ListingGood branding beyond the optional CTA link.
