#!/usr/bin/env python3
"""Lightweight validation for qiaomu-ai-prd outputs."""

from __future__ import annotations

import re
import sys
from pathlib import Path


CHAPTERS = [
    "第一章：产品概述",
    "第二章：整体布局与导航",
    "第三章：核心模块详细设计",
    "第四章：超越竞品的差异化功能",
    "第五章：数据模型",
    "第六章：技术架构",
    "第七章：交互细节",
    "第八章：导出与输出系统",
    "第九章：开发优先级",
    "第十章：性能指标",
    "第十一章：开发者交接说明",
]

# 占位符检测只跑在“剥掉代码块后的正文”上（见 strip_code_blocks）。
# 原因：JSON 数组 `[ ... ]`、ASCII 界面按钮 `[分拣]` 都活在代码块里，
# 它们是合法内容而不是未填模板。把它们当占位符是假阳性，
# 还和第五章“数据模型必须用 JSON”自相矛盾。
#
# 关键设计（v2）：方括号检测**不再抓任意 `[...]`**——那会误伤表格/正文里的
# 真实 UI 标签（如 `[复制]`、`[分拣]`）。真正的失败模式是“模型把本 skill 的
# 模板占位 token 原样留下没填”。所以只抓**模板占位词**：既覆盖 skill 自己
# 定位句模板（产品名/品类/目标用户/核心动作/被消除的关键摩擦），也覆盖
# 通用占位词（占位/待填/xxx/placeholder 等）。UI 标签 `[复制]` 不在词表内，放过。
PLACEHOLDER_BRACKET = (
    r"\[[^\]]*(?:产品名|品类|目标用户|核心动作|被消除的关键摩擦|"
    r"占位|待填|待定|某某|xxx|XXX|placeholder|图标名|按钮名|在此填入)[^\]]*\]"
)
PLACEHOLDER_PATTERNS = [
    PLACEHOLDER_BRACKET,    # 只抓“模板占位词”方括号，放过真实 UI 标签
    r"\bTODO\b",            # 大小写敏感：只抓占位用的大写 TODO，放过枚举值 todo
    r"\bTBD\b",
    r"待补充",
    r"在此填入",
    r"按钮\s*[A-ZＡ-Ｚ]",
    r"区域\s*[A-ZＡ-Ｚ]",
    r"功能\s*[A-ZＡ-Ｚ]",
    r"此处为",
]

VAGUE_PERFORMANCE_PATTERNS = [
    r"快速",
    r"很快",
    r"尽快",
    r"流畅",
    r"轻量",
    r"可扩展",
    r"高性能",
]

REQUIRED_MARKERS = [
    ("ai speed-read card", "AI 速读卡"),
    ("differentiation table", "差异化对比表"),
    ("three personas", "三类用户画像"),
    ("feasibility boundary", "可行性边界"),
    ("overdelivery opportunities", "超预期机会"),
    ("state list", "状态清单"),
    ("dependencies", "依赖关系"),
    ("core mechanism", "核心机制"),
    ("open questions", "待决问题"),
    ("data version", '"version"'),
    ("technical dependency table", "为何优于替代方案"),
    ("replaceable technology principle", "可替换技术原则"),
    ("keyboard shortcuts", "键盘快捷键"),
    ("context menu", "右键菜单"),
    ("export formats", "支持的输出格式"),
    ("implementation order", "实现顺序建议"),
    ("known unknowns", "已知的未知项"),
    ("acceptance scripts", "验收剧本"),
]


def chapter_positions(text: str) -> list[tuple[str, int]]:
    positions: list[tuple[str, int]] = []
    for chapter in CHAPTERS:
        match = re.search(rf"^#+\s*{re.escape(chapter)}", text, flags=re.MULTILINE)
        if match:
            positions.append((chapter, match.start()))
    return positions


def section(text: str, start_marker: str, end_marker: str | None = None) -> str:
    start = text.find(start_marker)
    if start == -1:
        return ""
    if end_marker is None:
        return text[start:]
    end = text.find(end_marker, start + len(start_marker))
    if end == -1:
        return text[start:]
    return text[start:end]


def strip_code_blocks(text: str) -> str:
    """移除围栏代码块（``` ... ```）和行内代码（`...`）。

    占位符检查应只针对正文散文：JSON、ASCII 图、命令示例里的方括号/关键字
    都是合法内容，不该被当成未填模板。用等长空行替换被删内容，保持行号语义。
    """
    # 去掉围栏代码块
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)
    # 去掉行内代码 `...`
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def count_table_rows(text: str) -> int:
    rows = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and "---" not in stripped:
            rows += 1
    return rows


def lint_text(text: str, source: str) -> list[str]:
    errors: list[str] = []

    positions = chapter_positions(text)
    found = {chapter for chapter, _ in positions}
    for chapter in CHAPTERS:
        if chapter not in found:
            errors.append(f"{source}: missing chapter `{chapter}`")

    if "AI 速读卡" in text and "第一章：产品概述" in text:
        if text.find("AI 速读卡") > text.find("第一章：产品概述"):
            errors.append(f"{source}: `AI 速读卡` should appear before chapter one")

    if len(positions) == len(CHAPTERS):
        ordered = [pos for _, pos in positions]
        if ordered != sorted(ordered):
            errors.append(f"{source}: chapters are not in required order")

    for label, marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f"{source}: missing required marker `{marker}` ({label})")

    prose = strip_code_blocks(text)
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, prose):  # 大小写敏感，且只查正文（不含代码块）
            errors.append(f"{source}: unresolved placeholder matched `{pattern}`")

    if "+--" not in text and "-->" not in text:
        errors.append(f"{source}: expected at least one ASCII flow or hierarchy diagram")

    if "+-" not in text and "+---" not in text:
        errors.append(f"{source}: expected at least one ASCII box/tree diagram")

    if "//" not in text:
        errors.append(f"{source}: data model should use inline `//` comments")

    priority = section(text, "第九章：开发优先级", "第十章：性能指标")
    for tier in ["P0", "P1", "P2", "P3"]:
        # v2：只要每档至少出现一次即可。正文里复述 `P0/P1` 是正常解释，
        # 旧规则要求“恰好一次”会逼模型把解释句里的档位改写成“第一档”，是过严。
        if len(re.findall(rf"\b{tier}\b", priority)) < 1:
            errors.append(f"{source}: priority chapter is missing tier `{tier}`")

    metrics = section(text, "第十章：性能指标", "第十一章：开发者交接说明")
    for pattern in VAGUE_PERFORMANCE_PATTERNS:
        if metrics and re.search(pattern, metrics):
            errors.append(f"{source}: vague performance wording in performance chapter matched `{pattern}`")
    if metrics and count_table_rows(metrics) < 2:
        errors.append(f"{source}: performance metrics table looks too thin")
    if metrics and not re.search(r"\d", metrics):
        errors.append(f"{source}: performance metrics should include numeric targets")

    handoff = section(text, "第十一章：开发者交接说明")
    if handoff and not re.search(r"(此处未解决|未知|待确认|未验证|不清楚)", handoff):
        errors.append(f"{source}: chapter 11 should contain at least one honest known unknown")
    if handoff and len(re.findall(r"验收剧本\s*\d+", handoff)) < 3:
        errors.append(f"{source}: chapter 11 should include at least three numbered acceptance scripts")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] in {"-h", "--help"}:
        print("Usage: lint_prd.py <file> [<file> ...]")
        return 0

    if len(argv) < 2:
        print("Usage: lint_prd.py <file> [<file> ...]", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            all_errors.append(f"{path}: cannot read file: {exc}")
            continue
        all_errors.extend(lint_text(text, str(path)))

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1

    print("PRD lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
