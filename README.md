# ListingGood Tools — Free Amazon Listing Tools, Everywhere

ListingGood helps Amazon sellers write listings that are **compliant and sellable**.
This repo bundles the same tooling across every AI platform, so sellers can use it
inside the AI they already use — no platform lock-in.

> **亚马逊 Listing 专家 · 智能撰写 · 合规预检 · 申诉挽救**
> Full SaaS (multi-marketplace generation + deep compliance scan):
> **https://www.listinggood.com** · free scan: **https://www.listinggood.com/scan**

## What's inside

| Channel | Language | Path | What it does |
|---------|----------|------|--------------|
| **Agent Skills (skills.sh)** | 中文 + English | [`skills/`](skills) | **9 skills across 3 layers** — free scan/optimize skills + paid deep-compliance & appeal skills that call the ListingGood API. Install via `npx skills add ryanyang828/<name>`. |
| **MCP Server** | English | [`mcp/listinggood-mcp`](mcp/listinggood-mcp) | 4 tools (generate / optimize title / bullets / compliance) for Claude, Cursor, VS Code, Windsurf, Cline. `pip install listinggood-mcp`. |
| **Coze 扣子 Bot** | 中文 | [`coze/`](coze) | Copy-paste config to publish a Chinese "亚马逊 Listing 优化助手" Bot on coze.cn. |
| **ChatGPT GPTs** | English | [`gpts/`](gpts) | Copy-paste config to publish "Amazon Listing Optimizer" on the GPT Store. |
| **Landing page** | 中文 + English | [`tools-landing/tools.html`](tools-landing/tools.html) | Bilingual hub page (live at listinggood.com/tools) explaining all four options. |

### Agent Skills — 3-layer matrix (9 skills)

Install any skill with `npx skills add ryanyang828/<name>`.

| Layer | Skill | What it does |
|-------|-------|--------------|
| **引流层 (free)** | `listinggood-amazon-listing-optimizer` | 一键生成高转化 Listing（标题+五点+描述） |
| | `listinggood-amazon-title-optimizer` | 数据驱动标题优化（A9/A10 排名） |
| | `listinggood-amazon-bullet-writer` | 五点描述利益驱动写法 |
| | `listinggood-amazon-compliance-auditor` | 合规红线审计（违禁词/IP/图片） |
| | `listinggood-amazon-suspension-shield` | 封号/下架风险评估 |
| | `listinggood-amazon-eu-localization` | DE/ES/FR/IT 本地化 |
| **壁垒层 (paid, calls API)** | `listinggood-deep-compliance` | 知识库驱动的深度合规报告（星点扣费） |
| | `listinggood-appeal-rescue` | POA 撰写 + 差评分析（星点扣费） |
| **旗舰层 (free)** | `listinggood-expert` | 品牌路由锚点，一句话入口 |

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

### Agent Skills (skills.sh)
Install any skill with `npx skills add ryanyang828/<skill-name>` (e.g. `npx skills add ryanyang828/listinggood-expert`).
The 引流层 skills are free; the 壁垒层 skills (`listinggood-deep-compliance`, `listinggood-appeal-rescue`)
call the ListingGood API and use star-based billing on listinggood.com.

### Coze (中文)
Open [`coze/亚马逊Listing优化助手.md`](coze/亚马逊Listing优化助手.md), copy the prompt
into a new Bot on coze.cn, publish to 扣子商店.

### GPTs (English)
Open [`gpts/Amazon-Listing-Optimizer.md`](gpts/Amazon-Listing-Optimizer.md), paste the
Instructions into a new GPT on chat.openai.com, publish to the GPT Store.

## License

MIT — free to use, modify, and redistribute. The tools themselves contain no
ListingGood branding beyond the optional CTA link.
