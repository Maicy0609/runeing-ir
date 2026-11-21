#!/usr/bin/env python3
"""输出咒语目录：认识哪些咒语，认识多深。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proto"))

from runeing.catalog import build  # noqa: E402

CORPUS = ROOT / "corpus" / "corpus.jsonl"
ORDER = ("full", "partial", "ring_only", "name_only")
LABEL = {
    "full": "完整结构",
    "partial": "有魔文数，无结构",
    "ring_only": "仅环数",
    "name_only": "仅名字",
}


def main() -> int:
    entries = build(CORPUS)
    print(f"共 {len(entries)} 个咒语\n")
    for depth in ORDER:
        items = [e for e in entries if e.depth == depth]
        print(f"[{depth}] {LABEL[depth]} —— {len(items)} 个")
        for e in items:
            layer = "模拟" if e.layer == "模拟" else "真实"
            element = e.element or "—"
            rings = e.rings if e.rings is not None else "—"
            runes = e.rune_count if e.rune_count is not None else "—"
            print(f"  {e.name:<8} {layer}  {element:<4} 环={rings} 魔文={runes}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
