#!/usr/bin/env python3
"""ListingGood · ListingGood Cosmetics Compliance MCP（远程托管版 · streamable-http）。

垂直品类 MCP（来自付费转化策略 v2.0 §4）：化妆品（Cosmetics）。定位 = **免费诊断引流**，
把"怕合规/怕下架"的卖家在离痛点最近的地方（AI agent 工作流）捞进来，
再导流到 listinggood.com/compliant 付费生成「合规证据文件包」（DoC / 风险评估 / 标志清单）。

与通用 mcp_remote.py 的关系（策略 §4）：
- 通用 MCP（7 工具）= "AI 推荐就绪度" 入口；本垂直 MCP = 更窄、更高付费意愿的获客前端。两者并行。
- 本 MCP 只做诊断（免费），不收费；收费动作一律指向站点 /compliant（per-SKU 文件包）。

运行（服务器，独立 venv / 独立端口 8053，零侵入主站）：
    LISTINGGOOD_API_BASE=http://127.0.0.1:8020 \
    python mcp_beauty.py            # 监听 127.0.0.1:8053，nginx 反代 /mcp-beauty

计费：本 MCP 全部工具免费（诊断引流）；付费在站点侧。
依赖：mcp>=1.3（streamable_http_app）、uvicorn、starlette（mcp 自带）。
工具清单（3 个，均免费、无需 Key）：
- beauty_market_requirements → 返回目标市场化妆品产品的必备标志/法规框架（内置知识）
- beauty_compliance_scan      → /api/free-check 风险扫描 + 化妆品专项缺口叙述（免费，无需 Key）
- beauty_file_package         → 返回站点 /compliant 付费文件包链接与说明（导流）
"""
import os
import json
import urllib.request
import urllib.error
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

BASE = os.environ.get("LISTINGGOOD_API_BASE", "http://127.0.0.1:8020").rstrip("/")
HOST = os.environ.get("MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("MCP_PORT", "8053"))

API_KEY_CTX: ContextVar = ContextVar("api_key", default=None)

# 化妆品（按市场区域）必备标志/法规框架 —— 内置知识，独立于主站模块。
FRAMEWORKS = {
    'EU': [
            ('EU Cosmetics Regulation 1223/2009', '化妆品法规（安全评估 + 责任人 + 通报）'),
            ('CPNP 通报', '化妆品通报门户（上市前通报）'),
            ('SCCS 意见（限用/准用物质）', '防腐剂/紫外线吸收剂/染发剂等限用物质'),
            ('INCI 成分标注', '全成分 INCI 命名标注'),
            ('Responsible Person (RP)', '欧盟责任人'),
            ('REACH (EC 1907/2006)', '化学品法规（香料过敏原 / SVHC）'),
            ('GPSR (EU 2023/988)', '通用产品安全法规（责任人 + 可追溯）'),
            ('26 种香料过敏原标注', '超标需标注'),
            ('纳米材料通报', '含纳米材料须通报'),
    ],
    'US': [
            ('FDA (FD&C Act / MoCRA 2022)', '美国化妆品监管（2022 现代化法案：设施注册 + 产品列名 + 不良事件报告）'),
            ('INCI 成分标注', '全成分标注'),
            ('California Prop 65', '含已知致癌/生殖毒性物质需警示'),
            ('GMP (良好生产规范)', 'GMP 生产规范'),
            ('色素添加剂 (FDA 批准)', '允许使用的着色剂'),
            ('OTC（若涉功效/药物宣称）', '药品声称走 OTC 路径'),
    ],
    'UK': [
            ('UK Cosmetics Regulation 2020', '英国化妆品法规'),
            ('UK Responsible Person', '英国责任人'),
            ('UK REACH', '英国化学品法规'),
            ('INCI 标注', '全成分标注'),
    ],
}

_REGION = {"US": "US", "UK": "UK", "CA": "US", "AU": "US", "JP": "EU", "AE": "EU",
           "SA": "EU", "BR": "US", "MX": "US"}
for _c in ("DE", "FR", "ES", "IT", "NL"):
    _REGION[_c] = "EU"

# Smithery 提分：给每个工具注入 outputSchema（均返回 JSON 字符串）。
_TOOL_OUTPUT_SCHEMA = {
    "type": "string",
    "description": "JSON string with the structured result.",
}
_OUTPUT_SCHEMAS = {
    "beauty_market_requirements": _TOOL_OUTPUT_SCHEMA,
    "beauty_compliance_scan": _TOOL_OUTPUT_SCHEMA,
    "beauty_file_package": _TOOL_OUTPUT_SCHEMA,
}
_ORIG_FASTMCP_LIST_TOOLS = FastMCP.list_tools


async def _patched_fastmcp_list_tools(self):
    tools = await _ORIG_FASTMCP_LIST_TOOLS(self)
    out = []
    for _t in tools:
        _name = getattr(_t, "name", None)
        if _name in _OUTPUT_SCHEMAS:
            _d = _t.model_dump(by_alias=True, exclude_none=True)
            _d["outputSchema"] = _OUTPUT_SCHEMAS[_name]
            out.append(type(_t).model_validate(_d))
        else:
            out.append(_t)
    return out


FastMCP.list_tools = _patched_fastmcp_list_tools

mcp = FastMCP("listinggood-beauty", streamable_http_path="/mcp-beauty")


# --------------------------------------------------------------------------- #
# HTTP 转发层
# --------------------------------------------------------------------------- #
def _req(method, path, token, data=None, timeout=30):
    url = BASE + path
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except Exception:
            return e.code, {"error": str(e.reason)}


def _get_key():
    return API_KEY_CTX.get()


# --------------------------------------------------------------------------- #
# 工具定义（全部免费，无需 Key —— 诊断引流）
# --------------------------------------------------------------------------- #
@mcp.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=False, open_world_hint=True))
def beauty_market_requirements(marketplace: str = "EU", lang: str = "en") -> str:
    """返回目标市场化妆品产品的必备标志与法规框架清单（内置知识，免费、无需 Key）。
    用于判断你的产品进入该市场前需具备哪些合规文件。
    marketplace: EU / US / UK（或站点代码如 DE/FR/US/UK）；lang: zh/en。"""
    region = _REGION.get((marketplace or "EU").upper(), "EU")
    fw = FRAMEWORKS.get(region, [])
    if lang == "zh":
        lines = ["# 化妆品 · %s 市场必备标志 / 法规框架" % region,
                 "> 来源：ListingGood 化妆品合规知识库（诊断用，非认证结论）。\n"]
        for n, d in fw:
            lines.append("- **%s** — %s" % (n, d))
        lines.append("\n下一步：在 listinggood.com/compliant 生成单 SKU 的「合规证据文件包」"
                     "（符合性声明 DoC + 风险评估 + 标志清单）。")
    else:
        lines = ["# Cosmetics · required marks / frameworks for %s" % region,
                 "> Source: ListingGood Cosmetics compliance knowledge (diagnostic, not a certification).\n"]
        for n, d in fw:
            lines.append("- **%s** — %s" % (n, d))
        lines.append("\nNext: generate a per-SKU compliance evidence file package "
                     "(DoC + risk assessment + marks checklist) at listinggood.com/compliant.")
    return json.dumps({"marketplace": marketplace, "region": region, "frameworks": fw,
                       "report": "\n".join(lines)}, ensure_ascii=False, indent=2)


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=False, open_world_hint=True))
def beauty_compliance_scan(text: str, marketplace: str = "US", lang: str = "en") -> str:
    """免费化妆品合规风险扫描（无需 Key）：对粘贴的 Listing 文案做确定性规则体检，返回风险点 +
    已通过项，并附化妆品专项缺口叙述。完整「合规证据文件包」（DoC/风险评估/标志清单）在站点付费生成。
    text: 标题+五点+描述原文；marketplace: 站点代码；lang: zh/en。"""
    payload = {"text": text, "marketplace": marketplace, "lang": lang, "source": "beauty"}
    st, body = _req("POST", "/api/free-check", None, payload, timeout=30)
    if st != 200:
        return json.dumps({"error": "后端扫描失败(%s)" % st, "detail": body}, ensure_ascii=False)
    region = _REGION.get((marketplace or "US").upper(), "EU")
    fw = FRAMEWORKS.get(region, [])
    if lang == "zh":
        note = ('\n\n## 化妆品专项提示\n该市场化妆品通常还需具备：%s。上述为「诊断」，完整的成分合规清单、安全评估报告与责任人文件请到 https://listinggood.com/compliant 生成（按 SKU 收费）。' % "、".join(n for n, _ in fw))
    else:
        note = ('\n\n## Cosmetics note\nCosmetics in this market typically also need: %s. The above is a diagnosis only. Generate the full ingredient compliance checklist, safety assessment and Responsible-Person file at https://listinggood.com/compliant (per-SKU).' % ", ".join(n for n, _ in fw))
    body["note"] = note
    return json.dumps(body, ensure_ascii=False, indent=2)


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=False, open_world_hint=True))
def beauty_file_package(sku: str, marketplace: str = "US", lang: str = "en") -> str:
    """返回 listinggood.com/compliant 的「单 SKU 合规证据文件包」付费生成链接与说明（导流，不直接收费）。
    包内含：符合性声明(DoC)模板、风险评估、必备标志/文件清单，并带蓝标「合规文件已备」。
    sku: 产品编号；marketplace: 站点代码；lang: zh/en。"""
    url = "https://listinggood.com/compliant"
    if lang == "zh":
        out = ('# 合规证据文件包（按 SKU 收费）\n- 链接：%s\n- SKU：%s\u3000目标市场：%s\n- 包含：成分合规清单 + 安全评估摘要 + 责任人/通报文件清单\n- 蓝标「合规文件已备」仅为文件齐备后的免费可视化副产品，ListingGood 不做认证结论。\n- 费用：每个 SKU 5 次合规检测（约 $0.50），从账户余额扣除。' % (url, sku, marketplace))
    else:
        out = ('# Compliance evidence file package (per-SKU, paid)\n- Link: %s\n- SKU: %s  Target market: %s\n- Includes: ingredient compliance checklist + safety-assessment summary + RP/filing checklist\n- The blue "Compliance file ready" mark is a free visual byproduct once files are assembled; ListingGood issues no certification verdict.\n- Cost: 5 compliance checks per SKU (approx $0.50), deducted from account balance.' % (url, sku, marketplace))
    return json.dumps({"url": url, "sku": sku, "marketplace": marketplace, "report": out},
                      ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
# 中间件：CORS（便于浏览器/跨域客户端连接）
# --------------------------------------------------------------------------- #
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key, Mcp-Session-Id, Accept",
}


class KeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        key = request.query_params.get("apikey")
        auth = request.headers.get("Authorization", "")
        if not key and auth.startswith("Bearer "):
            key = auth[7:].strip()
        if not key:
            key = (request.headers.get("X-API-Key") or "").strip()
        if key:
            API_KEY_CTX.set(key)
        if request.method == "OPTIONS":
            return Response(status_code=204, headers=CORS_HEADERS)
        resp = await call_next(request)
        for k, v in CORS_HEADERS.items():
            resp.headers.setdefault(k, v)
        return resp


def build_app():
    app = mcp.streamable_http_app()
    app.add_middleware(KeyMiddleware)
    # 健康检查必须放在 /mcp-beauty 前缀之外，否则会被 FastMCP session 中间件
    # 拦截并强制要求 Accept: text/event-stream，导致监控拿到 JSON-RPC 错误而非 200。
    app.add_route("/lg-beauty-health",
                  lambda r: JSONResponse({"ok": True, "service": "listinggood-mcp-beauty"}))
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(build_app(), host=HOST, port=PORT)
