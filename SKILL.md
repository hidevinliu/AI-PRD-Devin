---
name: AI-PRD-Devin
description: |
  Generate AI-implementable product requirement documents (PRDs) from one-line product ideas, vague app/site/tool requests, or feature concepts. Use when the user asks for PRD, 产品需求文档, 需求文档, AI 可执行 PRD, 产品规格, MVP 方案, app/site/tool planning, or developer handoff docs for AI coding assistants.
---

# Qiaomu AI PRD (Devin fork)

把一句模糊产品想法，写成产品经理、人类开发者和 AI 编程助手都能直接执行的 PRD。

> Devin 本地优化版（fork from 向阳乔木 qiaomu-ai-prd）。改动：①P0 核心模块强制写 `核心机制`（不许架空核心）；②关键数字单一事实源（跨章不打架）；③lint 只在正文查占位符、放过 JSON/ASCII/Markdown 链接。

Copyright (c) 向阳乔木（原作者）· 本地优化 by Devin
X: https://x.com/vista8
GitHub: https://github.com/joeseesun/

## Operating Mode

Run as a production-lite product specification skill.

Default assumptions:

- The user usually wants a finished PRD, not a questionnaire.
- If the input is only one sentence, infer the best conservative product direction and continue.
- Ask only when the answer would materially change product category, platform, safety, legal risk, budget, data ownership, or implementation scope.
- When a choice is needed, make the best default decision and give the reason inside the relevant chapter.
- Do not start implementation unless the user explicitly asks; this skill produces the PRD.
- Write Chinese-first unless the user asks for English.
- Output all 11 required chapters in order. Do not skip chapters, even in compact mode.
- Add an `AI 速读卡` before the chapters so an implementing agent can grasp the product in 10 lines or fewer.
- Keep implementation details out unless they affect product behavior, architecture risk, data contracts, verification, or AI handoff.
- Do not invent current competitor, API, platform, or package facts. If current facts matter and cannot be verified, mark them as unresolved or use `未知`.
- Treat fuzzy product words as direction, not proof. Translate them into concrete UI states, measurable targets, outputs, and acceptance criteria.
- Separate each important instruction into `硬约束`, `推荐默认`, or `发挥空间` so implementation agents know what must hold and where they can improve freely.

## Workflow

1. Parse the user input and optional mode tags from `references/modes-and-defaults.md`.
2. Decide the likely product category, target users, primary platform, and MVP surface.
3. Decide the product's `硬约束`, `推荐默认`, and `发挥空间`.
4. Identify facts that must be verified, assumptions that can be used safely, and unknowns that must be represented honestly.
5. Generate the PRD with the exact chapter contract in `references/prd-methodology.md`. Decide the key numbers (input limits, timeouts, thresholds) once in the `AI 速读卡` and reuse those exact values everywhere — never restate a different number for the same concept.
6. For each module, include realistic ASCII UI/state diagrams, normal flow, at least two failure paths, states, dependencies, and 1-3 real product decisions or `无`. For the module that delivers the P0 core value, also write a `核心机制` subsection: either an implementable sketch of the rules/algorithm/heuristic, or an explicit `关键未决项` with a safe default — never hand-wave the core as "准确率未知".
7. Add `超预期机会`: 2-4 product moments that can make the implementation feel memorable without bloating P0.
8. For differentiation and technical choices, explain structural causes and tradeoffs instead of saying competitors "did not think of it".
9. Give numeric performance targets with measurement methods and degradation thresholds.
10. Finish chapter 11 as a direct note to the implementing AI assistant using second person `你`, including acceptance scripts it can run or manually verify.
11. Run the self-check in `references/output-quality.md` before final output.
12. If the PRD is saved to a file, run `python3 scripts/lint_prd.py <file>` and fix any reported issue.
13. **（棒①·red-green 管线衔接）若本 PRD 将进入 `red-green-mode` 实现**（即 Devin 要把它做成代码并刷绿），额外产出一份 `acceptance-contract.json` —— 把第十一章的「验收剧本」逐条转成共享验收 SSOT，供 TDD 棒回填 verifier、red-green 棒做 GAP_CHECK + GATE。这是 PRD→TDD→red-green 三棒接力的第一棒交接物。
    - schema 每条：`id`（AC-01…）/ `scenario`（**行为级断言，禁写文件路径+行号**，防跨棒腐烂）/ `scenario_ref`（指回第十一章）/ `check_type`（test|smoke|lint|constraint）/ `expect` / `verifier`（①留 null，③TDD 回填）/ `depends_on`（[]）/ `status`（todo）。顶层带 `version:"1"` / `task` / `prd_source` / `items` / `anticheat_allows:[]`。
    - 产出后跑 `python3 ~/.agents/skills/red-green-mode/tools/acceptance_contract.py validate --file <contract>` 自检 schema（behavior-lint 会警告绑了路径行号的断言）。**不在这一棒 attest**（验证器命令要等 TDD 棒回填后才锁）。
    - 默认行为：纯文档型 / 不进 red-green 的 PRD **不强制**产契约；只有明确要走红绿灯实现时才产。

## Output Contract

When the user gives a product idea, output the PRD directly. Use this order:

1. `# [产品名] PRD`
2. `## AI 速读卡`
3. `## 第一章：产品概述`
4. `## 第二章：整体布局与导航`
5. `## 第三章：核心模块详细设计`
6. `## 第四章：超越竞品的差异化功能`
7. `## 第五章：数据模型`
8. `## 第六章：技术架构`
9. `## 第七章：交互细节`
10. `## 第八章：导出与输出系统`
11. `## 第九章：开发优先级`
12. `## 第十章：性能指标`
13. `## 第十一章：开发者交接说明`

Do not add a long preface. If assumptions are needed, place them inside the relevant chapter, usually `1.3 可行性边界`, module `待决问题`, or `第十一章 d) 已知的未知项`.

## Optional Modes

Recognize these tags anywhere in the user request:

- `[深度模式]`: add boundary-case analysis to each major module.
- `[精简模式]`: keep every chapter, but focus detailed design on P0; mark lower tiers as `待扩展`.
- `[前端视角]`: add component decomposition and state-management guidance where product-relevant.
- `[后端视角]`: add API design and database schema where product-relevant.
- `[移动优先]`: make all layout diagrams mobile-first unless the product is clearly desktop-only.
- `[竞品深挖]`: deepen competitor weakness analysis and product blind-spot reasoning.
- `[商业化]`: add pricing, paid feature, and monetization implications where appropriate.
- `[开源友好]`: prefer permissive open-source libraries, especially MIT, when the choice does not harm the product.

See `references/modes-and-defaults.md` for how to combine modes.

## Quality Bar

A strong PRD from this skill:

- makes product decisions instead of pushing every ambiguity to the user
- gives an implementing agent a short `AI 速读卡`
- distinguishes `硬约束`, `推荐默认`, and `发挥空间`
- contains realistic ASCII diagrams with actual labels and representative content
- names meaningful competitor differences instead of filling a comparison table with obvious parity
- defines module states, data flows, failure paths, and open decisions
- includes a small set of `超预期机会` that invite tasteful implementation beyond the baseline
- uses data structures with commented JSON fields and a top-level `version`
- explains technical choices and package-size uncertainty honestly
- explains when a technical choice is replaceable and what must remain invariant
- prioritizes by user behavior impact, not implementation difficulty
- turns performance expectations into exact numbers and measurement methods
- tells the implementing AI what to build first, what not to reinterpret, what to freely improve, what remains unknown, and how to verify the first build

Reject or revise a PRD that:

- leaves placeholders such as `[产品名]`, `按钮 A`, `TODO`, or `待补充`
- uses vague performance language such as `快`, `流畅`, `轻量`, or `可扩展` instead of numbers
- claims impossible browser, iOS, Android, web, AI model, or export capabilities
- invents competitor facts, package sizes, or platform limits
- has no honest known-unknown item in chapter 11
- lacks `验收剧本` for implementation verification
- lists P0 as a wishlist instead of the smallest usable product

## Reference Files

- `references/prd-methodology.md`: the required 11-chapter PRD structure and detailed generation rules.
- `references/modes-and-defaults.md`: lazy-user defaults, optional modes, question policy, and uncertainty handling.
- `references/output-quality.md`: output self-check and common failure patterns.
- `scripts/lint_prd.py`: lightweight checker for required chapters, unresolved placeholders, vague performance terms, and structural omissions.
