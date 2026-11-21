"""文档与实现不漂移：文档里的示例必须就是可跑文件的内容。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _first_code_line(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if stripped:
            return stripped
    raise AssertionError(f"{path} 没有有效代码行")


def test_language_doc_contains_runnable_examples() -> None:
    doc = (ROOT / "docs" / "language.md").read_text(encoding="utf-8")
    for name in ("light_ray.rune", "oversize.rune", "bad_element.rune"):
        code = _first_code_line(ROOT / "examples" / name)
        assert code in doc, f"examples/{name} 的源码没有出现在 docs/language.md 中"


def test_readme_quickstart_matches_example() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    code = _first_code_line(ROOT / "examples" / "light_ray.rune")
    assert code in readme, "README 快速开始与 examples/light_ray.rune 不一致"


def test_doc_has_no_fullwidth_syntax() -> None:
    """语法符号必须 ASCII：文档里的示例行不得出现 → 或 ×。"""
    for name in ("light_ray.rune", "oversize.rune", "bad_element.rune"):
        code = _first_code_line(ROOT / "examples" / name)
        assert "→" not in code and "×" not in code, f"{name} 含全角语法符号"
