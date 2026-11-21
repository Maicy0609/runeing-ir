"""魔法源语言：解析。

写法（一行定义一个咒语）：

    光射线 : 光 = 发光 -> 点 -> 发射 -> 发射

规则：

- ``名字 : 元素 = 魔文序列``
- 魔文之间用 ``->`` 连接，方向即连笔方向（末尾 -> 开头，第 16 章）
- ``魔文 * 3`` 表示该魔文重复 3 次
- ``#`` 之后是注释
- 一个文件只放一个咒语

**语法符号一律 ASCII。** 标识符用中文，因为它们是原文术语（魔文名、元素名）。
**源码里没有连笔的具体形状。** 连笔是 (魔文对 × 魔女) 的私有表，
由施法者补齐，不进源码、不进 IR（第 17 章）。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_DEF = re.compile(r"^([^\s:#=]+)\s*:\s*([^\s=#]+)\s*=\s*(.+)$")
_TIMES = re.compile(r"^(.+?)\s*[xX*]\s*(\d+)$")

ARROW = "->"
REPEAT = "*"


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
    """源码格式错误，带行号。"""

    def __init__(self, message: str, line: int = 0, col: int = 1) -> None:
        self.message = message
        self.line = line
        self.col = col
        where = f"第 {line} 行" if line else ""
        super().__init__(f"{where}：{message}" if where else message)


def _expand(part: str) -> list[str]:
    m = _TIMES.match(part)
    if not m:
        return [part]
    rune, times = m.group(1).strip(), int(m.group(2))
    if not rune:
        raise ParseError(f"`{REPEAT}` 前缺少魔文：{part}")
    if times <= 0:
        raise ParseError(f"重复次数必须为正：{part}")
    return [rune] * times


def parse(text: str) -> SpellSource:
    body: str | None = None
    name: str | None = None
    element: str | None = None

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = _DEF.match(line)
        if not m:
            raise ParseError(f"无法解析：{line}", lineno)
        if body is not None:
            raise ParseError("一个文件只允许一个咒语", lineno)
        name, element, body = m.group(1), m.group(2), m.group(3)

    if name is None or element is None or body is None:
        raise ParseError("缺少 `名字 : 元素 = 魔文序列`")

    runes: list[str] = []
    for part in body.split(ARROW):
        part = part.strip()
        if not part:
            raise ParseError(f"`{ARROW}` 两侧不能为空")
        runes.extend(_expand(part))

    return SpellSource(name=name, element=element, runes=tuple(runes))
