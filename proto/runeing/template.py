"""投射类模板 Projectile<E>。

依据（第 22 章，叙述 + 墨砚秋）：

- 冰系的丢冰块要四个魔文，效果是把一块拳头大小的冰块当石头丢出去
- 之前提到的丢XX里都有它的身影（指发射魔文）
- 其实就是基础元素魔法加上发射魔文，把前者发射出去

结构假设（**可证伪**）：

    Projectile<E> = create_E(2) + emit(2)

- ``create_E``：元素特异；丢冰块的具体魔文原文未给，记为 ``None``
- ``emit``：跨元素共享的两个魔文

推翻条件见 ``tests/test_projectile.py``。
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import Rune, Source


@dataclass(frozen=True)
class Value:
    """求值结果。

    ``work`` 是结构工作量，目前唯一有文本依据的度量是魔文个数。
    ``pipeline`` 记录求值经过的段，用于区分「有 emit」与「无 emit」。
    """

    element: str
    form: str
    work: int = 0
    pipeline: tuple[str, ...] = ()


@dataclass(frozen=True)
class Projectile:
    """投射类咒语。

    ``declared_runes`` 是原文直接给出的魔文总数；``create`` 为 ``None``
    表示原文未给该元素的实体魔文。
    """

    name: str
    element: str
    declared_runes: int
    create: tuple[Rune, ...] | None
    emit: tuple[Rune, ...]
    create_source: Source

    @property
    def complete(self) -> bool:
        """原文是否给全了 4 个魔文。"""
        return self.create is not None

    @property
    def known_runes(self) -> tuple[Rune, ...]:
        """当前已知的魔文序列（create 未知时只含 emit）。"""
        return (self.create or ()) + self.emit

    def value(self) -> Value:
        """求值：保留元素、形态、工作量与段落路径。"""
        if self.create is None:
            return Value(element=self.element, form="projectile", work=self.declared_runes)
        create = "+".join(r.name for r in self.create)
        emit = "+".join(r.name for r in self.emit)
        return Value(
            element=self.element,
            form="projectile",
            work=self.declared_runes,
            pipeline=(create, emit),
        )
