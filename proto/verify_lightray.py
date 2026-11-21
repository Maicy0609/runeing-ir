"""验证：光射线 = 元素部分(2 魔文) + 发射部分(2 魔文)。

依据（第 22 章，墨砚秋）：

- 光射线由四个魔文组成，其中有两个魔文你已经学会，新的两个魔文……意思是发射
- 它的魔文含义就是发光的点
- 其实就是基础元素魔法加上发射魔文，把前者发射出去

注意：原文只说“其中有两个魔文你已经学会”，未说这两个在环上的位置，
因此本验证**不使用“前 N 个”**，只用 role 计数 + 旋转规范形。
"""
from runeing.core import Ring, Rune, Spell, capacity_status

# 名称来源：原文写的是语义“发光的点”，拆成两个魔文名属于推断
发光 = Rune("发光", role="element", name_source="推断")
点 = Rune("点", role="element", name_source="推断")
# “新的两个魔文，意思是发射” —— 两个不同魔文共同表示发射，不是同一魔文重复
发射一 = Rune("发射-1", role="emit", name_source="推断")
发射二 = Rune("发射-2", role="emit", name_source="推断")

闪光术 = Spell(name="闪光术", rings=(Ring((发光, 点)),), element="光")
光射线 = Spell(name="光射线", rings=(Ring((发光, 点, 发射一, 发射二)),), element="光")

ring = 光射线.rings[0]
base = ring.canonical()
rotations_equal = all(
    Ring(ring.runes[i:] + ring.runes[:i]).canonical() == base for i in range(len(ring.runes))
)

checks: list[tuple[str, bool]] = [
    ("光射线 魔文数 == 4", 光射线.rune_count == 4),
    ("光射线 element 角色数 == 2", ring.roles().get("element") == 2),
    ("光射线 emit 角色数 == 2", ring.roles().get("emit") == 2),
    ("元素部分 + 发射部分 == 4", 2 + 2 == 光射线.rune_count),
    ("闪光术 魔文数 == 2", 闪光术.rune_count == 2),
    ("光射线环在 4 种旋转下规范形不变", rotations_equal),
    ("光射线环闭合（边数 == 魔文数）", len(ring.edges()) == len(ring.runes)),
]

ok = True
for desc, result in checks:
    if not result:
        ok = False
    print(f"[{'PASS' if result else 'FAIL'}] {desc}")

print()
print(f"闪光术: {[r.name for r in 闪光术.rings[0].runes]}  角色={闪光术.rings[0].roles()}")
print(f"光射线: {[r.name for r in ring.runes]}  角色={ring.roles()}")
print(f"规范形(旋转归一): {base}")
print(f"容量(4 魔文): {capacity_status(光射线.rune_count)}  ← 未采样点，按不内插原则返回 unknown")
print()
print("名称来源标注：")
for r in ring.runes:
    print(f"  {r.name}: {r.name_source}")

raise SystemExit(0 if ok else 1)
