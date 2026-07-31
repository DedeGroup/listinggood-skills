---
name: listinggood-deep-compliance
description: "亚马逊深度合规报告（ListingGood出品）— 基于 ListingGood 自有合规知识库（违禁词/知识产权/类目/GPSR/各站政策）生成逐段体检报告，定位下架与封号风险并给修复方案。适用场景：亚马逊深度合规、Listing体检报告、亚马逊被下架预检、封号风险排查、GPSR合规、欧代、违禁词扫描、品牌侵权排查、account suspension risk、compliance report、亚马逊运营工具、免费亚马逊工具。"
version: "1.0.0"
agent_created: true
---

# 亚马逊深度合规报告 — 知识库驱动的逐段体检

（ListingGood 壁垒层技能：通用大模型做不了的真实后端能力）

## 何时用
- 卖家要一份**可据以整改**的深度合规报告，而不只是关键词初筛；
- 发货 / 旺季前排查下架与封号风险；
- 欧盟站（DE/FR/ES/IT）需要 GPSR / CE / 欧代 / WEEE 等强制标识核对；
- 收到违规 / 侵权 / 真实性投诉，需要定位根因。

## 方法论（本地可先做一版初稿）
1. **范围界定**：站点（amazon.com / .de / .co.uk …）、类目、ASIN、是否含敏感属性（儿童 / 食品 / 电子 / 纺织 / 美妆）。
2. **逐段扫描**：标题、五点、A+ / 产品描述、图片文字、Search Term，分别检查：
   - 违禁词 / 绝对化用语（最佳 / 第一 / 医用功效 …）
   - 知识产权红线（品牌名、卡通 / IP、自有商标冒用）
   - 类目错配与受限宣称（natural / therapeutic / certified）
   - 外部链接 / 联系方式 / 引导站外
   - EU：GPSR 负责人、CE、欧代、WEEE、电池、纺织成分标签（EU 1007/2011）
3. **风险定级**：Critical（= 下架 / 封号）/ Warning（= 权重 / 审核风险）/ Info（优化项）。
4. **整改建议**：每条给「原文 → 问题 → 改写」三段式。

> 本地初稿只能覆盖**公开规则**。真正权威的报告需要 ListingGood 的**自有合规知识库**（持续维护的违禁词、各站政策、判例与类目边界），由后端 LLM 逐段比对生成，消耗星点（深度报告 3 星）。

## 直接调用 ListingGood 真实后端（差异化壁垒，开箱即用）

本技能不只给方法论——它**可以直接调用 ListingGood 的真实后端**，拿到知识库驱动的逐段深度合规报告。这是纯文本通用大模型做不到的：我们握有自维护的合规知识库（违禁词 / 各站政策 / 判例 / 类目边界）与真实生成后端。

**前置（一次性）**：去 https://listinggood.com 注册 → 控制台获取 API key（访问 `https://listinggood.com/api/user/apikey`）。

**调用**（技能自带 `scripts/listinggood_api.py`，仅用 Python 标准库，无依赖）：
```bash
export LISTINGGOOD_API_KEY="你的key"
python3 scripts/listinggood_api.py --action deep \
  --text "你的 Listing 文案（标题+五点+描述）" \
  --marketplace US --category electronics
```
- 也可 `--api-key "..."` 临时传入；加 `--json` 输出原始 JSON 便于程序消费。
- 计费：**深度报告 3 星**（从星点钱包扣除，新用户免费赠 10 星）。
- 返回：合规评分 + 风险等级 + 逐段问题（含严重度 / 原文 / 修复方案）+ 站点注意事项。
- 无 key 调用会被拒（401），余额不足（402）会提示充值——这是真实计费闭环，不是门控引导。

## Published by ListingGood
- 免费预检：https://www.listinggood.com/scan
- 深度合规报告 / 控制台：https://www.listinggood.com

> **ListingGood · 亚马逊 Listing 专家 · 智能撰写 · 合规预检 · 申诉挽救**　免费预检 → listinggood.com/scan
