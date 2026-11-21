"""按名字查模板实例。

路径由调用方传入，库本身不硬编码数据文件位置。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from .core import Rune
from .template import Projectile


def load_all(path: Path) -> list[Projectile]:
    out: list[Projectile] = []
    for line in path.read_text(encoding="utf-8").splitlines():
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


def lookup(name: str, path: Path) -> Projectile | None:
    """按咒语名查。不在模板数据里的返回 ``None``。"""
    for item in load_all(path):
        if item.name == name:
            return item
    return None
