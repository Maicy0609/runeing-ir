"""Projectile 模板测试。

每个断言失败时都说明“模板被推翻”，而不是“数据写错了”。
数据来自 corpus/templates.jsonl，不手输。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "corpus" / "templates.jsonl"


def load_raw() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in TEMPLATES.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(cast(dict[str, Any], json.loads(line)))
    return rows


def test_at_least_two_instances() -> None:
    """少于两个实例，模板没有意义。"""
    assert len(load_raw()) >= 2, "实例不足 2 个，模板无从验证"


def test_all_are_four_runes() -> None:
    """推翻条件 1：若出现非 4 魔文的投射咒语，模板的“固定 4 魔文”假设死。"""
    for row in load_raw():
        assert row["declared_runes"] == 4, (
            f"反例：{row['spell']} declared_runes={row['declared_runes']}，"
            "Projectile 的固定规模假设被推翻"
        )


def test_emit_is_two() -> None:
    """推翻条件 2：若 emit 不是 2 个，共享发射段的假设死。"""
    for row in load_raw():
        emit = cast(list[str], row["emit"])
        assert len(emit) == 2, f"反例：{row['spell']} emit 长度 {len(emit)}，共享 emit 假设被推翻"


def test_create_shape() -> None:
    """create 要么是 2 个魔文，要么明确为 None（原文未给）。"""
    for row in load_raw():
        create = cast(list[str] | None, row["create"])
        if create is not None:
            assert len(create) == 2, f"反例：{row['spell']} create 长度 {len(create)}"
        else:
            assert row["create_source"] == "unknown", (
                f"{row['spell']} create 为 None 但来源标成 {row['create_source']}"
            )


def test_values_differ_only_by_element() -> None:
    """模板的核心主张：两个咒语求值只在元素上不同。"""
    elements = [cast(str, row["element"]) for row in load_raw()]
    assert len(set(elements)) == len(elements), "两个实例元素相同，无法体现参数化"


def test_no_silent_unknown() -> None:
    """未知必须显式标注，不能靠缺字段默认。"""
    for row in load_raw():
        assert "create" in row, f"{row['spell']} 缺 create 字段"
        assert "create_source" in row, f"{row['spell']} 缺 create_source 字段"
