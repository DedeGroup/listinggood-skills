# ListingGood MCP

**Get recommended by Amazon's AI.**

ListingGood is an AI Recommendation Engine for Amazon sellers. As Amazon's shopping agents (and ChatGPT / Gemini's catalog filters) begin deciding what gets recommended, the winning products are the ones those agents can read and trust. **ListingGood's hosted MCP server plugs that capability straight into your AI assistant** — zero install, just a URL and your API key.

## What it does

7 tools that make your listings compliant, readable, and recommendable:

| Tool | Stars | What it does |
|------|-------|--------------|
| `ai_readiness_check` | Free | AI recommendation readiness scan — compliance health + AI readability scores |
| `compliance_check` | Free | Quick compliance pre-check before generation |
| `compliance_scan` | 3 ⭐ | Deep knowledge-base driven audit (prohibited words, IP, category, GPSR) |
| `generate_poa` | 10 ⭐ | Plan of Action for Amazon appeals |
| `analyze_review` | 3 ⭐ | Negative-review analysis + response draft |
| `fill_from_sentence` | Free | One-sentence → structured Listing fields |
| `generate_listing` | 1 ⭐/marketplace | High-converting Listing (title + bullets + description, A9 optimized) |

## Connect (remote, no install)

```
https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY
```

- **Transport**: Streamable HTTP
- **Auth**: API Key in the `apikey` query parameter
- Get your key at **https://listinggood.com/api/user/apikey** (new users get 10 free stars)

### Claude Desktop / Cursor config

```json
{
  "mcpServers": {
    "listinggood": {
      "url": "https://listinggood.com/mcp?apikey=YOUR_LISTINGGOOD_API_KEY"
    }
  }
}
```

## Listed on

- [Smithery](https://smithery.ai/server/@yangqi0828/listinggood-mcp)
- [mcp.so](https://mcp.so/server/listinggood-amazon-listing-tools) (remote, under review)
- Glama · PulseMCP · Official MCP Registry (coming)

## Links

- Website: https://listinggood.com
- Developers: https://listinggood.com/developers
- API key: https://listinggood.com/api/user/apikey

## License

MIT
