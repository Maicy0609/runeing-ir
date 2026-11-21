# runeing-ir

《变成软糯魔女？不对是钢筋大运！》魔文魔法体系的形式化项目。

- 目录名：`runeing-ir`
- 包名 / Python 模块名：`runeing`
- 文档语言：中文为主，术语保留原文用词（魔文 / 环 / 连笔）

## 状态

语料库刚建立，处于**审计阶段**，尚未进入语言设计。
三项关键参数（环间引用 / 参数离散 / 起点朝向）已冻结为设计选择，见 `docs/decisions.md`。

## 目录

| 路径 | 内容 |
|---|---|
| `docs/decisions.md` | 决议表：原文 / 推断 / 设计选择 / 悬置 + 翻案条件 |
| `docs/open-questions.md` | 开放问题与判据 |
| `corpus/schema.md` | 语料字段定义 |
| `corpus/corpus.jsonl` | 逐条语料，一行一条 |
| `corpus/queries.md` | 查询词记录与复测结果 |
| `proto/` | 最小原型 |

## 引用约定

每条结论必须落在四类之一：

- `原文`：附章节 + 逐字引文（≤40 字）
- `推断`：附依据
- `设计选择`：附默认值与翻案条件
- `悬置`：无证据，不进入模型

设定类结论只接受 `叙述` 与 `可靠角色陈述`；`推测` / `疑问` / `心理` 一律降级。

## 语言

源语言参考见 **[docs/language.md](docs/language.md)**。

```
光射线 : 光 = 发光 → 点 → 发射 → 发射
```

```bash
python3 examples/compile.py examples/light_ray.rune
```

`→` 就是连笔方向（第 16 章“从一个魔文的末尾连接另一个魔文的开头”）。
源码里没有连笔的形状——那是施法者私有的。

## 示例

```bash
python3 examples/demo.py
```

| 输入 | 预期输出 |
|---|---|
| `"光射线"` | 元素 光；声明 4 魔文；`create=['发光','点']` [推断]；`emit` 2 个；求值 `Value('光','projectile')` |
| `"丢冰块"` | 元素 冰；声明 4 魔文；`create=None` [unknown]；已知 2/4；求值 `Value('冰','projectile')` |
| `"火苗"` | `None`（不在投射模板内） |
| `10 / 13 / 15 / 4` | 常态 / 一秒后崩溃 / 失败 / unknown |
| `"光" / "水" / "雷"` | 有实例 / 仅提及 / 未出现 |

只认识 `corpus/templates.jsonl` 里的咒语；其余一律 `None`，不猜。

## 许可证

| 部分 | 许可 |
|---|---|
| 代码（`proto/`、`tools/`） | [MIT](LICENSE) |
| 文档与语料结构（`docs/`、`corpus/`、`README.md`） | [CC BY-NC-SA 4.0](LICENSE-DOCS) |
| 小说原文摘录 | 不授权，版权属作者与平台 |

**第三方内容**：仓库内含小说《变成软糯魔女？不对是钢筋大运！》（作者：太阳花田里的树）
的短摘录，仅用于评论与技术分析，不在本仓库任何许可证覆盖范围内。详见 [NOTICE](NOTICE)。
