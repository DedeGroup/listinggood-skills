#!/usr/bin/env python3
"""ListingGood 壁垒层 API 调用器（仅用标准库，无第三方依赖）。

让 ListingGood 技能直接调用官网真实后端，拿到知识库驱动的深度合规报告 / POA / 差评分析——
这是纯文本通用大模型做不到的真实后端能力。

用法：
  python3 listinggood_api.py --action deep   --text "..." --marketplace US --category electronics
  python3 listinggood_api.py --action poa    --text "..." --marketplace DE --violation_type ip_complaint
  python3 listinggood_api.py --action review --text "..." --marketplace US

API key：环境变量 LISTINGGOOD_API_KEY，或 --api-key。
  获取：登录 listinggood.com 后访问 https://listinggood.com/api/user/apikey
计费（从星点钱包扣除，新用户免费赠 10 星）：deep 3 星 / poa 10 星 / review 3 星
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

BASE_DEFAULT = "https://listinggood.com"
ENDPOINTS = {"deep": "/api/scan/deep", "poa": "/api/appeal/poa", "review": "/api/appeal/review"}


def _req(method, url, token, data=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {"error": str(e.reason)}


def run(action, text, marketplace, category, violation_type, api_key, base, as_json):
    if not api_key:
        sys.stderr.write("错误：未配置 API key。请设置环境变量 LISTINGGOOD_API_KEY，或用 --api-key。\n"
                         "获取：登录 listinggood.com 后访问 https://listinggood.com/api/user/apikey\n")
        return 2
    if not text or len(text.strip()) < 5:
        sys.stderr.write("错误：--text 不能为空（至少粘贴一段 Listing 文案 / 违规通知 / 差评内容）。\n")
        return 2

    payload = {"text": text.strip(), "marketplace": marketplace}
    if category:
        payload["category"] = category
    if action == "poa" and violation_type:
        payload["violation_type"] = violation_type

    st, body = _req("POST", base + ENDPOINTS[action], api_key, payload)
    if st == 401:
        sys.stderr.write("错误：API key 无效或未配置（401）。\n"); return 1
    if st == 402:
        sys.stderr.write("错误：星点余额不足（402）。请到 listinggood.com 充值。\n"); return 1
    if st != 200 or "task_id" not in body:
        sys.stderr.write("错误：提交失败（%s）：%s\n" % (st, json.dumps(body, ensure_ascii=False))); return 1

    task_id = body["task_id"]
    if not as_json:
        sys.stderr.write("已提交，任务 %s 处理中…\n" % task_id)

    result = None
    for _ in range(60):
        st, body = _req("GET", base + "/api/task/" + task_id, api_key)
        if st == 200 and body.get("status") == "done":
            result = body.get("result"); break
        if st == 200 and body.get("status") == "error":
            sys.stderr.write("后端错误：" + json.dumps(body, ensure_ascii=False) + "\n"); return 1
        time.sleep(3)

    if result is None:
        sys.stderr.write("超时：任务未完成，请稍后重试。\n"); return 1

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _pretty(action, result)
    return 0


def _pretty(action, r):
    if not isinstance(r, dict):
        print(json.dumps(r, ensure_ascii=False, indent=2)); return
    if action == "deep":
        print("合规评分：%s / 等级：%s" % (r.get("score"), r.get("level")))
        print("摘要：%s" % r.get("summary", ""))
        for it in r.get("issues", []):
            print("\n[%s] %s · %s" % (str(it.get("severity", "")).upper(),
                                      it.get("area", ""), it.get("finding", "")))
            if it.get("remediation"):
                print("  修复：" + it.get("remediation"))
    elif action == "poa":
        print(r.get("poa") or json.dumps(r, ensure_ascii=False, indent=2))
    elif action == "review":
        print(r.get("analysis") or json.dumps(r, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="ListingGood 壁垒层 API 调用器")
    ap.add_argument("--action", required=True, choices=["deep", "poa", "review"])
    ap.add_argument("--text", required=True, help="Listing 文案 / 违规通知 / 差评内容")
    ap.add_argument("--marketplace", default="US",
                    help="站点代码，如 US DE FR IT ES JP AE SA MX BR")
    ap.add_argument("--category", default=None, help="类目，可选，如 electronics / apparel")
    ap.add_argument("--violation_type", default=None,
                    help="仅 poa：违规类型，如 ip_complaint / authenticity / policy")
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = ap.parse_args()
    key = args.api_key or os.environ.get("LISTINGGOOD_API_KEY")
    sys.exit(run(args.action, args.text, args.marketplace, args.category,
                 args.violation_type, key, args.base, args.json))


if __name__ == "__main__":
    main()
