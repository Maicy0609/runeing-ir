"""runeing 核心：魔文、环、连笔边、咒语。

命名约定（全项目统一，不混用同义词）：
  rune  魔文
  ring  环
  edge  连笔（环上相邻魔文之间的连接）

只建模语料能支持的部分。引文未支持的字段一律标 ``unknown``，不内插。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Source = Literal["原文", "推断", "unknown"]
Topology = Literal["cycle", "chain"]


@dataclass(frozen=True)
class Rune:
    """一个魔文。

    name_source 标注 ``name`` 这个字符串本身是否有原文支持：

    - ``原文``    原文直接出现该名称
    - ``推断``    名称由本项目拆分或命名
    - ``unknown`` 无依据
    """

    name: str
    role: str = "unknown"
    name_source: Source = "unknown"


@dataclass(frozen=True)
class Ring:
    """一个有向环。

    topology:

    - ``cycle`` 闭合环，最后一个魔文连回第一个（第 12 章“魔文都排列在一个环中”）
    - ``chain`` 线性链，不闭合

    环无全局起点，因此 ``canonical()`` 在循环旋转下取规范形。
    """

    runes: tuple[Rune, ...]
    topology: Topology = "cycle"

    def edges(self) -> tuple[tuple[int, int], ...]:
        """连笔边：src -> dst 的索引对。"""
        n = len(self.runes)
        if n == 0:
            return ()
        if self.topology == "cycle":
            return tuple((i, (i + 1) % n) for i in range(n))
        return tuple((i, i + 1) for i in range(n - 1))

    def canonical(self) -> tuple[str, ...]:
        """循环旋转下的规范形：取字典序最小的旋转。``chain`` 直接返回原序。"""
        names = tuple(r.name for r in self.runes)
        if self.topology != "cycle" or len(names) <= 1:
            return names
        n = len(names)
        return min(names[i:] + names[:i] for i in range(n))

    def roles(self) -> dict[str, int]:
        """按 role 计数，用于在不依赖位置的前提下检验组合关系。"""
        out: dict[str, int] = {}
        for r in self.runes:
            out[r.role] = out.get(r.role, 0) + 1
        return out


@dataclass(frozen=True)
class Spell:
    """一个咒语，包含一个或多个环。"""

    name: str
    rings: tuple[Ring, ...]
    element: str | None = None

    @property
    def rune_count(self) -> int:
        return sum(len(r.runes) for r in self.rings)

    def capacity(self) -> str:
        return capacity_status(self.rune_count)


# 容量已知点（不内插）
CAP_TYPICAL = 10
CAP_ONE_SECOND = 13
CAP_FAIL = 15


def capacity_status(n: int) -> str:
    """容量三值函数。

    只在语料给出实数的点上返回值，其余返回 ``unknown``：

    - 10 —— 第 44 章“我平时也就容纳十个魔文”（叙述·拟人修辞）
    - 13 —— 第 44 章“稳定上限十三个”；第 58 章实测“只维持了一秒”
    - 15 —— 第 44 章“十五个魔文根本稳定不住”
    """
    if n == CAP_TYPICAL:
        return "常态"
    if n == CAP_ONE_SECOND:
        return "一秒后崩溃"
    if n == CAP_FAIL:
        return "失败"
    return "unknown"
