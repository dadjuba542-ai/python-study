# ================================================================
# Day17：函数高级应用 —— 装饰器 + 递归
# ================================================================

# ================================================================
# 第一部分：装饰器（Decorator）
#
# 本质：不修改原函数，给它"套一层壳"，加额外功能。
# 现实类比：你有一台咖啡机（原函数），
#           你给它加了一个"自动投币"的外壳（装饰器），
#           这样每次用的时候先投币，再出咖啡。
# ================================================================

print("=" * 60)
print("第一部分：装饰器（Decorator）")
print("=" * 60)

# ---- 1.1 最简单的装饰器 ----
# 在不改 say_hello 的前提下，给它的输出加个框

def add_frame(func):
    """装饰器：给函数输出加一圈框"""
    def wrapper():
        print("-" * 20)
        func()
        print("-" * 20)
    return wrapper

@add_frame
def say_hello():
    print("你好，世界！")

print("\n1.1 普通调用：")
say_hello()
# 输出：
# --------------------
# 你好，世界！
# --------------------

# ---- 1.2 装饰器原理拆解 ----
# @add_frame 等价于 say_hello = add_frame(say_hello)
# 所以装饰器本质就是：把原函数传给一个函数，返回一个新函数。

print("\n1.2 原理：@add_frame 等价于：")
print("  say_hello = add_frame(say_hello)")

# ---- 1.3 带参数的函数装饰 ----
# 原函数有参数，wrapper 也要接收同样的参数

def log_call(func):
    """装饰器：记录函数被调用了，参数是什么"""
    def wrapper(name, age):
        print(f"  [日志] 调用了 {func.__name__}({name}, {age})")
        return func(name, age)
    return wrapper

@log_call
def introduce(name, age):
    print(f"  我叫{name}，今年{age}岁。")

print("\n1.3 带参数的装饰器：")
introduce("小明", 18)
# 输出：
#   [日志] 调用了 introduce(小明, 18)
#   我叫小明，今年18岁。

# ---- 1.4 通用装饰器（*args, **kwargs） ----
# 用可变参数，不管原函数有几个参数，装饰器都能通用

def log_call_v2(func):
    """通用版日志装饰器：不管原函数有几个参数都能用"""
    def wrapper(*args, **kwargs):
        print(f"  [日志] 调用了 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call_v2
def add(a, b):
    return a + b

@log_call_v2
def greet(name):
    print(f"  你好，{name}！")

print("\n1.4 通用装饰器（任意参数）：")
print(f"  add(3, 5) = {add(3, 5)}")
greet("张三")

# ---- 1.5 实际场景：计时装饰器 ----
# 测量函数执行时间，调试性能时非常有用

import time

def timer(func):
    """装饰器：计算函数执行时间"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"  [{func.__name__}] 耗时：{end - start:.4f} 秒")
        return result
    return wrapper

@timer
def slow_add(n):
    """模拟一个慢速计算"""
    total = 0
    for i in range(n):
        total += i
        time.sleep(0.0001)  # 模拟耗时
    return total

print("\n1.5 计时装饰器：")
result = slow_add(1000)
print(f"  计算结果：{result}")

# ---- 1.6 实际场景：权限检查装饰器 ----

def require_login(func):
    """装饰器：模拟检查用户是否登录"""
    def wrapper(*args, **kwargs):
        # 模拟检查（实际项目中会查 session/token）
        if not getattr(wrapper, "logged_in", False):
            print("  [权限] 未登录，拒绝访问！")
            return None
        return func(*args, **kwargs)
    return wrapper

@require_login
def view_profile():
    print("  个人资料：张三，18岁，Python爱好者")

print("\n1.6 权限装饰器：")
view_profile()  # 没登录，被拒

require_login.logged_in = True  # 模拟登录
view_profile()  # 已登录，放行

# ---- 1.7 多个装饰器叠加 ----
# 一个函数可以套多层装饰器，执行顺序：从下往上套，从上往下执行

def bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def italic(func):
    def wrapper():
        return "<i>" + func() + "</i>" + "（斜体）"
    return wrapper

@bold
@italic
def get_text():
    return "你好"

print("\n1.7 多层装饰器：")
print(f"  结果：{get_text()}")
# 执行顺序：先 italic 再 bold
# 等价于 get_text = bold(italic(get_text))

# ---- 1.8 装饰器总结 ----
print("\n--- 装饰器总结 ---")
print("装饰器 = 在不改原函数代码的前提下，给它加功能")
print("固定格式：")
print("  def 装饰器名(func):")
print("      def wrapper(*args, **kwargs):")
print("          # 调用前做的事")
print("          result = func(*args, **kwargs)")
print("          # 调用后做的事")
print("          return result")
print("      return wrapper")
print("")
print("使用：@装饰器名 放在函数定义上面")


# ================================================================
# 第二部分：递归（Recursion）
#
# 本质：函数自己调用自己。
# 现实类比：俄罗斯套娃——打开一个，里面还有一个，直到最小的那个。
# 递归必须有两个要素：
#   ① 终止条件（不再调用自己）
#   ② 递推公式（调用自己，且参数越来越接近终止条件）
# ================================================================

print("\n" + "=" * 60)
print("第二部分：递归（Recursion）")
print("=" * 60)

# ---- 2.1 阶乘（n!）—— 递归入门 ----
# n! = n × (n-1) × (n-2) × ... × 1
# 递推公式：n! = n × (n-1)!
# 终止条件：1! = 1

def factorial(n):
    """计算 n 的阶乘"""
    if n == 1:           # 终止条件
        return 1
    return n * factorial(n - 1)   # 递推公式：调用自己

print("\n2.1 阶乘：")
print(f"  5! = {factorial(5)}")   # 5×4×3×2×1 = 120

# 执行过程拆解：
# factorial(5)
# → 5 * factorial(4)
# → 5 * 4 * factorial(3)
# → 5 * 4 * 3 * factorial(2)
# → 5 * 4 * 3 * 2 * factorial(1)
# → 5 * 4 * 3 * 2 * 1
# → 120

# ---- 2.2 斐波那契数列 ----
# 0, 1, 1, 2, 3, 5, 8, 13, 21...
# 递推公式：f(n) = f(n-1) + f(n-2)
# 终止条件：f(0) = 0, f(1) = 1

def fib(n):
    """返回第 n 个斐波那契数"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)

print("\n2.2 斐波那契数列：")
for i in range(10):
    print(f"  fib({i}) = {fib(i)}", end="")
print()

# ---- 2.3 递归遍历文件夹 ----
# 递归最实用的场景：遍历嵌套结构
import os

def scan_folder(path, indent=0):
    """递归遍历文件夹，打印所有文件和子文件夹"""
    prefix = "  " * indent
    try:
        items = os.listdir(path)
    except PermissionError:
        return

    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print(f"{prefix}📁 {item}/")
            scan_folder(item_path, indent + 1)   # 递归：进子文件夹
        else:
            print(f"{prefix}📄 {item}")

print("\n2.3 递归遍历当前目录：")
scan_folder(".", 0)

# ---- 2.4 递归反向输出字符串 ----

def reverse_string(s):
    """递归反转字符串"""
    if len(s) == 0:
        return ""
    return reverse_string(s[1:]) + s[0]

print("\n2.4 递归反转字符串：")
print(f"  'Python' → {reverse_string('Python')}")
# 执行过程：
# reverse_string("Python")
# → reverse_string("ython") + "P"
# → reverse_string("thon") + "y" + "P"
# → ... → "nohtyP"

# ---- 2.5 递归 vs 循环 ----
# 很多递归能做的事，循环也能做
# 选择标准：代码可读性

print("\n2.5 递归 vs 循环对比（以阶乘为例）：")

def factorial_loop(n):
    """循环实现阶乘"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(f"  递归：factorial(10) = {factorial(10)}")
print(f"  循环：factorial_loop(10) = {factorial_loop(10)}")

# ---- 2.6 递归的坑：重复计算 ----
# 斐波那契的递归实现效率很低，因为大量重复计算

@timer
def fib_slow(n):
    """慢速递归斐波那契（大量重复计算）"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_slow(n - 1) + fib_slow(n - 2)

@timer
def fib_fast(n, memo={}):
    """带缓存的递归（记忆化），避免重复计算"""
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fib_fast(n - 1, memo) + fib_fast(n - 2, memo)
    return memo[n]

print("\n2.6 递归的效率问题（计算 fib(35)）：")
print("  慢速递归（大量重复计算）：")
# fib_slow(35)   # 这行很慢，先注释掉
print("    → 约 5 秒，不建议运行")
print("  带缓存递归（记忆化）：")
result = fib_fast(35)
print(f"    fib_fast(35) = {result}，几乎瞬间完成")


# ================================================================
# 第三部分：装饰器 + 递归 实战综合
# ================================================================

print("\n" + "=" * 60)
print("第三部分：装饰器 + 递归 综合实战")
print("=" * 60)

# 实战：给递归函数加缓存装饰器
# 把"记忆化"做成通用装饰器，任何递归函数都能用

def memoize(func):
    """装饰器：为函数添加缓存（记忆化）"""
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

@memoize
def fib_memo(n):
    """带缓存装饰器的斐波那契"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_memo(n - 1) + fib_memo(n - 2)

@memoize
def factorial_memo(n):
    """带缓存装饰器的阶乘"""
    if n == 1:
        return 1
    return n * factorial_memo(n - 1)

print("\n带缓存装饰器的递归函数：")
print(f"  fib_memo(100) = {fib_memo(100)}")
print(f"  factorial_memo(50) = {factorial_memo(50)}")
print("  （能算大数，因为缓存避免了重复计算）")


# ================================================================
# 总结
# ================================================================

print("\n" + "=" * 60)
print("总结")
print("=" * 60)
print("""
装饰器（Decorator）：
  - 在不改原函数的前提下，给它加功能
  - 固定模板：外层接收函数，内层 wrapper 接收参数
  - 常用场景：日志、计时、权限检查、缓存

递归（Recursion）：
  - 函数自己调用自己
  - 必须有两个要素：终止条件 + 递推公式
  - 适合处理嵌套结构（文件夹、树状数据）
  - 注意：递归太深会栈溢出，无缓存会重复计算
""")
