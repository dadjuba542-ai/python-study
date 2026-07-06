"""
第 1 课：变量类型 —— 变量到底能装什么？
"""

# ================================================================
# 第一部分：四种基本类型
# 变量 = 带标签的盒子，类型 = 盒子里装的是什么东西
# ================================================================

print("=" * 55)
print("1. int（整数）—— 就是数学里的整数")
print("=" * 55)

# int：整数，可以算数
a = 10
b = 3

print(f"a = {a}, b = {b}")
print(f"a + b = {a + b}")
print(f"a - b = {a - b}")
print(f"a * b = {a * b}")
print(f"a / b = {a / b}   ← 除出来是小数")
print(f"a // b = {a // b}  ← // 是整除，只取整数部分")
print(f"a % b = {a % b}   ← % 是取余数，10 ÷ 3 剩 1")
print(f"a ** b = {a ** b}  ← ** 是乘方，10³")


print("\n" + "=" * 55)
print("2. str（字符串）—— 就是文字")
print("=" * 55)

# str：字符串，用引号包起来的都是文字
name = "小明"
greeting = "你好"

# 字符串不能算数，只能拼接
print(f"name = '{name}', greeting = '{greeting}'")
print(f"name + greeting = '{name + greeting}'   ← 拼接")
print(f"name * 3 = '{name * 3}'               ← 重复 3 遍")

# 数字字符串和真正的数字不同
price_str = "10"
price_int = 10
print(f"\nprice_str = '{price_str}'（字符串），price_int = {price_int}（整数）")
print(f"price_str + '5' = '{price_str + '5'}'  ← 文字拼接，变成 '105'")
print(f"price_int + 5 = {price_int + 5}        ← 数字相加，等于 15")


print("\n" + "=" * 55)
print("3. bool（布尔值）—— True 或 False")
print("=" * 55)

# bool：只有两个值，True 和 False
is_done = True
is_empty = False

print(f"is_done = {is_done}")
print(f"is_empty = {is_empty}")

# bool 常来自"比较"的结果
print(f"\n比较结果：")
print(f"10 > 5  → {10 > 5}")
print(f"10 < 5  → {10 < 5}")
print(f"10 == 5 → {10 == 5}   ← == 是判断相等，两个等号")
print(f"10 != 5 → {10 != 5}   ← != 是不等于")

# bool 用在 if 后面
if is_done:
    print(f"\nif is_done: → 因为 is_done 是 True，所以这行执行了")
else:
    print("这行不会执行")


print("\n" + "=" * 55)
print("4. None（空）—— 表示'啥都没有'")
print("=" * 55)

# None：空的，特殊值
result = None
print(f"result = {result}")

# None 常表示"还没拿到结果"
def find_user(name):
    return None  # 假设没找到用户

user = find_user("张三")
print(f"查找用户返回：{user}")

# None 在 if 里相当于 False
if not user:
    print("user 是 None → 相当于 False → 进了这个分支")


# ================================================================
# 第二部分：type() —— 查看变量是什么类型
# ================================================================

print("\n" + "=" * 55)
print('5. type() —— 问 Python"这个变量是什么类型"')
print("=" * 55)

print(f"type(10)     → {type(10)}")
print(f"type('10')   → {type('10')}")
print(f"type(True)   → {type(True)}")
print(f"type(None)   → {type(None)}")

# 实用技巧：写代码不确定类型时，加一行 print(type(x)) 看看
x = "42"
print(f"\n不确定 x 的类型？→ type(x) = {type(x)}")


# ================================================================
# 第三部分：类型转换 —— 在 str 和 int 之间切换
# ================================================================

print("\n" + "=" * 55)
print("6. 类型转换 —— int() 和 str() 互相转")
print("=" * 55)

# str → int：文字转成数字，才能算数
s = "123"
n = int(s)
print(f"int('123') = {n}，类型是 {type(n)}")

# int → str：数字转成文字，才能拼接
m = 456
t = str(m)
print(f"str(456) = '{t}'，类型是 {type(t)}")

# bool → int：True = 1，False = 0
print(f"\nint(True)  = {int(True)}")
print(f"int(False) = {int(False)}")


# ================================================================
# 速查表
# ================================================================

print("\n" + "=" * 55)
print("类型速查表")
print("=" * 55)
print("""
  写法             类型          能不能算数
  ─────────────────────────────────────
  x = 42          int(整数)       ✅ 加减乘除
  x = "42"        str(字符串)     ❌ 只能拼接、重复
  x = True        bool(布尔)      特殊：True=1, False=0
  x = None        NoneType(空)   不能算数

  常用转换：
  int("123")  → 把字符串变成整数
  str(123)    → 把整数变成字符串
  bool(1)     → 任何非零、非空的值都是 True
""")
