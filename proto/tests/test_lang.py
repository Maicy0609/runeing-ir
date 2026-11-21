"""魔法源语言：解析、检查、IR、求值。"""
import pytest

from runeing.compile import check, evaluate, has_error, lower
from runeing.lang import ParseError, parse

GOOD = """
咒语 光射线 {
  元素 光
  魔文 发光 点 发射 发射
}
"""

OVERSIZE = """
咒语 巨型光球 {
  元素 光
  魔文 发光 点 发射 发射 旋转 旋转 旋转 旋转 旋转 旋转 旋转 旋转 旋转 旋转 旋转
}
"""


def test_parse_good() -> None:
    src = parse(GOOD)
    assert src.name == "光射线"
    assert src.element == "光"
    assert src.runes == ("发光", "点", "发射", "发射")
    assert src.rune_count == 4


def test_parse_missing_fields() -> None:
    with pytest.raises(ParseError):
        parse("""
咒语 空 {
  元素 光
}
""")  # 缺魔文
    with pytest.raises(ParseError):
        parse("""
咒语 空 {
  魔文 发光
}
""")  # 缺元素


def test_check_good_has_no_error() -> None:
    assert not has_error(check(parse(GOOD)))


def test_check_oversize_is_error() -> None:
    diags = check(parse(OVERSIZE))
    assert has_error(diags)
    assert any(d.code == "E_CAPACITY" for d in diags)


def test_check_unknown_element() -> None:
    src = parse("""
咒语 雷击 {
  元素 雷
  魔文 发光 点 发射 发射
}
""")
    diags = check(src)
    assert any(d.code == "E_ELEMENT" for d in diags)


def test_lower_to_projectile() -> None:
    ir = lower(parse(GOOD))
    assert ir.kind == "projectile"
    assert ir.create == ("发光", "点")
    assert ir.emit == ("发射", "发射")


def test_lower_generic_when_shape_differs() -> None:
    src = parse("""
咒语 怪东西 {
  元素 光
  魔文 发光 点 发光
}
""")
    assert lower(src).kind == "generic"


def test_evaluate() -> None:
    value = evaluate(lower(parse(GOOD)))
    assert value.element == "光"
    assert value.form == "projectile"
