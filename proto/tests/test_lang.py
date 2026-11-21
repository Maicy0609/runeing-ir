"""魔法源语言：解析、检查、IR、求值。"""
import pytest

from runeing.compile import check, evaluate, has_error, lower
from runeing.lang import ParseError, parse

GOOD = "光射线 : 光 = 发光 -> 点 -> 发射 -> 发射"
FLASH = "闪光术 : 光 = 发光 -> 点"
OVERSIZE = "巨型光球 : 光 = 发光 -> 点 -> 发射 -> 发射 -> 旋转 * 11"


def test_parse_good() -> None:
    src = parse(GOOD)
    assert src.name == "光射线"
    assert src.element == "光"
    assert src.runes == ("发光", "点", "发射", "发射")
    assert src.rune_count == 4


def test_parse_expand_repeat() -> None:
    src = parse("旋转阵 : 光 = 旋转 * 11")
    assert src.runes == ("旋转",) * 11
    assert src.rune_count == 11


def test_parse_ignores_comment_and_blank() -> None:
    src = parse("# 注释\n\n光射线 : 光 = 发光 -> 点 -> 发射 -> 发射\n")
    assert src.name == "光射线"


def test_parse_missing_parts() -> None:
    with pytest.raises(ParseError):
        parse("光射线 = 发光 -> 点")  # 缺 元素
    with pytest.raises(ParseError):
        parse("光射线 : 光 =")  # 缺序列
    with pytest.raises(ParseError):
        parse("")  # 空文件


def test_parse_two_spells_rejected() -> None:
    with pytest.raises(ParseError):
        parse("A : 光 = 发光\nB : 光 = 点")


def test_parse_empty_segment() -> None:
    with pytest.raises(ParseError):
        parse("光射线 : 光 = 发光 ->  -> 点")


def test_check_good_has_no_error() -> None:
    assert not has_error(check(parse(GOOD)))


def test_check_oversize_is_error() -> None:
    diags = check(parse(OVERSIZE))
    assert has_error(diags)
    assert any(d.code == "E_CAPACITY" for d in diags)


def test_check_unknown_element() -> None:
    diags = check(parse("雷击 : 雷 = 发光 -> 点 -> 发射 -> 发射"))
    assert any(d.code == "E_ELEMENT" for d in diags)


def test_check_unknown_capacity_is_warning_not_error() -> None:
    # 11 个魔文：未采样，只警告，不判错
    src = parse("十一 : 光 = 旋转 * 11")
    diags = check(src)
    assert not has_error(diags)
    assert any(d.code == "W_CAPACITY" for d in diags)


def test_lower_to_projectile() -> None:
    ir = lower(parse(GOOD))
    assert ir.form == "projectile"
    assert ir.apply is not None
    assert ir.apply.create == ("发光", "点")
    assert ir.apply.emit == ("发射", "发射")
    assert ir.work == 4


def test_lower_generic_when_shape_differs() -> None:
    ir = lower(parse("怪东西 : 光 = 发光 -> 点 -> 发光"))
    assert ir.form == "opaque"
    assert ir.apply is None
    assert ir.work == 3


def test_evaluate_consumes_structure() -> None:
    value = evaluate(lower(parse(GOOD)))
    assert value.element == "光"
    assert value.form == "projectile"
    assert value.work == 4
    assert value.pipeline == ("发光+点", "发射+发射")


def test_ray_and_flash_differ() -> None:
    """M1 验收：光射线与闪光术的求值必须不同，且差异来自有无 emit。"""
    ray = evaluate(lower(parse(GOOD)))
    flash = evaluate(lower(parse(FLASH)))

    assert ray.form != flash.form
    assert ray.work != flash.work
    assert ray.pipeline != flash.pipeline
    # 差异可追溯：投射有 emit 段，闪光术没有
    assert ray.pipeline and not flash.pipeline
    assert flash.form == "opaque"
