# ListingGood — MCP & Skills 分发策略（单一真相源）

> **本文件是 ListingGood MCP server 与 Skills 在各大目录 / 平台的提交、状态、更新方法的唯一对照源。任何新增或更新目录，先改这里，再执行。**
> 最后核实：2026-08-16

---

## 0. 产品真相（所有目录统一口径，禁止再用旧版「本地 stdio 安装」写法）

- **名称**：`ListingGood MCP`
- **定位 slogan**：Get recommended by Amazon's AI.（让 AI 主动推荐你的商品）
- **形态**：Hosted MCP server（远程托管，streamable-http）
- **接入地址**：`https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY` — **零安装，填 Key 即连**
- **Transport**：streamable-http ｜ **Auth**：API Key（query 参数 `apikey`）
- **获取 Key**：https://listinggood.com/api/user/apikey（新用户送 10 星入永久钱包）
- **差异化卖点**：不需要 `pip` / `uvx` 安装、不需要本地跑 Python。Claude / Cursor / 任意支持 MCP 的 AI 客户端，配一个 URL + Key 就能原生调用。
- **仓库**：https://github.com/DedeGroup/listinggood-skills
- **官网 / Developers**：https://listinggood.com/developers

---

## 1. 目录状态总表（2026-08-16 核实）

| 目录 | 状态 | 上线方式 | 备注 / 链接 |
|------|------|----------|-------------|
| **Glama** | ✅ live | `glama.json`（仓库根，Glama 自动同步） | 已收录 |
| **Smithery** | ✅ live（待优化）| 用户 `yangqi0828` 账号注册 | 缺 description / 评分 35/100 → 见 §4 |
| **官方 MCP Registry** | ✅ live | `server.json` + GitHub Actions `publish-mcp-registry.yml`（push 自动发布） | `io.github.DedeGroup/listinggood`，8/12 active，streamable-http |
| **MCP Market** | ✅ live | 已提交 | mcpmarket.com/zh/server/listinggood |
| **UIComet** | ✅ live | 已提交 | Google 可搜到 |
| **mcpservers.org** | ✅ 已提交 | 开放表单（本会话 8/16 提交，12h 审核） | 无需登录 |
| **mcp.so** | ✅ 已提交（待审核）| 开放表单 | 用户确认 8/16 提交 |
| **PulseMCP** | ❌ 不发 | 平台不让发 | **放弃，不再投入时间** |

> 结论：**没有重复提交**。Glama / Smithery / 官方 Registry / MCP Market / UIComet 此前已发布；本会话新增 mcpservers.org；mcp.so 由用户提交待审；PulseMCP 放弃。

---

## 2. 提交数据包（任何新目录直接抄这段）

- **Name**：`ListingGood MCP`
- **Short description（≤160 字符）**：
  `Hosted MCP server that lets Claude, Cursor, and any AI agent audit, optimize, and appeal Amazon listings — compliance checks, A9 title/bullet generation, POA appeals, review analysis. No install: connect with an API key. Free tier included.`
- **Long description**：
  `Get recommended by Amazon's AI. ListingGood is a hosted MCP server that makes your Amazon listings readable and recommendable by Amazon's AI shopping agents and ChatGPT / Gemini catalog filters. It exposes 7 tools — AI readiness check, compliance pre-check, deep compliance audit, POA appeals, review analysis, one-sentence listing builder, and high-converting listing generation — over a single streamable-HTTP endpoint. No pip install, no local Python: just paste the URL with your API key into Claude Desktop, Cursor, or any MCP client. Free tier included; points deducted only for deep scans / generation.`
- **Category**：E-commerce / Developer Tools / Marketing
- **Tags**：`amazon`, `mcp`, `listing`, `compliance`, `ai-agent`, `ecommerce`, `claude`, `cursor`
- **Repository**：https://github.com/DedeGroup/listinggood-skills
- **Homepage**：https://listinggood.com/developers
- **Endpoint**：`https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY`
- **Client config（Claude Desktop / Cursor）**：
  ```json
  {
    "mcpServers": {
      "listinggood": {
        "url": "https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY"
      }
    }
  }
  ```

### 7 个工具（统一口径，禁止用旧名 `deep_compliance_scan`）

| 工具名 | 计费 | 作用 |
|--------|------|------|
| `ai_readiness_check` | Free | AI 推荐就绪度扫描（合规健康度 + AI 可读性评分，零 token 规则引擎，不扣星）|
| `compliance_check` | Free（需 Key）| 生成前合规预检，快速扫红线词 / 类目风险 |
| `compliance_scan` | 3 ⭐ | 深度合规体检（知识库驱动报告：违禁词 / 知识产权 / 类目 / GPSR）|
| `generate_poa` | 10 ⭐ | 生成亚马逊申诉 POA 行动计划 |
| `analyze_review` | 3 ⭐ | 差评根因分析 + 回复 / POA 角度草拟 |
| `fill_from_sentence` | Free（需 Key）| 一句话 → 结构化 Listing 字段 |
| `generate_listing` | 1 ⭐/站点 | 高转化 Listing（标题 + 五点 + 描述，A9 优化，遵守各站点字符上限）|

---

## 3. 各目录更新方法

- **官方 MCP Registry**：改 `server.json` → push `main` → GitHub Actions 自动 `mcp-publisher publish`（workflow 监听 `server.json` 变更）。无需手动。
- **Glama**：改 `glama.json` → push → Glama 自动同步。
- **mcpservers.org / mcp.so**：开放表单提交；要改描述需进各自后台（mcp.so 需 GitHub 登录）。
- **MCP Market / UIComet**：已上线，改描述需进各自后台（通常 GitHub / Google 登录）。
- **Smithery**：见 §4。

---

## 4. Smithery 优化（需用户 `yangqi0828` 登录，助理无法代做）

**现状**：页面显示 `No description`、质量评分 **35/100**，影响点击与排名。
**根因**：Smithery 的源 `mcp/listinggood-mcp/mcp.json` 与 `README.md` 是旧版本地 stdio 写法，描述缺失 / 不准。

**修法 A（最省事，1 分钟）**：
1. 登录 https://smithery.ai （`yangqi0828` 账号）
2. 打开 https://smithery.ai/server/@yangqi0828/listinggood-mcp → **Edit**
3. 在 Description 粘贴下方文案 → Save

**修法 B（重注册，从仓库源读最新描述）**：
在本地克隆的 `mcp/listinggood-mcp/` 目录执行：
```bash
npx @smithery/cli@latest register .
```
（需 `npx` 登录 Smithery 账号；会从新增的 `smithery.yaml` 读取 description）

**推荐 Description 文案（直接粘贴）**：
> Get recommended by Amazon's AI. ListingGood is a hosted MCP server that makes your Amazon listings readable and recommendable by Amazon's AI shopping agents and ChatGPT / Gemini catalog filters. 7 tools: AI readiness check, compliance pre-check, deep compliance audit, POA appeals, review analysis, one-sentence listing builder, and high-converting listing generation. Zero install — connect with a URL and your API key.

---

## 5. Skills（9 个，已在 WorkBuddy 技能市场）

| Skill | 状态 |
|-------|------|
| listinggood-amazon-listing-optimizer | ✅ |
| listinggood-amazon-title-optimizer | ✅ |
| listinggood-amazon-bullet-writer | ✅ |
| listinggood-amazon-compliance-auditor | ✅ |
| listinggood-deep-compliance | ✅ |
| listinggood-amazon-eu-localization | ✅ |
| listinggood-amazon-suspension-shield | ✅ |
| listinggood-appeal-rescue | ✅ |
| listinggood-expert（总入口）| ✅ |

---

## 6. 历史坑（避免重复劳动 / 误判）

1. **不要再提交「本地 stdio pip 安装」版本**——产品已是远程托管（填 Key 即连）。旧 `MCP_HUBS_SUBMISSION.md` 写的 `pip install git+...` + `mcp_server.py` 是过时写法，已于 2026-08-16 重写。
2. **PulseMCP 不发**——平台限制，别再试。
3. **Google / Bing sitemap ping 端点已官方弃用**（Google 404 / Bing 410）——收录只能 GSC 手动「请求编入索引」。
4. **agent-browser 查 SPA（Smithery / 官方 Registry / mcp.so）要用渲染**，curl / WebFetch 会因 JS 未渲染误判成 404 / 不存在。
5. **PyPI 不需要**——Smithery / 官方 Registry 实际已上线，走的不是 PyPI 路径（旧文档误判需 PyPI）。
