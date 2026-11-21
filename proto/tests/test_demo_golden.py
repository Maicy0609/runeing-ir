"""示例输出的黄金测试：预期输出是断言，不是描述。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "demo.py"

EXPECTED = """\
=== 示例 1：完整实例 ===
输入: "光射线"
输出:
  元素: 光
  声明魔文数: 4
  create: ['发光', '点'] [推断]
  emit: ['发射-1', '发射-2']
  已知魔文: 4/4
  求值: Value(element='光', form='projectile', work=4, pipeline=('发光+点', '发射-1+发射-2'))
  容量(4): unknown

=== 示例 2：残缺实例 ===
输入: "丢冰块"
输出:
  元素: 冰
  声明魔文数: 4
  create: None [unknown]
  emit: ['发射-1', '发射-2']
  已知魔文: 2/4
  求值: Value(element='冰', form='projectile', work=4, pipeline=())
  容量(4): unknown

=== 示例 3：不认识的咒语 ===
输入: "火苗"
输出: None（不在投射模板内）

=== 示例 4：容量 ===
输入: 10 → 输出: 常态
输入: 13 → 输出: 一秒后崩溃
输入: 15 → 输出: 失败
输入: 4 → 输出: unknown

=== 示例 5：元素 ===
输入: "光" → 输出: 有实例
输入: "水" → 输出: 仅提及
输入: "雷" → 输出: 未出现"""


def test_demo_stdout_matches_expected() -> None:
    result = subprocess.run(
        [sys.executable, str(DEMO)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.rstrip("\n") == EXPECTED.rstrip("\n")
