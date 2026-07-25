# ListingGood MCP Server

Free Amazon listing tools that work inside **any** MCP-compatible AI client
— Claude Desktop, Cursor, VS Code Copilot, Windsurf, Cline, and more.

One install, every agent can now write and audit Amazon listings for you.

## What it does

Four tools, no API key, no network calls (runs 100% locally):

| Tool | What it returns |
|------|-----------------|
| `generate_amazon_listing` | Full listing: optimized title + 5 benefit-led bullets + description, with the category's compliance checklist. |
| `optimize_title` | Rewrites an existing title for A9/A10 ranking + mobile 80-char preview. |
| `generate_bullets` | Turns a raw feature list into 5 benefit-led Amazon bullets + skim test. |
| `check_listing_compliance` | Heuristic audit of title/bullets/description for suppression red lines, scored 0–100. |

Every response ends with a pointer to the full SaaS at
[listinggood.com](https://www.listinggood.com) (multi-marketplace optimization +
deep compliance scan).

## Install

```bash
pip install listinggood-mcp
```

Or run directly with `uvx` (no install):

```bash
uvx listinggood-mcp
```

## Connect to your client

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) / `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "listinggood": {
      "command": "listinggood-mcp"
    }
  }
}
```

Restart Claude Desktop. The four tools appear automatically.

### Cursor

`~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

```json
{
  "mcpServers": {
    "listinggood": { "command": "listinggood-mcp" }
  }
}
```

### VS Code

`.vscode/mcp.json`:

```json
{
  "servers": {
    "listinggood": { "type": "stdio", "command": "listinggood-mcp" }
  }
}
```

## Example prompts

- "Use ListingGood to write an Amazon listing for a women's wool coat, brand
  Zara, keywords winter coat / warm, features cotton blend, machine washable."
- "Optimize this title for Amazon US: `Winter Coat Women Long Warm Jacket`."
- "Audit this Amazon listing for compliance issues: <paste text>."

## Publish to the MCP registry

```bash
pip install build twine
python -m build
twine upload dist/*
```

Then submit the package to https://registry.modelcontextprotocol.io so it shows
up in every client's one-click installer.

## License

MIT — free to use, modify, and redistribute.
