"""从模板数据反生成源码。

原则：**不知道就不生成**。``create`` 为 ``None`` 时直接拒绝，
不编造魔文名。
"""
from __future__ import annotations


def to_rune(
    spell: str,
    element: str,
    create: tuple[str, ...] | None,
    emit: tuple[str, ...],
) -> str:
    """生成一行 ``.rune`` 源码。

    若 ``create`` 未知，抛 ``ValueError``，不返回半成品。
    """
    if create is None:
        raise ValueError(f"{spell} 的 create 未知，拒绝生成源码")
    if not create or not emit:
        raise ValueError(f"{spell} 的段为空，拒绝生成源码")
    body = " -> ".join([*create, *emit])
    return f"{spell} : {element} = {body}"
