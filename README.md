# runeing-ir

《变成软糯魔女？不对是钢筋大运！》魔文魔法体系的形式化项目。

- 目录名：`runeing-ir`
- 包名 / Python 模块名：`runeing`
- 文档语言：中文为主，术语保留原文用词（魔文 / 环 / 连笔）

## 现在能做什么

- 写 `.rune` 源文件，编译器给出阶段化输出：解析 → 检查 → 降级 → 求值
- 容量、元素、结构三项检查，依据全部落在语料上
- 两个模板实例（光射线、丢冰块），未知字段显式标 `unknown`
- 35 个测试、`ruff`、`mypy --strict` 全绿

## 快速开始

```
光射线 : 光 = 发光 -> 点 -> 发射 -> 发射
```

```bash
python3 examples/compile.py examples/light_ray.rune
```

完整语法见 **[docs/language.md](docs/language.md)**。

## 目录

| 路径 | 内容 |
|---|---|
| `docs/language.md` | **源语言参考**（读者入口） |
| `docs/ROADMAP.md` | **规划书**：定位 B，阶段 / 验收判据 / 天花板 / 退出条件 |
| `docs/lessons.md` | 经验与教训：方法、六种反复犯的错、引文纪律 |
| `docs/decisions.md` | 决议表：原文 / 推断 / 设计选择 / 悬置 + 翻案条件 |
| `docs/open-questions.md` | 开放问题与判据 |
| `corpus/schema.md` | 语料字段定义 |
| `corpus/corpus.jsonl` | 逐条语料，44 条 |
| `corpus/templates.jsonl` | 模板实例，2 条 |
| `corpus/queries.md` | 查询词记录与复测结果 |
| `examples/` | 可跑样例（3 个 `.rune` + 2 个脚本） |
| `proto/` | 核心实现 |
| `tools/verify_quotes.py` | 引文逐字校验 |

## 两个示例的区别

| 脚本 | 作用 | 何时用 |
|---|---|---|
| `examples/compile.py` | 编译 `.rune` 源码 | **主入口**：写魔法代码时用 |
| `examples/demo.py` | 查内置模板数据 | 只想看结构化结果时用 |

`compile.py` 处理你写的源码；`demo.py` 只展示 `corpus/templates.jsonl` 里已有的两个咒语，不读源码。

## 引用约定

每条结论必须落在四类之一：

- `原文`：附章节 + 逐字引文（≤40 字）
- `推断`：附依据
- `设计选择`：附默认值与翻案条件
- `悬置`：无证据，不进入模型

设定类结论只接受 `叙述` 与 `可靠角色陈述`；`推测` / `疑问` / `心理` 一律降级。

## 许可证

| 部分 | 许可 |
|---|---|
| 代码（`proto/`、`tools/`、`examples/`） | [MIT](LICENSE) |
| 文档与语料结构（`docs/`、`corpus/`、`README.md`） | [CC BY-NC-SA 4.0](LICENSE-DOCS) |
| 小说原文摘录 | 不授权，版权属作者与平台 |

**第三方内容**：仓库内含小说《变成软糯魔女？不对是钢筋大运！》（作者：太阳花田里的树）
的短摘录，仅用于评论与技术分析，不在本仓库任何许可证覆盖范围内。详见 [NOTICE](NOTICE)。
