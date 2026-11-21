"""元素与类别类型测试。"""
from runeing.types import (
    ELEMENTS_ABSENT,
    ELEMENTS_MENTIONED_ONLY,
    ELEMENTS_WITH_INSTANCE,
    SIM_CATEGORIES,
    element_status,
    is_sim_category,
)


def test_six_elements_with_instance() -> None:
    assert ELEMENTS_WITH_INSTANCE == {"光", "冰", "火", "金", "风", "木"}


def test_two_mentioned_only() -> None:
    assert ELEMENTS_MENTIONED_ONLY == {"水", "土"}


def test_two_absent() -> None:
    assert ELEMENTS_ABSENT == {"雷", "暗"}


def test_element_status() -> None:
    assert element_status("光") == "有实例"
    assert element_status("水") == "仅提及"
    assert element_status("雷") == "未出现"
    assert element_status("unknown") == "unknown"


def test_element_groups_disjoint() -> None:
    assert not (ELEMENTS_WITH_INSTANCE & ELEMENTS_MENTIONED_ONLY)
    assert not (ELEMENTS_WITH_INSTANCE & ELEMENTS_ABSENT)
    assert not (ELEMENTS_MENTIONED_ONLY & ELEMENTS_ABSENT)


def test_sim_categories_are_three() -> None:
    assert SIM_CATEGORIES == {"攻击", "防御", "状态"}
    assert is_sim_category("攻击")
    # 真实层开放集里的类别，不应被当成模拟三分类
    assert not is_sim_category("增益")
