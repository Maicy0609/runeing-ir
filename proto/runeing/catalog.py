"""咒语目录：这门语言认识哪些咒语，认识多深。

只从 ``corpus/corpus.jsonl`` 聚合，不新增数据。四个深度：

- ``full``     有魔文数 + 结构
- ``partial``  有魔文数，无结构
- ``ring_only`` 有环数，无魔文数
- ``name_only`` 只有名字与元素
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast


@dataclass(frozen=True)
class Entry:
    name: str
    layer: str
    element: str | None
    rings: int | None
    rune_count: int | None
    structure: bool

    @property
    def depth(self) -> str:
        if self.structure and self.rune_count is not None:
            return "full"
        if self.rune_count is not None:
            return "partial"
        if self.rings is not None:
            return "ring_only"
        return "name_only"


def _value(fields: dict[str, Any], key: str) -> Any:
    spec = fields.get(key)
    if isinstance(spec, dict) and spec.get("status") == "原文":
        return spec.get("value")
    return None


def build(path: Path) -> list[Entry]:
    acc: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = cast(dict[str, Any], json.loads(line))
        if row["kind"] != "spell":
            continue
        name = row["id"].split(":")[1]
        slot = acc.setdefault(name, {"layer": row["layer"]})
        fields = cast(dict[str, Any], row["fields"])
        for key, attr in (
            ("元素", "element"),
            ("环数", "rings"),
            ("魔文数", "rune_count"),
            ("结构", "structure"),
        ):
            val = _value(fields, key)
            if val is not None:
                slot[attr] = val

    out: list[Entry] = []
    for name, slot in sorted(acc.items()):
        out.append(
            Entry(
                name=name,
                layer=cast(str, slot["layer"]),
                element=cast(str | None, slot.get("element")),
                rings=cast(int | None, slot.get("rings")),
                rune_count=cast(int | None, slot.get("rune_count")),
                structure=bool(slot.get("structure")),
            )
        )
    return out
