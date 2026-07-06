"""
第14课：函数进阶与模块 —— 参数的玩法 + 模块组织
100-Days 对应 Day14
"""

# ================================================================
# 第一部分：函数定义回顾 + 为什么需要函数
# 核心：消除重复代码。一次封装，到处用。
# ================================================================

print("=" * 55)
print("1. 函数消除重复 —— 阶乘的例子")
print("=" * 55)

# 不用函数：求 C(7,3) 要写三遍阶乘循环，重复代码
# 用函数：把阶乘逻辑包起来，只写一次

def fac(num):
    """计算 num 的阶乘"""
    result = 1
    for n in range(2, num + 1):
        result *= n
    return result

m, n = 7, 3
print(f"C({m},{n}) = {fac(m) // fac(n) // fac(m - n)}")
# 三次调用 fac，但阶乘逻辑只写了一处

# Python 自带的 math.factorial 也能算，不用自己造轮子
from math import factorial as f
print(f"用 math.factorial 验证：{f(m) // f(n) // f(m - n)}")


# ================================================================
# 第二部分：参数的四种玩法
# 现实类比：你开了一家店，有的顾客只说来几杯（位置参数），
# 有的说糖度冰量都要指定（关键字参数），
# 有的说先上着后面再加（默认值），
# 还有的带了一堆朋友来，人数不确定（可变参数）
# ================================================================

print("\n" + "=" * 55)
print("2. 参数的四种玩法")
print("=" * 55)

# --- 2.1 位置参数：按顺序给值 ---
def make_judgement(a, b, c):
    """判断三条边能否构成三角形"""
    return a + b > c and b + c > a and a + c > b

print(f"\n位置参数：make_judgement(3, 4, 5) = {make_judgement(3, 4, 5)}")
print(f"位置参数：make_judgement(1, 2, 3) = {make_judgement(1, 2, 3)}")

# --- 2.2 关键字参数：指名道姓地给值，顺序无所谓 ---
print(f"\n关键字参数：make_judgement(c=5, a=3, b=4) = {make_judgement(c=5, a=3, b=4)}")

# --- 2.3 参数默认值：不传就用默认 ---
def roll_dice(n=2):
    """摇色子，默认摇2颗"""
    from random import randrange
    total = 0
    for _ in range(n):
        total += randrange(1, 7)
    return total

print(f"\n参数默认值：")
print(f"  不传参 roll_dice()  = {roll_dice()}   (默认2颗)")
print(f"  传参    roll_dice(3) = {roll_dice(3)}  (指定3颗)")

# 注意：带默认值的参数必须放后面
# def wrong(a=1, b): pass  # ❌ 会报错

# --- 2.4 可变参数 *args：不知道会来多少个 ---
print(f"\n可变参数 *args：")

def add(*args):
    """对任意多个数求和"""
    total = 0
    for val in args:
        if type(val) in (int, float):
            total += val
    return total

print(f"  add()          = {add()}")
print(f"  add(1)         = {add(1)}")
print(f"  add(1, 2, 3)   = {add(1, 2, 3)}")
print(f"  add(1, 2, 'x', 3.5) = {add(1, 2, 'x', 3.5)}")
# *args 把所有传入的位置参数打包成一个元组 (1, 2, 'x', 3.5)

# --- 2.5 可变关键字参数 **kwargs：不知道会传来什么键值对 ---
print(f"\n可变关键字参数 **kwargs：")

def foo(*args, **kwargs):
    """接收任意位置参数和关键字参数"""
    print(f"  args  = {args}")    # 元组
    print(f"  kwargs = {kwargs}")  # 字典

foo(3, 2.1, True, name="小明", age=25, score=95)
# **kwargs 把所有关键字参数打包成一个字典


# ================================================================
# 第三部分：强制位置参数 / 和命名关键字参数 *
# 场景：你开了一个自助餐厅，
#   / 前面的参数 = "必须排队按顺序拿"
#   * 后面的参数 = "必须喊名字才能给"
# ================================================================

print("\n" + "=" * 55)
print("3. / 和 *  —— 强制位置 vs 命名关键字")
print("=" * 55)

# --- 3.1 / 前面的是强制位置参数（只能按顺序传，不能写名字）---
def judge_pos(a, b, c, /):
    return a + b > c and b + c > a and a + c > b

print(f"\n强制位置参数：judge_pos(3, 4, 5) = {judge_pos(3, 4, 5)}")
# judge_pos(a=3, b=4, c=5)  # ❌ 会报错，因为 / 禁止写参数名

# --- 3.2 * 后面的是命名关键字参数（必须写名字才能传）---
def judge_key(*, a, b, c):
    return a + b > c and b + c > a and a + c > b

print(f"命名关键字参数：judge_key(a=3, b=4, c=5) = {judge_key(a=3, b=4, c=5)}")
# judge_key(3, 4, 5)  # ❌ 会报错，因为 * 禁止传位置参数

# --- 3.3 混合写法：左边位置，右边关键字 ---
def judge_mix(a, b, /, c, *, d):
    """a,b 只能按位置；c 两者都行；d 只能按名字"""
    return a + b + c + d

print(f"混合参数：judge_mix(1, 2, 3, d=4) = {judge_mix(1, 2, 3, d=4)}")


# ================================================================
# 第四部分：模块管理 —— 用文件名解决命名冲突
# 现实类比：两个人都叫"小王"，但你加上部门名就能分清
#  module1.py 里有个 foo()
#  module2.py 里也有个 foo()
#  用 import module1 → module1.foo() 区分
# ================================================================

print("\n" + "=" * 55)
print("4. 模块管理 —— 同名函数不打架")
print("=" * 55)

# 在同一个文件里定义两个同名函数，后面的会覆盖前面的
def foo():
    return "第一个 foo"

def foo():
    return "第二个 foo"

# foo() 只会输出第二个
print(f"\n同名覆盖：foo() = {foo()}")

# 正确的做法：把函数放到不同模块里
# 比如建两个文件：
# my_math.py  → def add(a, b): return a + b
# my_text.py  → def add(a, b): return a + b  (拼接)
# 使用时 import my_math → my_math.add(1, 2) 不会搞混

# Python 模块就是一个 .py 文件，import 就是导入另一个文件的内容

# 导入的三种方式：
# import 模块名              → 模块名.函数名()
# from 模块名 import 函数名   → 直接函数名()
# from 模块名 import 函数名 as 别名 → 别名()


# ================================================================
# 第五部分：实用内置函数一览（不用 import 直接用的）
# ================================================================

print("\n" + "=" * 55)
print("5. 常用内置函数速览")
print("=" * 55)

tests = [
    ("abs(-5)", abs(-5)),
    ("pow(2, 3)", pow(2, 3)),
    ("round(3.14159, 2)", round(3.14159, 2)),
    ("max(3, 7, 2, 9, 5)", max(3, 7, 2, 9, 5)),
    ("min(3, 7, 2, 9, 5)", min(3, 7, 2, 9, 5)),
    ("sum([1, 2, 3, 4, 5])", sum([1, 2, 3, 4, 5])),
    ("len('你好世界')", len("你好世界")),
    ("type(42)", type(42)),
    ("ord('A')", ord('A')),
    ("chr(65)", chr(65)),
]

for expr, result in tests:
    print(f"  {expr} → {result}")


# ================================================================
# 速查
# ================================================================

print("\n" + "=" * 55)
print("速查表")
print("=" * 55)
print("""
  def 函数名(参数):    定义函数
  return 值            返回值（不写 return → None）

  参数类型：
    位置参数          按顺序传值
    关键字参数         按名字传值（顺序随意）
    默认值参数         不传就用默认值（必须放最后）
    *args            任意多个位置参数 → 打包成元组
    **kwargs          任意多个关键字参数 → 打包成字典
    参数 /            / 前面的参数只能按位置传
    *, 参数           * 后面的参数只能按名字传

  模块：
    import 模块名                  → 模块名.函数名()
    from 模块名 import 函数名       → 直接使用
    import 模块名 as 别名           → 别名.函数名()
""")
