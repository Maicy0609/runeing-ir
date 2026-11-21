"""语料库结构测试：全部从 corpus.jsonl 读取，不重复手输数据。"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "corpus" / "corpus.jsonl"

REQUIRED = {"id", "kind", "chapter", "speaker", "viewpoint", "layer", "quote", "fields"}
KINDS = {"spell", "rule", "rune", "meta"}
VIEWPOINTS = {"全知", "角色", "拟人修辞"}
LAYERS = {"真实", "模拟", "设定"}
STATUSES = {"原文", "推断", "无", "悬置"}


def load() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in CORPUS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def test_each_line_is_valid_json_object() -> None:
    assert load(), "语料库为空"


def test_required_fields_present() -> None:
    for row in load():
        missing = REQUIRED - set(row)
        assert not missing, f"{row.get('id')} 缺字段 {missing}"


def test_enums_are_valid() -> None:
    for row in load():
        assert row["kind"] in KINDS, row["id"]
        assert row["viewpoint"] in VIEWPOINTS, row["id"]
        assert row["layer"] in LAYERS, row["id"]


def test_ids_unique() -> None:
    ids = [row["id"] for row in load()]
    assert len(ids) == len(set(ids)), "id 重复"


def test_quote_length() -> None:
    for row in load():
        q = row["quote"]
        assert q, f"{row['id']} 引文为空"
        # 允许用省略号截断，但被截断的引文本体不超过 40 字
        body = q.replace("……", "")
        assert len(body) <= 40, f"{row['id']} 引文过长: {len(body)}"


def test_status_values_and_basis() -> None:
    for row in load():
        for field, spec in row["fields"].items():
            assert spec["status"] in STATUSES, f"{row['id']}.{field}"
            if spec["status"] == "推断":
                assert spec.get("basis"), f"{row['id']}.{field} 标推断但无 basis"
