"""往返：模板数据 → 源码 → 编译 → IR，结构必须一致。"""
import json
from pathlib import Path
from typing import Any, cast

import pytest

from runeing.compile import lower
from runeing.decompile import to_rune
from runeing.lang import parse

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "corpus" / "templates.jsonl"


def _rows() -> list[dict[str, Any]]:
    return [
        cast(dict[str, Any], json.loads(line))
        for line in TEMPLATES.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_complete_entry_roundtrips() -> None:
    for row in _rows():
        create = cast(list[str] | None, row["create"])
        if create is None:
            continue
        emit = cast(list[str], row["emit"])
        src = to_rune(cast(str, row["spell"]), cast(str, row["element"]),
                      tuple(create), tuple(emit))
        ir = lower(parse(src))
        assert ir.form == "projectile"
        assert ir.apply is not None
        assert ir.apply.create == tuple(create)
        assert ir.apply.emit == tuple(emit)
        assert ir.element == row["element"]
        assert ir.work == row["declared_runes"]


def test_unknown_create_is_refused() -> None:
    """create 未知时反编译器必须拒绝，不能编造魔文名。"""
    with pytest.raises(ValueError):
        to_rune("丢冰块", "冰", None, ("发射", "发射"))


def test_all_rows_accounted_for() -> None:
    """每一行要么可往返，要么显式拒绝，不能静默跳过。"""
    rows = _rows()
    assert rows
    generated = 0
    refused = 0
    for row in rows:
        create = cast(list[str] | None, row["create"])
        emit = cast(list[str], row["emit"])
        if create is None:
            with pytest.raises(ValueError):
                to_rune(cast(str, row["spell"]), cast(str, row["element"]), None, tuple(emit))
            refused += 1
        else:
            to_rune(cast(str, row["spell"]), cast(str, row["element"]), tuple(create), tuple(emit))
            generated += 1
    assert generated + refused == len(rows)
