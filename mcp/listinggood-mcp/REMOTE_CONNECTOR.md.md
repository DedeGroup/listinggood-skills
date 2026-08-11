# ListingGood 远程 MCP 连接器（Remote / streamable-http）

> 形态：智慧芽式 —— 用户只需在 MCP 客户端里填一个 **URL + 自己的 API Key**，零安装即可调用 ListingGood 真实后端。
> 端点：`https://listinggood.com/mcp?apikey=<你的Key>`（已部署于新加坡机，nginx 反代 `/mcp` → 独立进程 8050）

## 1. 获取你的 API Key
登录 listinggood.com → 访问 https://listinggood.com/api/user/apikey
（返回你的 `lg_live_xxx` Key；没有则自动生成。也可在 https://listinggood.com/developers 登录后一键复制含 Key 的完整配置。）

## 2. 接入方式

### WorkBuddy（推荐）
在连接器设置里添加 streamable-http 类型，URL 填：
```
https://listinggood.com/mcp?apikey=${LISTINGGOOD_API_KEY}
```
把 `LISTINGGOOD_API_KEY` 在连接器里填成你自己的 Key 即可。
已预置在 `~/.workbuddy/mcp.json`（`mcpServers.listinggood`）—— 在 WorkBuddy 连接器 UI 里填入 Key 即可启用。

### Claude Desktop / Cursor（通用 streamable-http）
编辑对应 `mcp.json`：
```json
{
  "mcpServers": {
    "listinggood": {
      "type": "streamable-http",
      "url": "https://listinggood.com/mcp?apikey=YOUR_KEY"
    }
  }
}
```

### 代码（Python）
```python
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async with streamablehttp_client("https://listinggood.com/mcp?apikey=YOUR_KEY") as (r, w, _):
    async with ClientSession(r, w) as s:
        await s.initialize()
        res = await s.call_tool("ai_readiness_check", {"text": "wireless earbuds", "marketplace": "US"})
```

## 3. 工具清单（7 个）
| 工具 | 后端 | 计费 | 说明 |
|------|------|------|------|
| `ai_readiness_check` | /api/free-check | 免费（无需 Key） | AI 推荐就绪度检测（合规健康度 + AI 可读性），获客钩子 |
| `compliance_check` | /api/compliance-check | 免费 | 生成前快速合规初检 |
| `compliance_scan` | /api/scan/deep | 3 星 | 深度合规体检，知识库驱动风险报告（异步） |
| `generate_poa` | /api/appeal/poa | 10 星 | 生成可提交 POA 申诉信（异步） |
| `analyze_review` | /api/appeal/review | 3 星 | 差评根因与回应建议（异步） |
| `fill_from_sentence` | /api/fill-from-sentence | 免费 | 一句话拆成结构化表单字段 |
| `generate_listing` | /api/generate | 每站 1 星 | 生成高转化多站点 Listing（异步） |

计费：1 星 = $0.10；新用户注册赠 10 星。余额不足返回 402 提示充值。

## 4. 认证原理
远程 MCP 服务**不存任何用户的 Key**。每次请求从 URL `?apikey=` 或 `Authorization: Bearer` 头提取 Key，
存入请求级 contextvar，转发到后端时写成 `Authorization: Bearer <key>`（复用 `current_user_id()`）。
→ 同一服务可服务所有用户，各自用自己的 Key（企业级、零耦合）。

## 5. 运维
- 进程：`systemctl status listinggood-mcp`（独立 venv `/opt/listinggood/mcp_venv`，Python 3.12，端口 8050）
- 源码：`/opt/listinggood/mcp_remote.py`
- 反代：`/etc/aa_nginx/aa_nginx.conf` 的 `location /mcp`（关闭缓冲，透传 Authorization）
- 升级：`uv pip install --python /opt/listinggood/mcp_venv "mcp==1.9.4"`，`systemctl restart listinggood-mcp`
- 注意：主站仍是 Python 3.8 venv，**切勿**把 mcp 装进主站 venv 或升级主站 Python；MCP 用独立 venv 隔离。

## 6. 与本地 stdio 版的区别
`mcp_server.py`（stdio）用于本机运行、Key 来自环境变量；`mcp_remote.py`（streamable-http）用于远程托管、
Key 来自每次请求。两者都只是「MCP 协议 ↔ 现有 HTTP API」的薄翻译层，智能全在后端。
