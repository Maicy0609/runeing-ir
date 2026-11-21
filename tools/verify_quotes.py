#!/usr/bin/env python3
"""校验 corpus.jsonl 中每条引文是否真能在指定章节里逐字找到。

规则：
- 引文按 ``……`` 分段，每段都必须在该章正文中按顺序出现；
- 任何一条不通过即非零退出；
- 原文路径通过 ``--source`` 指定，默认 ``/upload`` 下的小说 txt。

用法：
    python3 tools/verify_quotes.py --source /upload/83f2....txt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus" / "corpus.jsonl"

CHAPTER_RE = re.compile(r"^第(\d+)章", re.MULTILINE)


def split_chapters(text: str) -> dict[int, str]:
    marks = [(int(m.group(1)), m.start()) for m in CHAPTER_RE.finditer(text)]
    out: dict[int, str] = {}
    for i, (num, pos) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        out[num] = text[pos:end]
    return out


def chapter_number(label: str) -> int:
    m = re.match(r"第(\d+)章", label)
    if not m:
        raise ValueError(f"章节标签无法解析: {label}")
    return int(m.group(1))


def quote_ok(quote: str, body: str) -> bool:
    parts = [p for p in quote.split("……") if p]
    pos = 0
    for part in parts:
        idx = body.find(part, pos)
        if idx < 0:
            return False
        pos = idx + len(part)
    return bool(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="小说原文 txt 路径")
    ap.add_argument("--corpus", default=str(CORPUS))
    args = ap.parse_args()

    text = Path(args.source).read_text(encoding="utf-8")
    chapters = split_chapters(text)

    rows = [
        json.loads(line)
        for line in Path(args.corpus).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    failures: list[str] = []
    for row in rows:
        num = chapter_number(row["chapter"])
        body = chapters.get(num)
        if body is None:
            failures.append(f"{row['id']}: 找不到第 {num} 章")
            continue
        if not quote_ok(row["quote"], body):
            failures.append(f"{row['id']}: 引文未命中 → {row['quote']}")

    total = len(rows)
    if failures:
        print(f"FAIL {len(failures)}/{total}")
        for f in failures:
            print("  " + f)
        return 1

    print(f"PASS {total}/{total} 条引文均在对应章节逐字命中")
    return 0


if __name__ == "__main__":
    sys.exit(main())
