"""容量三值函数测试：只认已知点，不内插。"""
from runeing.core import capacity_status


def test_known_points() -> None:
    assert capacity_status(10) == "常态"
    assert capacity_status(13) == "一秒后崩溃"
    assert capacity_status(15) == "失败"


def test_unknown_points_are_not_interpolated() -> None:
    # 11、12 不得被内插成“边缘”之类
    assert capacity_status(11) == "unknown"
    assert capacity_status(12) == "unknown"
    assert capacity_status(14) == "unknown"


def test_out_of_range_is_unknown() -> None:
    for n in (0, 1, 4, 9, 16, 100):
        assert capacity_status(n) == "unknown"
