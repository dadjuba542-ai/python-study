"""
Day16 —— 函数使用进阶：高阶函数、Lambda、偏函数
100-Days 对应 Day16
"""

import operator
import functools

# ================================================================
# 第一部分：高阶函数 —— 把函数当参数传
# 核心思想：函数和数字、字符串一样，可以传来传去
# 现实类比：你开了一家加工厂，客户说"我要加1"还是"我要乘2"
#          你把"加1"或"乘2"这个操作本身当成参数送进流水线
# ================================================================

print("=" * 55)
print("1. 高阶函数 —— 函数也能当参数")
print("=" * 55)

# ---- 场景：一个可以自定义运算的"计算器" ----
# 常规写法：calc 固定做加法
# def calc(*args):
#     result = 0
#     for v in args:
#         result += v
#     return result

# 高阶函数写法：把"怎么算"也作为参数传进来
def calc(init, op, *args):
    """
    高阶函数：对任意多个数做指定运算。
    init = 初始值
    op   = 运算函数（加法、乘法、……）
    args = 要计算的数字
    """
    result = init
    for v in args:
        if type(v) in (int, float):
            result = op(result, v)
    return result

# 定义两个运算函数
def add(x, y):
    return x + y

def mul(x, y):
    return x * y

# 把 add / mul 当成参数传进去
print(f"  calc(0, add, 1, 2, 3, 4, 5)     = {calc(0, add, 1, 2, 3, 4, 5)}")
print(f"  calc(1, mul, 1, 2, 3, 4, 5)     = {calc(1, mul, 1, 2, 3, 4, 5)}")

# 也可以用 operator 模块自带的 add/mul（不用自己定义）
print(f"  calc(0, operator.add, 1,2,3,4,5) = {calc(0, operator.add, 1,2,3,4,5)}")
print(f"  calc(1, operator.mul, 1,2,3,4,5) = {calc(1, operator.mul, 1,2,3,4,5)}")

print("\n  —— 关键在于不要把 op 写成 op() ——")
print("  op   = 把函数传进去（不执行）")
print("  op() = 当场执行函数，再把结果传进去（错了）")


# ---- 高阶函数的另一个例子：sorted 的 key 参数 ----
print("\n" + "-" * 55)
print("  sorted() 的 key 参数也是高阶函数")

words = ["in", "apple", "zoo", "waxberry", "pear"]

# 默认按字母排序
print(f"  默认排序：{sorted(words)}")

# 按字符串长度排序 —— len 函数本身作为参数
print(f"  按长度：{sorted(words, key=len)}")

# key 参数 = "排序时，用这个函数处理每个元素，按处理后的结果比大小"
# len("in")=2, len("apple")=5, ... 所以短的排前面


# ================================================================
# 第二部分：Lambda 函数 —— 匿名的一行函数
# 适用场景：函数很简单（一行），只用一次，不值得用 def 起名字
# ================================================================

print("\n" + "=" * 55)
print("2. Lambda 函数 —— 不用 def 起名字")
print("=" * 55)

# ---- 传统写法 ----
def square(x):
    return x ** 2

def is_even(x):
    return x % 2 == 0

# ---- Lambda 等价写法 ----
# lambda 参数: 表达式
square_lambda = lambda x: x ** 2
is_even_lambda = lambda x: x % 2 == 0

print(f"  square(5)          = {square(5)}")
print(f"  square_lambda(5)   = {square_lambda(5)}")
print(f"  is_even(4)         = {is_even(4)}")
print(f"  is_even_lambda(4)  = {is_even_lambda(4)}")

# ---- 实际场景：和 filter / map 搭配使用 ----
# filter(判断函数, 列表) → 过滤
# map(变换函数, 列表)    → 映射
old = [35, 12, 8, 99, 60, 52]

# 用传统函数
def is_even_filter(x):
    return x % 2 == 0

result1 = list(map(square, filter(is_even_filter, old)))
print(f"\n  传统函数版：{result1}")

# 用 lambda —— 省掉 is_even_filter 和 square 的定义
result2 = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, old)))
print(f"  Lambda 版：{result2}")

# 列表推导式也能干同样的事，更直观
result3 = [x**2 for x in old if x % 2 == 0]
print(f"  推导式版：{result3}")

# Lambda 语法总结：
# lambda 参数: 表达式
#    ↑       ↑    ↑
#  关键字  参数  结果（不用写 return）


# ================================================================
# 第三部分：偏函数 —— 固定某些参数，造一个新函数
# 现实类比：你常买某家咖啡，每次都说"美式，少冰，无糖"
#          你直接起个名字叫"我的咖啡"，以后只说这个名字就好
# ================================================================

print("\n" + "=" * 55)
print("3. 偏函数 —— 固定参数，造简化版")
print("=" * 55)

# ---- 例子：int() 默认把字符串当十进制 ----
# int("1001") = 1001
# 但你可以通过 base 参数指定进制

# 常规写法：每次都写 base
print(f"  int('1001', base=2)  = {int('1001', base=2)}")   # 二进制 → 9
print(f"  int('1001', base=8)  = {int('1001', base=8)}")   # 八进制 → 513
print(f"  int('1001', base=16) = {int('1001', base=16)}")  # 十六进制 → 4097

# 偏函数：固定 base 参数，造三个专用函数
int2 = functools.partial(int, base=2)
int8 = functools.partial(int, base=8)
int16 = functools.partial(int, base=16)

print(f"\n  偏函数版：")
print(f"    int2('1001')  = {int2('1001')}")
print(f"    int8('1001')  = {int8('1001')}")
print(f"    int16('1001') = {int16('1001')}")

# 原理：partial(原函数, 固定的参数) → 返回一个新函数
# 新函数调用时，不需要再传那些固定的参数了


# ================================================================
# 速查
# ================================================================

print("\n" + "=" * 55)
print("速查表")
print("=" * 55)
print("""
  高阶函数：
    把函数当成参数传给另一个函数
    sorted(list, key=len)    → len 函数本身传进去
    filter(函数, 列表)        → 过滤
    map(函数, 列表)           → 映射

  Lambda 函数：
    lambda 参数: 表达式
    lambda x: x**2           → 等价于 def f(x): return x**2
    适合一行搞定、只用一次的场景

  偏函数：
    functools.partial(原函数, 固定参数) → 返回一个新函数
    int2 = partial(int, base=2)    → int2("1001") = 9

  核心概念：
    函数是一等公民 —— 可以赋值、传参、返回
    op    = 传函数本身（不执行）
    op()  = 执行函数，传结果
""")
