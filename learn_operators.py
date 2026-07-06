"""
第 2 课：运算符 —— == 和 is 的区别，and/or/not 的规则
"""

# ================================================================
# 第一部分：== 和 is
# == 问的是"内容一样吗"
# is 问的是"是同一个东西吗"
# ================================================================

print("=" * 55)
print("1. == 和 is 的区别")
print("=" * 55)

# 两个人穿着一模一样的衣服
a = [1, 2, 3]
b = [1, 2, 3]

# == 问的是"看起来一样吗"
print(f"a = {a}")
print(f"b = {b}")
print(f"a == b → {a == b}   ← 内容一样，True")
print(f"a is b → {a is b}   ← 不是同一个对象，False")

# is 什么时候是 True？—— 当两个变量指向同一个东西时
c = a  # c 和 a 指向同一个列表
print(f"\nc = a 之后：")
print(f"a is c → {a is c}   ← 是同一个对象，True")

# 实际影响：改 c 也会改 a，因为它们是同一个东西
c.append(4)
print(f"c.append(4) 之后，a 也变了：{a}")

# --- 特殊情况：小整数和短字符串 ---
print("\n--- 特殊情况 ---")
x = 256
y = 256
print(f"x = 256, y = 256")
print(f"x is y → {x is y}   ← Python 缓存了小整数")

x2 = 257
y2 = 257
print(f"\nx2 = 257, y2 = 257")
print(f"x2 is y2 → {x2 is y2}   ← 超出缓存范围，变成 False")

# --- 什么时候用 is ---
# is 最常见的正确用法：判断 None
result = None
print(f"\n--- is 的正确用法 ---")
print(f"result is None → {result is None}")  # √ 推荐
print(f"result == None → {result == None}")  # 也能用，但不推荐


# ================================================================
# 第二部分：and / or / not —— 组合多个判断条件
# ================================================================

print("\n" + "=" * 55)
print("2. and / or / not  —— 组合条件")
print("=" * 55)

age = 25
has_ticket = True
is_vip = False

# --- and：两个都要满足 ---
print(f"age = {age}, has_ticket = {has_ticket}, is_vip = {is_vip}")
print(f"\nage > 18 and has_ticket → {age > 18 and has_ticket}")
#  age > 18 = True, has_ticket = True → True and True = True

# --- or：二选一就行 ---
print(f"\nis_vip or has_ticket → {is_vip or has_ticket}")
#  is_vip = False, has_ticket = True → False or True = True

# --- not：反过来 ---
print(f"\nnot is_vip → {not is_vip}")
#  not False = True

# --- 组合使用 ---
print(f"\n(age > 18 or is_vip) and has_ticket → {(age > 18 or is_vip) and has_ticket}")
#  (True or False) and True → True and True → True


# ================================================================
# 第三部分：真值表 —— 什么值相当于 True，什么值相当于 False
# ================================================================

print("\n" + "=" * 55)
print("3. 真值表 —— 哪些值相当于 True/False")
print("=" * 55)

# 以下值在 if 判断里相当于 False
false_values = [None, 0, 0.0, "", [], {}, ()]
print("相当于 False 的值：")
for v in false_values:
    # bool(v) 可以看出 v 是 True 还是 False
    print(f"  bool({v!r}) → {bool(v)}")

# 其余所有值都相当于 True
print(f"\n相当于 True 的值：")
print(f"  bool(1)      → {bool(1)}")
print(f"  bool(-1)     → {bool(-1)}")
print(f"  bool('abc')  → {bool('abc')}")
print(f"  bool([0])    → {bool([0])}   ← 注意：空列表是 False，但 [0] 有内容所以是 True")


# ================================================================
# 第四部分：实战 —— 权限检查
# ================================================================

print("\n" + "=" * 55)
print("4. 实战：权限检查")
print("=" * 55)

def check_access(user):
    """检查用户是否有权限进入。返回 (是否通过, 原因)。"""

    # 如果 user 是 None，直接拒绝
    if user is None:
        return False, "用户未登录"

    name = user.get("name", "未知")
    is_admin = user.get("is_admin", False)
    is_member = user.get("is_member", False)
    age = user.get("age", 0)

    # 未满 18 岁，拒绝
    if age < 18:
        return False, f"{name} 未满 18 岁"

    # admin 或会员都可以进
    if is_admin or is_member:
        return True, f"{name} 欢迎进入"
    else:
        return False, f"{name} 不是会员也不是管理员"


# 测试几个用户
users = [
    None,
    {"name": "小明", "age": 17, "is_admin": False, "is_member": False},
    {"name": "小红", "age": 25, "is_admin": False, "is_member": True},
    {"name": "老王", "age": 30, "is_admin": True, "is_member": False},
    {"name": "路人", "age": 22, "is_admin": False, "is_member": False},
]

for user in users:
    passed, reason = check_access(user)
    symbol = "✅" if passed else "❌"
    print(f"  {symbol} {reason}")


# ================================================================
# 第五部分：进阶挑战 —— 规则管理器
# 试着读懂下面这个函数在做什么，然后自己修改规则测试
# ================================================================

print("\n" + "=" * 55)
print("5. 进阶挑战：规则管理器")
print("=" * 55)

def evaluate_rules(age, score, has_coupon):
    """
    根据多条规则判断用户能否享受优惠。
    
    规则：
    1. 年龄 >= 60 → 老人优惠，直接通过
    2. 年龄 < 18 → 学生优惠，分数必须 >= 80
    3. 有优惠券并且分数 >= 60 → 通过
    4. 分数 >= 90 → 优秀奖励，通过
    5. 其他情况 → 不通过
    """

    if age >= 60:
        return True, "老人优惠"
    if age < 18 and score >= 80:
        return True, "学生优惠"
    if has_coupon and score >= 60:
        return True, "优惠券折扣"
    if score >= 90:
        return True, "优秀奖励"
    return False, "不符合任何优惠条件"


# 测试数据
cases = [
    (65, 70, False),   # 老人
    (16, 90, False),   # 高分学生
    (16, 70, False),   # 低分学生
    (30, 85, True),    # 有券高分
    (30, 85, False),   # 无券高分
    (30, 95, False),   # 优秀
    (25, 50, False),   # 都不符合
]

print("年龄  分数  有券  →  结果")
print("-" * 30)
for age, score, coupon in cases:
    passed, reason = evaluate_rules(age, score, coupon)
    print(f" {age}   {score}    {int(coupon)}   →  {reason}")


# ================================================================
# 速查表
# ================================================================

print("\n" + "=" * 55)
print("速查表")
print("=" * 55)
print("""
  ==    → 问"内容一样吗"
  is    → 问"是同一个东西吗"
  is None → 判断是否为空的推荐写法

  and   → 两个都要 True，结果才是 True
  or    → 只要有一个 True，结果就是 True
  not   → 把 True 变 False，False 变 True

  相当于 False 的值：
  None, 0, 0.0, "", [], {}, ()
  其他所有值都相当于 True
""")
