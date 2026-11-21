"""输入 → 预期输出示例。输出由 ``render()`` 生成，可被测试逐字断言。

运行：
    python3 examples/demo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

PROTO = Path(__file__).resolve().parents[1] / "proto"
if str(PROTO) not in sys.path:
    sys.path.insert(0, str(PROTO))

from runeing.core import capacity_status  # noqa: E402
from runeing.query import lookup  # noqa: E402
from runeing.template import Projectile  # noqa: E402
from runeing.types import element_status  # noqa: E402

TEMPLATES = Path(__file__).resolve().parents[1] / "corpus" / "templates.jsonl"


def describe(p: Projectile | None, name: str) -> list[str]:
    lines = [f'输入: "{name}"']
    if p is None:
        lines.append("输出: None（不在投射模板内）")
        return lines
    if p.create is None:
        create = "None [unknown]"
    else:
        create = f"{[r.name for r in p.create]} [推断]"
    lines += [
        "输出:",
        f"  元素: {p.element}",
        f"  声明魔文数: {p.declared_runes}",
        f"  create: {create}",
        f"  emit: {[r.name for r in p.emit]}",
        f"  已知魔文: {len(p.known_runes)}/{p.declared_runes}",
        f"  求值: {p.value()}",
        f"  容量({p.declared_runes}): {capacity_status(p.declared_runes)}",
    ]
    return lines


def render() -> str:
    parts: list[str] = []

    parts.append("=== 示例 1：完整实例 ===")
    parts += describe(lookup("光射线", TEMPLATES), "光射线")
    parts.append("")

    parts.append("=== 示例 2：残缺实例 ===")
    parts += describe(lookup("丢冰块", TEMPLATES), "丢冰块")
    parts.append("")

    parts.append("=== 示例 3：不认识的咒语 ===")
    parts += describe(lookup("火苗", TEMPLATES), "火苗")
    parts.append("")

    parts.append("=== 示例 4：容量 ===")
    for n in (10, 13, 15, 4):
        parts.append(f"输入: {n} → 输出: {capacity_status(n)}")
    parts.append("")

    parts.append("=== 示例 5：元素 ===")
    for e in ("光", "水", "雷"):
        parts.append(f'输入: "{e}" → 输出: {element_status(e)}')

    return "\n".join(parts)


def main() -> None:
    print(render())


if __name__ == "__main__":
    main()
