"""咒语目录：覆盖与深度分档。"""
from pathlib import Path

from runeing.catalog import build

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "corpus" / "corpus.jsonl"


def test_covers_all_spells() -> None:
    entries = build(CORPUS)
    names = {e.name for e in entries}
    assert len(entries) >= 25
    for expected in ("光射线", "闪光术", "丢冰块", "火苗", "冰旋刃"):
        assert expected in names


def test_light_ray_is_full() -> None:
    entry = next(e for e in build(CORPUS) if e.name == "光射线")
    assert entry.depth == "full"
    assert entry.rings == 1
    assert entry.rune_count == 4


def test_flash_is_partial() -> None:
    entry = next(e for e in build(CORPUS) if e.name == "闪光术")
    assert entry.rune_count == 2
    assert entry.depth in {"partial", "full"}


def test_name_only_not_upgraded() -> None:
    """没有魔文数就是没有，不能因为别的咒语有就补上。"""
    entry = next(e for e in build(CORPUS) if e.name == "火苗")
    assert entry.rune_count is None
    assert entry.depth in {"ring_only", "name_only"}


def test_depths_are_disjoint() -> None:
    entries = build(CORPUS)
    total = sum(1 for _ in entries)
    by_depth = sum(
        1
        for depth in ("full", "partial", "ring_only", "name_only")
        for e in entries
        if e.depth == depth
    )
    assert total == by_depth
