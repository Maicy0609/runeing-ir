"""魔法源语言的编译管线：检查 → IR → 求值。

检查项全部来自语料：

- 容量：10 常态 / 13 一秒后崩溃 / 15 失败，其余未采样
- 元素：有实例 / 仅提及 / 未出现
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import CAP_TYPICAL, capacity_status
from .lang import SpellSource
from .template import Value
from .types import element_status


@dataclass(frozen=True)
class Diagnostic:
    level: str  # "错误" | "警告"
    code: str
    message: str


@dataclass(frozen=True)
class IR:
    """中间表示：只保留结构决定的量。"""

    kind: str  # "projectile" | "generic"
    element: str
    create: tuple[str, ...]
    emit: tuple[str, ...]


def check(src: SpellSource) -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    n = src.rune_count

    # 容量是上界：n ≤ 10 必然落在“常态”内（单调性，不是内插）。
    # 11/12/14 无采样，仍返回 unknown，不猜。
    if n <= CAP_TYPICAL:
        diags.append(Diagnostic("信息", "C_OK", f"容量 {n}/{CAP_TYPICAL}：常态"))
    else:
        cap = capacity_status(n)
        if cap == "失败":
            diags.append(Diagnostic("错误", "E_CAPACITY", f"容量 {n}：十五个魔文根本稳定不住"))
        elif cap == "一秒后崩溃":
            diags.append(Diagnostic("警告", "W_CAPACITY", f"容量 {n}：可成型，但约一秒后崩溃"))
        else:
            diags.append(Diagnostic("警告", "W_CAPACITY", f"容量 {n}：未采样点，不内插，无法判定"))

    es = element_status(src.element)
    if es == "未出现":
        diags.append(Diagnostic("错误", "E_ELEMENT", f"元素 {src.element}：原文未出现"))
    elif es == "仅提及":
        diags.append(Diagnostic("警告", "W_ELEMENT", f"元素 {src.element}：仅一句“同理”提及"))
    else:
        diags.append(Diagnostic("信息", "C_ELEMENT", f"元素 {src.element}：有实例"))

    return diags


def has_error(diags: list[Diagnostic]) -> bool:
    return any(d.level == "错误" for d in diags)


def lower(src: SpellSource) -> IR:
    """降级到 IR。4 魔文且后两段为发射时，识别为投射模板。"""
    if src.rune_count == 4 and src.runes[2:] == ("发射", "发射"):
        return IR(kind="projectile", element=src.element, create=src.runes[:2], emit=src.runes[2:])
    return IR(kind="generic", element=src.element, create=src.runes, emit=())


def evaluate(ir: IR) -> Value:
    return Value(element=ir.element, form=ir.kind)
