# ListingGood — MCP Hub 提交指南（P1）

MCP server 源码已在仓库 `mcp/listinggood-mcp/`，公开仓库：
**https://github.com/ryanyang828/listinggood-skills**

安装命令（用户侧，无需 PyPI）：
```
pip install "git+https://github.com/ryanyang828/listinggood-skills.git#subdirectory=mcp/listinggood-mcp"
```
装完即可用命令 `listinggood-mcp` 启动 stdio 服务。

客户端配置（复制给用户）：
```json
{
  "mcpServers": {
    "listinggood": { "command": "listinggood-mcp" }
  }
}
```

---

## 1. mcp.so（最高优先级，目录型，不用 PyPI）
1. 打开 https://mcp.so → 右上角 **Submit** / **Add MCP Server**。
2. 填：
   - **Name**: `ListingGood Amazon Listing Tools`
   - **Repository / URL**: `https://github.com/ryanyang828/listinggood-skills`
   - **Description**: `Free, local, no-API-key Amazon listing tools over MCP: generate a full compliant listing, optimize titles for A9/A10, turn features into benefit-led bullets, and audit listings for compliance red lines. Works with Claude, Cursor, VS Code, Windsurf, Cline. Deep multi-marketplace scan at https://www.listinggood.com.`
   - **Category**: E-commerce / Developer Tools
3. 提交后等审核（通常几小时~1天），上线即出现在 mcp.so 搜索。

## 2. PulseMCP（目录型，不用 PyPI）
1. 打开 https://www.pulsemcp.com → **Submit a server** / **Add**。
2. 粘贴仓库 URL `https://github.com/ryanyang828/listinggood-skills`，填名称/描述（同上）。
3. 提交后进入目录，用户可一键复制各客户端配置。

## 3. Smithery（实际托管运行，需先发 PyPI）
- 先发 PyPI：`cd mcp/listinggood-mcp && pip install build twine && python -m build && twine upload dist/*`
  （需 PyPI 账号 + token，待 Ryan 提供）
- 仓库已备 `mcp/listinggood-mcp/smithery.yaml`。
- 发完 PyPI 后到 https://smithery.ai 用 GitHub 登录提交，或 `npx @smithery/cli@latest register .`

## 4. 官方 registry（registry.modelcontextprotocol.io，需 PyPI）
- 同上发 PyPI 后，按 https://registry.modelcontextprotocol.io 指引提交包名 `listinggood-mcp`。

---

## 导流钩子（所有 hub 描述统一带）
`Free tool by ListingGood — full SaaS with deep multi-marketplace compliance scan at https://www.listinggood.com/scan`

## 现状
- ✅ 仓库已含 `smithery.yaml` + 修正后的安装说明（git 直装，无需 PyPI）
- ⏳ mcp.so / PulseMCP 提交 = 表单操作，需 Ryan 登录或我代填（无登录凭证）
- ⏳ Smithery / 官方 registry = 待 PyPI 发版（需 PyPI token）
