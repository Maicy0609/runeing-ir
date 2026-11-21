"""魔法源码编译器 CLI。

用法：
    python3 examples/compile.py examples/light_ray.rune
    python3 examples/compile.py examples/oversize.rune
"""
from __future__ import annotations

import sys
from pathlib import Path

PROTO = Path(__file__).resolve().parents[1] / "proto"
if str(PROTO) not in sys.path:
    sys.path.insert(0, str(PROTO))

from runeing.compile import check, evaluate, has_error, lower  # noqa: E402
from runeing.lang import ParseError, parse  # noqa: E402


def render(path: Path) -> tuple[str, int]:
    lines: list[str] = []
    try:
        src = parse(path.read_text(encoding="utf-8"))
    except ParseError as exc:
        return f"[解析错误] {exc}", 1

    lines.append(f"[解析] 咒语 {src.name}，{src.rune_count} 个魔文")

    diags = check(src)
    for d in diags:
        lines.append(f"[{d.level}] {d.code}: {d.message}")

    if has_error(diags):
        lines.append("[终止] 编译失败，不生成 IR")
        return "\n".join(lines), 1

    ir = lower(src)
    lines.append(f"[IR] element={ir.element} form={ir.form} work={ir.work}")
    if ir.apply is not None:
        create = "+".join(ir.apply.create)
        emit = "+".join(ir.apply.emit)
        lines.append(f"     apply: ({create}) |> ({emit})")
    lines.append(f"[求值] {evaluate(ir)}")
    return "\n".join(lines), 0


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: compile.py <file.rune>")
        return 2
    out, code = render(Path(sys.argv[1]))
    print(out)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
