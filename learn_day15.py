"""
Day15 —— 函数应用实战
把之前学的函数、循环、列表、字符串组合起来，写几个真实小工具
"""

import random
import string

# ================================================================
# 练习 1：生成随机验证码
# 现实类比：你登录网站时收到的短信验证码 "4832"
# ================================================================

print("=" * 55)
print("练习 1：随机验证码")
print("=" * 55)

def generate_code(length=4):
    """
    生成一个由数字组成的随机验证码。
    length = 验证码位数，默认 4 位。
    """

    # 准备一个空字符串，用来拼接结果
    code = ""

    # 循环 length 次，每次随机取一个数字
    for i in range(length):
        # random.choice() = 从一堆东西里随机挑一个
        # string.digits = "0123456789"
        code += random.choice(string.digits)

    return code


# 测试：生成 3 个验证码
print("生成的验证码：")
for i in range(3):
    print(f"  第 {i+1} 次：{generate_code()}")
    print(f"  第 {i+1} 次（6位）：{generate_code(6)}")


# ================================================================
# 练习 2：判断素数
# 素数 = 只能被 1 和它自己整除的数，比如 2, 3, 5, 7, 11
# 现实类比：找质数就是"这个数除了 1 和它自己，还有没有其他约数"
# ================================================================

print("\n" + "=" * 55)
print("练习 2：判断素数")
print("=" * 55)

def is_prime(n):
    """判断 n 是不是素数。是返回 True，不是返回 False。"""

    # 小于 2 的数都不是素数
    if n < 2:
        return False

    # 从 2 试到 n-1，看能不能整除 n
    # 如果能整除，说明 n 有别的约数 → 不是素数
    for i in range(2, n):
        if n % i == 0:    # % 是取余数，余数为 0 说明能整除
            return False

    return True


# 测试：列出 1 到 30 之间的素数
print("1 到 30 之间的素数：")
for n in range(1, 31):
    if is_prime(n):
        print(f"  {n} 是素数")

# 顺带演示：列表推导式 + 素数判断，一行找出所有素数
primes = [n for n in range(1, 31) if is_prime(n)]
print(f"\n列表推导式版：{primes}")


# ================================================================
# 练习 3：最大公约数和最小公倍数
# 最大公约数 = 能同时整除两个数的最大数
# 最小公倍数 = 能被两个数同时整除的最小数
# ================================================================

print("\n" + "=" * 55)
print("练习 3：最大公约数和最小公倍数")
print("=" * 55)

def gcd(a, b):
    """求 a 和 b 的最大公约数。"""

    # 辗转相除法（经典算法）：
    # 用小数除大数取余数，余数不为零就继续，为零时除数就是答案
    while b != 0:      # ≠0 就一直算
        a, b = b, a % b  # Python 特色写法：同时赋值，不用中间变量
    return a


def lcm(a, b):
    """求 a 和 b 的最小公倍数。"""
    # 公式：两数乘积 ÷ 最大公约数
    return a * b // gcd(a, b)


# 测试
pairs = [(12, 18), (24, 36), (7, 13)]
for a, b in pairs:
    print(f"  gcd({a}, {b}) = {gcd(a, b)}  lcm({a}, {b}) = {lcm(a, b)}")


# ================================================================
# 练习 4：数据统计
# 给一列数字，算出最大值、最小值、总和、平均值
# ================================================================

print("\n" + "=" * 55)
print("练习 4：数据统计")
print("=" * 55)

def analyze(numbers):
    """对一组数字做基本统计，返回一个字典。"""

    return {
        "最大值": max(numbers),
        "最小值": min(numbers),
        "总和": sum(numbers),
        "平均值": sum(numbers) / len(numbers),
        "个数": len(numbers),
    }


# 测试
scores = [85, 92, 78, 96, 88, 74, 91]
result = analyze(scores)

print(f"数据：{scores}")
for key, value in result.items():
    print(f"  {key}：{value}")


# ================================================================
# 练习 5：双色球随机选号
# 红球：1-33 选 6 个（不重复），篮球：1-16 选 1 个
# ================================================================

print("\n" + "=" * 55)
print("练习 5：双色球随机选号")
print("=" * 55)

def generate_lottery():
    """生成一组双色球号码。返回 (红球列表, 篮球)。"""

    # 从 1-33 里随机挑 6 个不重复的数字
    # random.sample(池子, 数量) = 从池子里抽指定数量，不重复
    red = sorted(random.sample(range(1, 34), 6))

    # 从 1-16 里随机挑 1 个
    blue = random.randint(1, 16)

    return red, blue


# 测试：生成 3 注
print("随机选号：")
for i in range(3):
    red, blue = generate_lottery()
    print(f"  第 {i+1} 注：红球 {red} + 蓝球 {blue}")


# ================================================================
# 进阶挑战：整合 —— 数据统计工具箱
# ================================================================

print("\n" + "=" * 55)
print("进阶挑战：数据统计工具箱")
print("=" * 55)

def stat_tool():
    """
    交互式统计工具：
    1. 问你一组数字
    2. 自动算最大值、最小值、总和、平均值
    3. 还能筛选出高于平均分的数字
    """

    # input() 拿到的是字符串，需要手动拆开
    raw = input("请输入一组数字（用逗号隔开）：")

    # 按逗号切开，再把每个字符串转成整数
    numbers = []
    for s in raw.split(","):
        numbers.append(int(s.strip()))

    # 算平均值
    avg = sum(numbers) / len(numbers)

    # 筛选出高于平均值的数
    above = [n for n in numbers if n > avg]

    print(f"\n统计结果：")
    print(f"  数据：{numbers}")
    print(f"  最大值：{max(numbers)}")
    print(f"  最小值：{min(numbers)}")
    print(f"  总和：{sum(numbers)}")
    print(f"  平均值：{avg}")
    print(f"  高于平均值：{above}")


# 取消下面这行的注释就能运行交互模式
# stat_tool()


# ================================================================
# 速查
# ================================================================

print("\n" + "=" * 55)
print("本课用到的新函数")
print("=" * 55)
print("""
  random.choice(列表)    → 从列表里随机挑一个
  random.sample(池子, n) → 从池子里抽 n 个，不重复
  random.randint(a, b)   → 返回 a 到 b 之间的随机整数
  string.digits          → "0123456789"
  .split(",")            → 按逗号切成列表
  .strip()               → 去掉首尾空白
""")
