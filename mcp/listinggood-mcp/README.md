# ListingGood MCP 服务器

把 [ListingGood](https://listinggood.com) 的真实后端能力（深度合规报告 / POA 申诉 / 差评分析 / 免费初检）暴露为 **MCP 工具**，供任意支持 MCP 的 AI 客户端（Claude Desktop、Cursor、WorkBuddy 等）原生调用。

> 这是「变现管 / 大客集成」层：给不想登网页、要批量嵌进自己工作流的高频 / 大卖家用的原生 API 接口。它和 9 个 Skills 共享同一个后端与星点计费。

## 它和 Skills 的区别
- **Skills**：一键安装的小插件，搜得到就装，适合广撒网获客（免费饵 → 壁垒层付费）。
- **MCP**：用户手动配置一个本地服务地址，AI 直接原生调用后端工具。门槛高一点，但深度集成、最黏——适合已意向的大客 / 开发者。

## 安装
```bash
pip install "mcp>=1.0"
```

## 配置 API key
登录 listinggood.com 后访问 https://listinggood.com/api/user/apikey 获取你的 key。

## 运行（stdio，本地）
```bash
export LISTINGGOOD_API_KEY=sk-xxxxxxxx
python mcp_server.py
```

## 接入 AI 客户端
以 Claude Desktop 为例，编辑 `claude_desktop_config.json`：
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
重启客户端后，即可在对话里直接说「帮我做一次深度合规体检」「写个 POA」，AI 会自动调用对应工具。

## 提供的工具
| 工具 | 说明 | 计费 |
|------|------|------|
| `deep_compliance_scan` | 深度合规体检（知识库驱动报告） | 3 星 |
| `generate_poa` | 生成 POA 申诉信 | 10 星 |
| `analyze_review` | 差评根因分析 | 3 星 |
| `compliance_check` | 免费合规初检 | 免费 |

## 计费
从星点钱包扣除，新用户免费赠 10 星。余额不足时工具会返回「402 请充值」提示。

## 说明
- 本服务器**不托管在 ListingGood 远端**，运行在你本地；它只通过 HTTPS 调用 listinggood.com 的公开 API。
- 所有智能（合规知识库、生成引擎）都在 ListingGood 后端，本文件只是协议翻译层。
- 远程托管版（用户只配 URL 即可用）暂未发布；如需可联系团队。
