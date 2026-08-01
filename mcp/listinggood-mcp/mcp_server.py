#!/usr/bin/env python3
"""ListingGood MCP 服务器（本地 stdio 版，不托管在远端）。

把 ListingGood 真实后端能力暴露成 MCP 工具，供 Claude Desktop / Cursor / 任意
支持 MCP 的 AI 客户端原生调用。所有智能都在 ListingGood 后端（合规知识库 +
生成引擎 + 星点计费），本服务器只是「MCP 协议 ↔ 现有 HTTP API」的薄翻译层。

依赖（仅一个第三方包）：
    pip install "mcp>=1.0"

运行：
    export LISTINGGOOD_API_KEY=sk-xxxxxxxx
    python mcp_server.py

在 AI 客户端配置（以 Claude Desktop 为例，编辑 claude_desktop_config.json）：
    {
      "mcpServers": {
        "listinggood": {
          "command": "python",
          "args": ["/绝对路径/mcp_server.py"],
          "env": { "LISTINGGOOD_API_KEY": "sk-xxxxxxxx" }
        }
      }
    }

获取 API key：登录 listinggood.com 后访问 https://listinggood.com/api/user/apikey
计费（从星点钱包扣，新用户免费赠 10 星）：deep 3 星 / poa 10 星 / review 3 星 / compliance_check 免费
"""
import os
import json
import time
import urllib.request
import urllib.error
from mcp.server.fastmcp import FastMCP

BASE = os.environ.get("LISTINGGOOD_API_BASE", "https://listinggood.com")
mcp = FastMCP("listinggood")


def _req(method, path, token, data=None, timeout=120):
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


def _poll(task_id, token, tries=80):
    for _ in range(tries):
        st, body = _req("GET", "/api/task/" + task_id, token)
        if st == 200 and body.get("status") == "done":
            return body.get("result")
        if st == 200 and body.get("status") == "error":
            raise RuntimeError("后端错误：" + json.dumps(body, ensure_ascii=False))
        time.sleep(3)
    raise TimeoutError("任务超时未完成，请稍后重试")


def _require_key():
    key = os.environ.get("LISTINGGOOD_API_KEY")
    if not key:
        raise ValueError(
            "未配置 LISTINGGOOD_API_KEY。请设置环境变量，或登录 listinggood.com "
            "后访问 https://listinggood.com/api/user/apikey 获取。"
        )
    return key


def _submit(path, payload, token):
    key = _require_key()
    st, body = _req("POST", path, key, payload)
    if st == 401:
        return "错误：API key 无效（401）。请到 https://listinggood.com/api/user/apikey 检查。"
    if st == 402:
        return "错误：星点余额不足（402）。请到 https://listinggood.com 充值。"
    if st != 200:
        return "提交失败(%s)：%s" % (st, json.dumps(body, ensure_ascii=False))
    # 同步接口直接返回；异步接口含 task_id 需轮询
    if "task_id" in body:
        res = _poll(body["task_id"], key)
        return json.dumps(res, ensure_ascii=False, indent=2)
    return json.dumps(body, ensure_ascii=False, indent=2)


@mcp.tool()
def deep_compliance_scan(text: str, marketplace: str = "US", category: str = "") -> str:
    """对一段亚马逊 Listing 文案做深度合规体检，返回知识库驱动的风险报告（消耗 3 星）。
    text: Listing 标题/五点/描述原文；marketplace: 站点代码如 US/DE/JP/AE/SA/MX/BR；
    category: 可选类目，如 electronics / apparel。"""
    payload = {"text": text, "marketplace": marketplace}
    if category:
        payload["category"] = category
    return _submit("/api/scan/deep", payload, None)


@mcp.tool()
def generate_poa(text: str, marketplace: str = "US", violation_type: str = "") -> str:
    """根据亚马逊违规通知/下架邮件，生成可提交的 POA 申诉信（消耗 10 星）。
    text: 违规通知或下架邮件原文；marketplace: 站点代码；
    violation_type: 可选，如 ip_complaint / authenticity / policy。"""
    payload = {"text": text, "marketplace": marketplace}
    if violation_type:
        payload["violation_type"] = violation_type
    return _submit("/api/appeal/poa", payload, None)


@mcp.tool()
def analyze_review(text: str, marketplace: str = "US") -> str:
    """分析一条亚马逊差评，给出根因与回应建议（消耗 3 星）。
    text: 差评原文；marketplace: 站点代码。"""
    return _submit("/api/appeal/review", {"text": text, "marketplace": marketplace}, None)


@mcp.tool()
def compliance_check(text: str, marketplace: str = "US") -> str:
    """免费合规初检（不扣星点）：快速扫描明显红线词与类目风险，适合生成前先做一遍。
    text: Listing 文案；marketplace: 站点代码。"""
    return _submit("/api/compliance-check", {"text": text, "marketplace": marketplace}, None)


if __name__ == "__main__":
    mcp.run()  # 默认 stdio 传输
