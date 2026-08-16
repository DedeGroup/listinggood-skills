# ListingGood Toys Compliance MCP 服务器

针对 **玩具（Toys）类亚马逊卖家** 的垂直 MCP。把 [ListingGood](https://listinggood.com) 的Toys合规模板能力暴露为 **3 个免费 MCP 工具**，让 AI 客户端（Claude Desktop、Cursor、WorkBuddy 等）在离痛点最近的地方帮卖家做合规体检，再导流到 [listinggood.com/compliant](https://listinggood.com/compliant) 付费生成「单 SKU 合规证据文件包」（符合性声明 DoC / 风险评估 / 标志清单）。

> **零安装、无需 API Key**：直接在你的 AI 客户端里配一个 URL 即可，不需要本地跑 Python：
> `https://listinggood.com/mcp-toys`
> 详见 https://listinggood.com/developers

本垂直 MCP 与通用 [ListingGood MCP](https://github.com/ryanyang828/listinggood-skills/tree/main/mcp/listinggood-mcp)（7 工具）并行：通用版是「AI 推荐就绪度」入口，本垂直版是更窄、更高付费意愿的获客前端（免费诊断 → 站点付费文件包）。

## 接入（远程，推荐）

Claude Desktop / Cursor / VS Code 配置：
```json
{
  "mcpServers": {
    "listinggood-toys": {
      "type": "streamable-http",
      "url": "https://listinggood.com/mcp-toys"
    }
  }
}
```
无需 `apikey`、无需 `command` —— 服务远程托管运行。

## 提供的工具（3 个，全部免费，无需 Key）

| 工具 | 说明 | 计费 |
|------|------|------|
| `toys_market_requirements` | 返回目标市场Toys产品的必备标志与法规框架清单（内置知识）| 免费 |
| `toys_compliance_scan` | 免费Toys合规风险扫描（确定性规则体检），返回风险点 + 已通过项 + 专项缺口叙述 | 免费 |
| `toys_file_package` | 返回 listinggood.com/compliant 的「单 SKU 合规证据文件包」付费生成链接与说明（导流）| 导流 |

## 计费
本 MCP 全部工具免费（诊断引流）；付费在站点侧（单 SKU 文件包，从账户星点余额扣除，新用户赠 10 星）。

## 说明
- 所有智能（合规知识库、生成引擎）都在 ListingGood 后端；本文件里的 `mcp_toys.py` 只是协议翻译层。
- **远程托管版已正式发布**：`https://listinggood.com/mcp-toys`。
- 服务端部署：独立 systemd `listinggood-mcp-toys`（端口 8052），nginx 反代 `https://listinggood.com/mcp-toys`。
