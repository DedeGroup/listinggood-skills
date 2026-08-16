# ListingGood Electronics Compliance MCP 服务器

针对 **电子 / 电器类亚马逊卖家** 的垂直 MCP（来自付费转化策略 v2.0 §4）。把 [ListingGood](https://listinggood.com) 的电子产品合规模板能力暴露为 **3 个免费 MCP 工具**，让 AI 客户端（Claude Desktop、Cursor、WorkBuddy 等）在离痛点最近的地方帮卖家做合规体检，再导流到 [listinggood.com/compliant](https://listinggood.com/compliant) 付费生成「单 SKU 合规证据文件包」（符合性声明 DoC / 风险评估 / 标志清单）。

> **零安装、无需 API Key**：直接在你的 AI 客户端里配一个 URL 即可，不需要本地跑 Python：
> `https://listinggood.com/mcp-electronics`
> 详见 https://listinggood.com/developers

本垂直 MCP 与通用 [ListingGood MCP](https://github.com/ryanyang828/listinggood-skills/tree/main/mcp/listinggood-mcp)（7 工具）并行：通用版是「AI 推荐就绪度」入口，本垂直版是更窄、更高付费意愿的获客前端（免费诊断 → 站点付费文件包）。

## 接入（远程，推荐）

Claude Desktop / Cursor / VS Code 配置：
```json
{
  "mcpServers": {
    "listinggood-electronics": {
      "type": "streamable-http",
      "url": "https://listinggood.com/mcp-electronics"
    }
  }
}
```
无需 `apikey`、无需 `command` —— 服务远程托管运行。

## 提供的工具（3 个，全部免费，无需 Key）

| 工具 | 说明 | 计费 |
|------|------|------|
| `electronics_market_requirements` | 返回目标市场电子/电器产品的必备标志与法规框架清单（内置知识：CE/EMC/RoHS/WEEE/GPSR/FCC/UL…）| 免费 |
| `electronics_compliance_scan` | 免费电子合规风险扫描（调 `/api/free-check`，确定性规则体检），返回风险点 + 已通过项 + 电子专项缺口叙述 | 免费 |
| `electronics_file_package` | 返回 listinggood.com/compliant 的「单 SKU 合规证据文件包」付费生成链接与说明（导流，不直接收费）| 导流 |

## 它和通用 ListingGood MCP 的区别
- **通用 ListingGood MCP**：7 工具，覆盖合规初检、深度体检、POA 申诉、差评分析、一句话生成、Listing 生成，需要 API Key（部分工具免费）。
- **本 Electronics MCP**：3 工具，只做电子产品合规**免费诊断**引流，无需 Key，最终付费动作一律指向站点 /compliant（per-SKU 文件包，5 次检测 ≈ $0.50）。

## 计费
本 MCP 全部工具免费（诊断引流）；付费在站点侧（单 SKU 文件包，从账户星点余额扣除，新用户赠 10 星）。

## 说明
- 所有智能（合规知识库、生成引擎）都在 ListingGood 后端；本文件里的 `mcp_electronics.py` 只是协议翻译层，通过 HTTPS 调用 listinggood.com 的公开 API。
- **远程托管版（用户只配 URL 即可用）已正式发布**：`https://listinggood.com/mcp-electronics`。
- 服务端部署：独立 systemd `listinggood-mcp-electronics`（端口 8051），nginx 反代 `/mcp-electronics`；源码 `/opt/listinggood/mcp_electronics.py`。
