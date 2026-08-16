# ListingGood MCP 服务器

把 [ListingGood](https://listinggood.com) 的真实后端能力（AI 推荐就绪度、合规初检、深度合规体检、POA 申诉、差评分析、一句话生成、Listing 生成）暴露为 **MCP 工具**，供任意支持 MCP 的 AI 客户端（Claude Desktop、Cursor、WorkBuddy 等）原生调用。

> **推荐用法：远程托管版（零安装）**。直接在你的 AI 客户端里配一个 URL + API Key 即可，不需要本地跑 Python：
> `https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY`
> 详见 https://listinggood.com/developers

本目录同时保留**本地 stdio 启动方式**（面向想自己托管协议层的高级用户），但绝大多数用户用上面的远程 URL 就够了。

## 接入（远程，推荐）

Claude Desktop / Cursor 配置：
```json
{
  "mcpServers": {
    "listinggood": {
      "url": "https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY"
    }
  }
}
```
API Key 获取：登录 listinggood.com 后访问 https://listinggood.com/api/user/apikey （新用户送 10 星）。

## 本地 stdio 启动（可选）

```bash
pip install "mcp>=1.0"
export LISTINGGOOD_API_KEY=sk-xxxxxxxx
python mcp_server.py
```
Claude Desktop 配置：
```json
{
  "mcpServers": {
    "listinggood": {
      "command": "python",
      "args": ["/绝对路径/mcp_server.py"],
      "env": { "LISTINGGOOD_API_KEY": "sk-xxxxxxxx" }
    }
  }
}
```

## 提供的工具（7 个）

| 工具 | 说明 | 计费 |
|------|------|------|
| `ai_readiness_check` | AI 推荐就绪度扫描（合规健康度 + AI 可读性评分）| 免费 |
| `compliance_check` | 免费合规初检（需 Key）| 免费 |
| `compliance_scan` | 深度合规体检（知识库驱动报告）| 3 星 |
| `generate_poa` | 生成 POA 申诉信 | 10 星 |
| `analyze_review` | 差评根因分析 | 3 星 |
| `fill_from_sentence` | 一句话 → 结构化 Listing 字段 | 免费（需 Key）|
| `generate_listing` | 高转化 Listing 生成（标题 + 五点 + 描述，A9 优化）| 1 星/站点 |

## 它和 Skills 的区别
- **Skills**：一键安装的小插件，搜得到就装，适合广撒网获客（免费饵 → 壁垒层付费）。
- **MCP**：用户配置一个地址，AI 直接原生调用后端工具。门槛高一点，但深度集成、最黏——适合已意向的大客 / 开发者。

## 计费
从星点钱包扣除，新用户免费赠 10 星。余额不足时工具会返回「402 请充值」提示。

## 说明
- 所有智能（合规知识库、生成引擎）都在 ListingGood 后端；本地 `mcp_server.py` 只是协议翻译层，通过 HTTPS 调用 listinggood.com 的公开 API。
- **远程托管版（用户只配 URL 即可用）已正式发布**：`https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY`。
