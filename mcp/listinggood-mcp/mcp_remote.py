#!/usr/bin/env python3
"""ListingGood MCP 服务器（远程托管版 · streamable-http）。

部署在新加坡机，常驻进程 + nginx 反代 `/mcp`。用户只需在 WorkBuddy / 任意支持
streamable-http 的 MCP 客户端里填一个 URL + 自己的 ListingGood API Key，零安装即可
调用 ListingGood 真实后端（合规知识库 + 生成引擎 + 星点计费）。

与本地 stdio 版（mcp_server.py）的区别：
- 传输改为 streamable-http（对外暴露 URL，而非本机 python 进程）。
- API Key 不再来自环境变量，而是**每次请求**从 URL `?apikey=` 或 `Authorization: Bearer`
  头提取，存进 contextvar，转发到后端时用 `Authorization: Bearer <key>`。
  → 同一个 MCP 服务可服务多个用户，各自用自己的 Key（智慧芽同款形态）。
- 内部 BASE 指向本机主站 `http://127.0.0.1:8020`，不经公网。

运行（服务器，独立 venv / 独立端口，零侵入主站）：
    LISTINGGOOD_API_BASE=http://127.0.0.1:8020 \
    python mcp_remote.py            # 监听 127.0.0.1:8050，nginx 反代 /mcp

获取 API Key：登录 listinggood.com → https://listinggood.com/api/user/apikey
计费：deep 3 星 / poa 10 星 / review 3 星 / generate 每站点 1 星 / compliance_check 与
      fill_from_sentence 与 ai_readiness_check 免费。
依赖：mcp>=1.3（streamable_http_app）、uvicorn、starlette（mcp 自带）。

工具清单（7 个）：
- ai_readiness_check   → /api/free-check            （免费，无需 Key，获客钩子）
- compliance_check     → /api/compliance-check      （免费，需 Key）
- compliance_scan      → /api/scan/deep             （3 星，异步）
- generate_poa         → /api/appeal/poa             （10 星，异步）
- analyze_review       → /api/appeal/review          （3 星，异步）
- fill_from_sentence   → /api/fill-from-sentence     （免费，需 Key）
- generate_listing     → /api/generate               （每站点 1 星，异步）
"""
import os
import json
import time
import urllib.request
import urllib.error
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from mcp.server.fastmcp import FastMCP

# 内部转发目标：本机主站。公网请求经 nginx 进来，这里只走 localhost。
BASE = os.environ.get("LISTINGGOOD_API_BASE", "http://127.0.0.1:8020").rstrip("/")
HOST = os.environ.get("MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("MCP_PORT", "8050"))

# 每次请求的 API Key（由中间件从 URL/Header 提取后写入）。
API_KEY_CTX: ContextVar = ContextVar("api_key", default=None)

mcp = FastMCP("listinggood")


# --------------------------------------------------------------------------- #
# HTTP 转发层（薄翻译：MCP 工具 ↔ 现有 HTTP API）
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


def _poll(task_id, token, tries=100):
    for _ in range(tries):
        st, body = _req("GET", "/api/task/" + task_id, token, timeout=20)
        if st == 200 and isinstance(body, dict):
            status = body.get("status")
            if status == "done":
                return body.get("result")
            if status == "error":
                raise RuntimeError("后端任务失败：" + str(body.get("error", "未知错误")))
        time.sleep(3)
    raise TimeoutError("任务超时未完成（>5 分钟），请稍后在 /api/task/%s 查询。" % task_id)


def _get_key():
    return API_KEY_CTX.get()


def _friendly_error(st, body):
    if isinstance(body, dict):
        msg = body.get("error_en") or body.get("error") or json.dumps(body, ensure_ascii=False)
    else:
        msg = str(body)
    if st == 401:
        return ("错误：API Key 无效或未配置（401）。请在 MCP 客户端连接 URL 里带上 "
                "你的 ListingGood API Key：https://listinggood.com/mcp?apikey=<你的Key>\n"
                "Key 获取：登录 listinggood.com → /api/user/apikey")
    if st == 402:
        return "错误：星点余额不足（402）。请到 https://listinggood.com 充值后再试。\n" + msg
    if st == 429:
        return "错误：请求过于频繁（429），请稍后再试。"
    return "请求失败(%s)：%s" % (st, msg)


def _submit(path, payload, needs_key=True, timeout=30, poll=True):
    key = _get_key()
    if needs_key and not key:
        return ("错误：未检测到 API Key。请在 MCP 客户端连接配置里使用 "
                "https://listinggood.com/mcp?apikey=<你的ListingGood API Key>\n"
                "Key 获取：登录 listinggood.com → https://listinggood.com/api/user/apikey")
    st, body = _req("POST", path, key, payload, timeout=timeout)
    if st not in (200, 201):
        return _friendly_error(st, body)
    if not poll:
        return json.dumps(body, ensure_ascii=False, indent=2)
    if isinstance(body, dict) and "task_id" in body:
        try:
            res = _poll(body["task_id"], key)
        except (TimeoutError, RuntimeError) as e:
            return "任务已提交但：%s" % e
        return json.dumps(res, ensure_ascii=False, indent=2)
    return json.dumps(body, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
# 工具定义
# --------------------------------------------------------------------------- #
@mcp.tool()
def ai_readiness_check(text: str, marketplace: str = "US", lang: str = "en", email: str = "") -> str:
    """免费 AI 推荐就绪度检测（无需 API Key，获客钩子）：对粘贴的 Listing 文案做确定性规则扫描，
    返回合规健康度 + AI 可读性双维度评分与建议（不扣星点）。
    text: 标题+五点+描述原文；marketplace: US/DE/JP/AE/SA 等；lang: zh/en；
    email: 可选，留资后发送确认信并记录线索。"""
    payload = {"text": text, "marketplace": marketplace, "lang": lang, "source": "mcp"}
    if email:
        payload["email"] = email
    # free-check 无需鉴权
    st, body = _req("POST", "/api/free-check", None, payload, timeout=30)
    if st != 200:
        return _friendly_error(st, body)
    return json.dumps(body, ensure_ascii=False, indent=2)


@mcp.tool()
def compliance_check(text: str, lang: str = "en", category: str = "") -> str:
    """免费合规初检（需 API Key，不扣星点）：快速扫描明显红线词与类目风险，适合生成前先做一遍。
    text: Listing 文案；lang: zh/en；category: 可选类目如 electronics / apparel。"""
    payload = {"text": text, "lang": lang}
    if category:
        payload["category"] = category
    return _submit("/api/compliance-check", payload, needs_key=True, poll=False)


@mcp.tool()
def compliance_scan(text: str, marketplace: str = "US", category: str = "", lang: str = "en",
                    images: list = None) -> str:
    """深度合规体检（消耗 3 星，异步）：知识库驱动的风险报告，覆盖违禁词/知识产权/类目/GPSR 等。
    text: Listing 标题/五点/描述原文；marketplace: 站点代码；category: 可选类目；
    lang: zh/en；images: 可选，最多 5 张 data:image base64（单张 <4MB）。"""
    payload = {"text": text, "marketplace": marketplace, "lang": lang}
    if category:
        payload["category"] = category
    if images:
        payload["images"] = images
    return _submit("/api/scan/deep", payload, needs_key=True, timeout=60)


@mcp.tool()
def generate_poa(text: str, marketplace: str = "US", lang: str = "en", violation_type: str = "") -> str:
    """根据亚马逊违规通知/下架邮件生成可提交 POA 申诉信（消耗 10 星，异步）。
    text: 违规通知或下架邮件原文；marketplace: 站点代码；lang: zh/en；
    violation_type: 可选，如 ip_complaint / authenticity / policy。"""
    payload = {"text": text, "marketplace": marketplace}
    if violation_type:
        payload["violation_type"] = violation_type
    return _submit("/api/appeal/poa", payload, needs_key=True, timeout=60)


@mcp.tool()
def analyze_review(text: str, marketplace: str = "US", lang: str = "en") -> str:
    """分析一条亚马逊差评，给出根因与回应建议（消耗 3 星，异步）。
    text: 差评原文；marketplace: 站点代码；lang: zh/en。"""
    payload = {"text": text, "marketplace": marketplace}
    return _submit("/api/appeal/review", payload, needs_key=True, timeout=60)


@mcp.tool()
def fill_from_sentence(sentence: str, lang: str = "en") -> str:
    """AI 一句话生成（免费，需 API Key，不扣星点）：把口语化一句产品描述拆成结构化表单字段，
    供后续生成使用。sentence: 一句产品描述（4-1000 字）；lang: zh/en。"""
    payload = {"sentence": sentence, "lang": lang}
    return _submit("/api/fill-from-sentence", payload, needs_key=True, poll=False)


@mcp.tool()
def generate_listing(cn_name: str, sku: str, marketplaces: list = None, price: str = "",
                     lang: str = "en") -> str:
    """生成高转化亚马逊 Listing（按所选站点数计费，每站点 1 星，异步）：标题+五点+描述，
    覆盖多站点字符限制与 A9 优化。
    cn_name: 产品中文名（必填）；sku: 产品编号（必填）；marketplaces: 可选站点列表，
    默认全站（9 站）；price: 可选价格；lang: zh/en。"""
    payload = {"cn_name": cn_name, "sku": sku}
    if marketplaces:
        payload["marketplaces"] = marketplaces
    if price:
        payload["price"] = price
    return _submit("/api/generate", payload, needs_key=True, timeout=60)


# --------------------------------------------------------------------------- #
# 中间件：从请求取 API Key → contextvar；并补 CORS（便于浏览器/跨域客户端连接）
# --------------------------------------------------------------------------- #
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key, Mcp-Session-Id, Accept",
}


class KeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # 1) 提取 Key：URL ?apikey= 优先，其次 Authorization: Bearer，再次 X-API-Key
        key = request.query_params.get("apikey")
        auth = request.headers.get("Authorization", "")
        if not key and auth.startswith("Bearer "):
            key = auth[7:].strip()
        if not key:
            key = (request.headers.get("X-API-Key") or "").strip()
        if key:
            API_KEY_CTX.set(key)
        # 2) CORS 预检
        if request.method == "OPTIONS":
            return Response(status_code=204, headers=CORS_HEADERS)
        # 3) 正常处理
        resp = await call_next(request)
        for k, v in CORS_HEADERS.items():
            resp.headers.setdefault(k, v)
        return resp


# --------------------------------------------------------------------------- #
# 入口
# --------------------------------------------------------------------------- #
def build_app():
    app = mcp.streamable_http_app()
    app.add_middleware(KeyMiddleware)
    app.add_route("/health", lambda r: JSONResponse({"ok": True, "service": "listinggood-mcp"}))
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(build_app(), host=HOST, port=PORT)
