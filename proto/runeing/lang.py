"""魔法源语言：解析。

人类写的形态（`.rune` 文件）：

    咒语 光射线 {
      元素 光
      魔文 发光 点 发射 发射
    }

**源码里没有连笔。** 连笔是 (魔文对 × 魔女) 的私有表，由施法者补齐，
不进源码、不进 IR（第 17 章）。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_NAME = re.compile(r"咒语\s+(\S+)\s*\{")
_ELEMENT = re.compile(r"元素\s+(\S+)")
_RUNES = re.compile(r"魔文\s+(.+)")


@dataclass(frozen=True)
class SpellSource:
    """解析后的源语法树。只保留语义相关字段。"""

    name: str
    element: str
    runes: tuple[str, ...]

    @property
    def rune_count(self) -> int:
        return len(self.runes)


class ParseError(ValueError):
    """源码格式错误。"""


def parse(text: str) -> SpellSource:
    name: str | None = None
    element: str | None = None
    runes: tuple[str, ...] = ()

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if m := _NAME.search(line):
            name = m.group(1)
        elif m := _ELEMENT.search(line):
            element = m.group(1)
        elif m := _RUNES.search(line):
            runes = tuple(m.group(1).split())

    if name is None:
        raise ParseError("缺少 `咒语 <名字> {`")
    if element is None:
        raise ParseError("缺少 `元素 <元素名>`")
    if not runes:
        raise ParseError("缺少 `魔文 <魔文…>`")

    return SpellSource(name=name, element=element, runes=runes)
