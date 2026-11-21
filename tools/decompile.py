#!/usr/bin/env python3
"""从 corpus/templates.jsonl 反生成 .rune 源码。

只生成已知结构；create 未知时输出跳过说明，不编造。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proto"))

from runeing.decompile import to_rune  # noqa: E402

TEMPLATES = ROOT / "corpus" / "templates.jsonl"


def main() -> int:
    ok = 0
    skipped = 0
    for line in TEMPLATES.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = cast(dict[str, Any], json.loads(line))
        create = cast(list[str] | None, row["create"])
        emit = cast(list[str], row["emit"])
        try:
            print(to_rune(cast(str, row["spell"]), cast(str, row["element"]),
                          tuple(create) if create else None, tuple(emit)))
            ok += 1
        except ValueError as exc:
            print(f"# 跳过：{exc}")
            skipped += 1
    print(f"# 生成 {ok} 个，跳过 {skipped} 个", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
