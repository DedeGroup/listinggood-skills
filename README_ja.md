# ListingGood AI Recommendation Engine（日本語）

**Amazon の AI に、あなたの商品を推薦させる。**
Make AI recommend your products.

ListingGood は、Amazon セラーの商品データを「AI ショッピングエージェント（ChatGPT / Gemini / Claude など）」が読み取り・推薦できる形に整えるエンジンです。A9 検索最適化だけでなく、AI カタログの選定基準もクリアします。

## 特徴
- 商品文を AI が読みやすい構造に変換（GEO 対応）
- Amazon コンプライアンス事前チェック（違禁語・知的財産・カテゴリ錯誤）
- 日本站（Amazon.co.jp）向け JCT インボイス・PSE・ACP 対応診断
- 無料の AI 推薦対応度スコア（AI Readiness Score）

## ツール一覧（7 ツール）
| ツール | 説明 |
|---|---|
| `ai_readiness_check` | 商品が AI に推薦されやすいかを診断（AI Readiness Score を返す） |
| `compliance_check` | コンプライアンス事前チェック（無料・違禁語/知財/カテゴリ） |
| `compliance_scan` | ディープコンプライアンス診断（段落ごと判定・修正提案） |
| `generate_listing` | 高転換 Amazon Listing を生成（タイトル+5点+説明） |
| `fill_from_sentence` | 一文の商品説明から Listing 項目を自動入力 |
| `generate_poa` | アカウント停止・知的財産苦情への POA（改善計画）を生成 |
| `analyze_review` | 低評価レビューの根本原因を分析・挽回策を提示 |

## 接続方法
エンドポイント（ストリーム可能 HTTP）：
```
https://listinggood.com/mcp?apikey=<YOUR_API_KEY>
```
1. ListingGood で API Key を発行（登録で 10 ★ 付与、無料）
2. 上記 URL の `<YOUR_API_KEY>` を差し替え
3. Claude / Cursor / Gemini 等の MCP クライアントに登録 → 即接続

## 設定例（mcp.json / claude_desktop_config.json）
{
  "mcpServers": {
    "listinggood": {
      "url": "https://listinggood.com/mcp?apikey=<YOUR_API_KEY>"
    }
  }
}

詳細: https://listinggood.com/developers
