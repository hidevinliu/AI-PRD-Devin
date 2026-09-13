# AI-PRD-Devin

Fork of [向阳乔木](https://x.com/vista8)'s [`qiaomu-ai-prd`](https://github.com/joeseesun/qiaomu-ai-prd), tuned by Devin for an agent workflow that ends in [`red-green-mode`](https://github.com/hidevinliu/red-green-mode) (an exit-code test-tampering guard, also open source).

> 你只有一句产品想法，但真正要交给 AI 编程助手时，它需要的是一份可执行 PRD。
> Turn one-line product ideas into AI-implementable PRDs.

[![License](https://img.shields.io/github/license/hidevinliu/AI-PRD-Devin?style=flat-square)](LICENSE)
[![Repo](https://img.shields.io/badge/GitHub-hidevinliu%2FAI--PRD--Devin-black?style=flat-square&logo=github)](https://github.com/hidevinliu/AI-PRD-Devin)

**[中文](#中文) | [English](#english)**

## 这个 fork 相比上游改了什么

- **任务分级**：新产品/大功能才写完整 11 章 PRD；单模块或 `[精简模式]` 只写目标、范围、核心行为、验收与未决项；小修补只给 3–5 行方案 —— 不用一份模板套所有需求体量。
- **核心机制强制落地**：P0 核心模块必须写清楚可实现的规则/算法/启发式，不许把核心功能架空成"准确率未知"。
- **单一事实源**：关键数字（阈值、超时、上限）只在 `AI 速读卡` 定一次，全文复用，杜绝跨章节互相打架。
- **lint 只查正文**：`scripts/lint_prd.py` 只在正文找占位符，放过 JSON / ASCII 图 / Markdown 链接里的合法内容，减少误报。
- **接力棒交接**（第 13 步）：当 PRD 要进 `red-green-mode` 实现时，额外产出 `acceptance-contract.json`，把「验收剧本」转成 TDD/red-green 两个下游 skill 都能消费的结构化契约——这是 `PRD → TDD → red-green` 三棒接力的第一棒交接物。

用法与上游一致（见下方安装与示例）；下方的 `npx skills add joeseesun/qiaomu-ai-prd` 装的是**上游原版**。要用这个 fork 的改动，直接把本仓库放进你的 agent skills 目录（例如 `~/.agents/skills/AI-PRD-Devin/`）即可，不需要额外构建。

---

<a name="中文"></a>

## 中文

`qiaomu-ai-prd` 把“我想做一个英语单词学习网站”“开发一个 iOS 提词器”“设计一个窦唯官网”这类一句话需求，整理成有速读卡、有布局、有模块、有数据模型、有技术架构、有优先级、有性能指标、有验收剧本的完整产品需求文档。

它的重点不是填模板，而是替你做产品判断，并把判断写成开发者和 AI 都能执行的形式。v0.2 增加了 `硬约束 / 推荐默认 / 发挥空间`，让 AI 知道哪里不能偏离，哪里可以大胆做得更好。

## 一行安装

```bash
npx skills add joeseesun/qiaomu-ai-prd
```

验证：

```bash
test -f ~/.agents/skills/qiaomu-ai-prd/SKILL.md
python3 ~/.agents/skills/qiaomu-ai-prd/scripts/lint_prd.py --help
```

## 你可以这样说

- “用 qiaomu-ai-prd 给我写一个英语单词学习网站的 PRD。”
- “我想开发一个 iOS 提词器，移动优先，生成 AI 可执行 PRD。”
- “为一个 GTA 风格网页游戏写 PRD，深度模式 + 前端视角。”
- “把这个产品想法整理成产品需求文档：一款面向独立开发者的 AI 记账工具。”

## 你会得到什么

1. 产品定位、竞品差异、三类用户画像和可行性边界。
2. 顶层布局、核心模块、真实状态、正常路径和失败路径。
3. 超越竞品的差异化功能，以及为什么竞品通常做不到。
4. 带 `//` 注释的数据模型、技术架构和依赖选择理由。
5. `超预期机会`、交互细节、输出系统、P0-P3 开发优先级和数字化性能指标。
6. 直接写给 AI 编程助手的开发者交接说明、可替换技术原则和验收剧本。

## 输出预览

```text
# WordPulse PRD

## AI 速读卡
产品一句话：一个自带复习节奏的个人词库学习网站。
核心循环：导入词库 -> 练习 -> 标记掌握度 -> 自动复习。
硬约束：P0 必须完成一次学习和复习闭环。
推荐默认：本地优先保存，不要求账号。
发挥空间：练习动效、分数反馈、复习完成页可以更有记忆点。
超预期机会：生成一张“今日掌握 18 个词”的分享卡。

## 第一章：产品概述
WordPulse 是一款 Web 英语单词学习工具，让自学者能够围绕自己的词库完成学习、练习和复习，而无需在固定课程和零散笔记之间来回切换。

## 第二章：整体布局与导航
+--------------------------------------------------+
| 顶部学习状态栏（100% x 64px）                    |
| 今日待复习：18 个词 | 连续学习：6 天 | 开始复习 |
+----------------------+---------------------------+
| 词库与筛选（28%）    | 练习工作区（72%）          |
| CET-6 核心词         | abandon                    |
| 错题本：12           | [认识] [模糊] [不认识]    |
+----------------------+---------------------------+

## 第十章：性能指标
| 指标名称 | 目标值 | 测量方法 | 劣化阈值 |
|---|---:|---|---:|
| 首屏可交互时间 | <= 1200ms | Lighthouse mobile 4G | > 2200ms |
| 答题反馈延迟 | <= 80ms | 点击选项到状态变化 | > 180ms |
```

## 可选模式

| 模式 | 作用 |
|---|---|
| `[深度模式]` | 每个模块增加边界情况分析 |
| `[精简模式]` | 短规格：目标、范围、核心行为、验收、必要未决项；不强制 11 章 |
| `[前端视角]` | 增加组件拆分和状态管理建议 |
| `[后端视角]` | 增加 API 和数据库设计 |
| `[移动优先]` | 图示和交互优先按移动端设计 |
| `[创意模式]` | 保留硬约束，扩展发挥空间和超预期机会 |
| `[竞品深挖]` | 深入分析竞品弱点和盲区 |
| `[商业化]` | 增加付费功能和变现路径 |
| `[开源友好]` | 技术选型优先考虑宽松许可证 |

## 前置条件

- [ ] 已安装 Node.js，并可运行 `node --version`。
- [ ] 当前 agent 支持本地 skills 目录，通常是 `~/.agents/skills`。
- [ ] 如果要发布或保存 PRD 文件，需要当前工作区可写。

## 质量门槛

- 每个主要模块都有真实内容的 ASCII 图。
- 必须包含 `AI 速读卡` 和 `超预期机会`；`硬约束 / 推荐默认 / 发挥空间` 可选，且硬约束只写用户明说的，禁止自行添加 UI 约束（颜色/token/字体/布局/壳层）。
- 每个模块覆盖默认态、激活态、空状态、错误态中的相关状态。
- 数据模型字段都有 `//` 注释，顶层对象包含 `"version"`。
- 性能指标必须是数字，不能只写“快”“流畅”。
- 第十一章必须写给实现者，并包含诚实的已知未知项和至少 3 条验收剧本。

## Troubleshooting

| 问题 | 原因 | 解决 |
|---|---|---|
| 输出像模板，缺少产品判断 | 输入太短且模型没有使用 skill | 明确说“使用 qiaomu-ai-prd”，或补一句核心用户和平台 |
| PRD 里出现占位符 | 输出前自检没有执行完整 | 运行 `scripts/lint_prd.py <file>` 并修复 |
| 技术选型包体积看起来不可信 | 当前环境没有验证包信息 | 写 `未知`，或联网核查官方包信息后更新 |
| P0 太大 | 按实现难度而不是用户行为排序 | 只保留能完成核心循环的最小集合 |
| PRD 把 AI 限制得太死 | 把低风险实现细节写成了硬约束 | 改成 `推荐默认` 或 `发挥空间` |

## 致谢

方法论来自向阳乔木对 AI 编程工作流、PRD 写作和 agent handoff 的实践整理。

---

<a name="english"></a>

## English

`qiaomu-ai-prd` turns a one-line product idea into a structured PRD that both human product builders and AI coding assistants can execute.

Install:

```bash
npx skills add joeseesun/qiaomu-ai-prd
```

Try prompts like:

- "Use qiaomu-ai-prd to write a PRD for an English vocabulary learning website."
- "Create an AI-implementable PRD for an iOS teleprompter, mobile-first."
- "Write a PRD for a GTA-style web game with deep mode and frontend perspective."

The skill produces:

- speed-read card, product positioning, personas, differentiation, and feasibility boundaries
- hard constraints, recommended defaults, and creative space
- ASCII layout and module diagrams with realistic content
- module states, failure paths, dependencies, and open decisions
- commented JSON data models
- architecture, replaceable technology principles, interaction details, export system, priorities, and metrics
- overdelivery opportunities and acceptance scripts
- a developer handoff written directly to the implementing AI assistant

## License

MIT

Copyright (c) 向阳乔木  
X: https://x.com/vista8  
GitHub: https://github.com/joeseesun/
