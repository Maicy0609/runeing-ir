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
    level: str  # "错误" | "警告" | "信息"
    code: str
    message: str


@dataclass(frozen=True)
class Apply:
    """``emit`` 作用于 ``create`` 的结果。

    这是 IR 里唯一的结构关系，替代此前并列的 ``create`` / ``emit`` 字段。
    """

    emit: tuple[str, ...]
    create: tuple[str, ...]


@dataclass(frozen=True)
class IR:
    """中间表示：只保留结构决定的量。"""

    element: str
    runes: tuple[str, ...]
    apply: Apply | None

    @property
    def work(self) -> int:
        """结构工作量：目前唯一有依据的度量是魔文个数。"""
        return len(self.runes)

    @property
    def form(self) -> str:
        return "projectile" if self.apply is not None else "opaque"


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
        return IR(
            element=src.element,
            runes=src.runes,
            apply=Apply(emit=src.runes[2:], create=src.runes[:2]),
        )
    return IR(element=src.element, runes=src.runes, apply=None)


def evaluate(ir: IR) -> Value:
    """求值：消费 ``apply`` 的结构，而不只是读 ``form``。

    ``pipeline`` 让「有 emit」与「无 emit」在结果里可区分：
    投射咒语返回 `(create, emit)` 两段，其余返回空。
    """
    if ir.apply is None:
        return Value(element=ir.element, form="opaque", work=ir.work)
    create = "+".join(ir.apply.create)
    emit = "+".join(ir.apply.emit)
    return Value(
        element=ir.element,
        form="projectile",
        work=ir.work,
        pipeline=(create, emit),
    )
