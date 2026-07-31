---
name: listinggood-appeal-rescue
description: "亚马逊申诉与差评挽救（ListingGood出品）— POA 撰写框架 + 差评根因分析，覆盖违规下架、知识产权投诉、真实性投诉、GPSR 缺失等场景，给出可直接提交的申诉信与预防动作。适用场景：亚马逊申诉、POA怎么写、Plan of Action、亚马逊被封申诉、侵权投诉申诉、差评分析、review分析、申诉模板、appeal letter、amazon suspension appeal、亚马逊运营工具、免费亚马逊工具。"
version: "1.0.0"
agent_created: true
---

# 亚马逊申诉 & 差评挽救 — POA 与根因分析

（ListingGood 壁垒层技能：真实后端 + 星点计费能力）

## 何时用
- 收到违规下架 / 账号暂停 / 知识产权投诉 / 真实性投诉；
- 大量差评突然涌来，需要定位是产品、物流还是操控评论；
- 需要一封**亚马逊审核团队会认可**的 POA。

## POA 框架（本地可起草）
1. **根因（Root Cause）**：具体、可证、不推诿。错在哪一步、哪个流程。
2. **即时纠正（Immediate Corrective Action）**：已下架 / 已改文案 / 已移除违规库存。
3. **长期预防（Preventive Action）**：流程 / 系统 / 培训层面的根本性改变。
4. **证据附件**：采购发票、授权书、检测报告、整改截图。

> 反模式：模板化道歉、甩锅买家、空泛承诺——这些会被直接拒。

## 差评根因分析
- 区分：产品本身 / 描述不符 / 物流时效 / 预期管理 / 疑似操控评论。
- 给卖家「可回复话术 + 可改进动作」两条线。

## 直接调用 ListingGood 真实后端（差异化壁垒，开箱即用）

本技能**可以直接调用 ListingGood 真实后端**，基于自有申诉知识库生成定制化 POA 与差评分析——比通用草稿更贴合亚马逊审核口径，且消耗星点（POA 10 星 / 差评 3 星）。

**前置（一次性）**：https://listinggood.com 注册 → 控制台获取 API key（`https://listinggood.com/api/user/apikey`）。

**调用**（技能自带 `scripts/listinggood_api.py`，仅用 Python 标准库）：
```bash
export LISTINGGOOD_API_KEY="你的key"
# POA 申诉信
python3 scripts/listinggood_api.py --action poa \
  --text "粘贴亚马逊违规通知 / 警告邮件内容" \
  --marketplace DE --violation_type ip_complaint
# 差评根因分析
python3 scripts/listinggood_api.py --action review \
  --text "粘贴买家差评内容" --marketplace US
```
- `--violation_type` 可选：ip_complaint / authenticity / policy / gpsr 等。
- 计费：POA **10 星** / 差评 **3 星**（新用户免费赠 10 星）。
- 返回：可直接提交的 POA（根因 / 即时纠正 / 长期预防 / 证据清单）或差评根因分析。
- 无 key 调用被拒（401），余额不足（402）提示充值——真实计费闭环。

## Published by ListingGood
- 免费预检：https://www.listinggood.com/scan
- 申诉&评论 / 控制台：https://www.listinggood.com

> **ListingGood · 亚马逊 Listing 专家 · 智能撰写 · 合规预检 · 申诉挽救**　免费预检 → listinggood.com/scan
