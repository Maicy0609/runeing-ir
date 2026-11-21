"""元素与类别的类型层。

元素（第 22、37、102、110、204、243 章）：

- 有魔法实例：光、冰、火、金、风、木 —— 6 个
- 仅一句“土系水系木系的丢XX同理”：水、土 —— 2 个
- 词表内零命中：雷、暗

类别：

- 真实层为**开放集**，不枚举（第 37 章的三类只在“魔法对战中”成立）
- 模拟层三分类：攻击、防御、状态
"""
from __future__ import annotations

from typing import Literal

Element = Literal["光", "冰", "火", "金", "风", "木", "水", "土", "unknown"]

ELEMENTS_WITH_INSTANCE: frozenset[str] = frozenset({"光", "冰", "火", "金", "风", "木"})
ELEMENTS_MENTIONED_ONLY: frozenset[str] = frozenset({"水", "土"})
ELEMENTS_ABSENT: frozenset[str] = frozenset({"雷", "暗"})

SIM_CATEGORIES: frozenset[str] = frozenset({"攻击", "防御", "状态"})


def element_status(e: str) -> str:
    """返回元素的证据等级。"""
    if e in ELEMENTS_WITH_INSTANCE:
        return "有实例"
    if e in ELEMENTS_MENTIONED_ONLY:
        return "仅提及"
    if e in ELEMENTS_ABSENT:
        return "未出现"
    if e == "unknown":
        return "unknown"
    return "未收录"


def is_sim_category(c: str) -> bool:
    """模拟层的三分类是否包含该类别。真实层类别不在此列。"""
    return c in SIM_CATEGORIES
