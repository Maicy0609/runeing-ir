"""验证 Projectile<E>：两个咒语撞在同一个骨架上。

数据来自 corpus/templates.jsonl，不手输。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from runeing.core import Rune
from runeing.template import Projectile

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "corpus" / "templates.jsonl"


def load() -> list[Projectile]:
    out: list[Projectile] = []
    for line in TEMPLATES.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = cast(dict[str, Any], json.loads(line))
        create_names = cast(list[str] | None, row["create"])
        create = (
            tuple(Rune(n, role="create", name_source="推断") for n in create_names)
            if create_names
            else None
        )
        emit = tuple(Rune(n, role="emit", name_source="推断") for n in cast(list[str], row["emit"]))
        out.append(
            Projectile(
                name=cast(str, row["spell"]),
                element=cast(str, row["element"]),
                declared_runes=cast(int, row["declared_runes"]),
                create=create,
                emit=emit,
                create_source=cast(Any, row["create_source"]),
            )
        )
    return out


def main() -> int:
    items = load()
    values = [p.value() for p in items]
    elements = [v.element for v in values]

    checks: list[tuple[str, bool]] = [
        ("实例数 >= 2", len(items) >= 2),
        ("declared_runes 全为 4", all(p.declared_runes == 4 for p in items)),
        ("emit 全为 2 个魔文", all(len(p.emit) == 2 for p in items)),
        ("create 要么 None 要么 2 个", all(p.create is None or len(p.create) == 2 for p in items)),
        ("求值形态全为 projectile", {v.form for v in values} == {"projectile"}),
        ("求值元素互不相同", len(set(elements)) == len(elements)),
        (
            "create 已知的实例长度正确",
            all(len(p.create) == 2 for p in items if p.create is not None),
        ),
    ]

    ok = True
    for desc, passed in checks:
        if not passed:
            ok = False
        print(f"[{'PASS' if passed else 'FAIL'}] {desc}")

    print()
    for p in items:
        state = "完整" if p.complete else "create 未知"
        print(f"{p.name}({p.element}): declared={p.declared_runes}")
        print(f"  已知魔文数={len(p.known_runes)} 状态={state}")
        print(f"  value = {p.value()}")
        print(f"  create_source = {p.create_source}")

    print()
    print("模板: Projectile<E> = create_E(2) + emit(2)")
    print("推翻条件见 proto/tests/test_projectile.py")

    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
