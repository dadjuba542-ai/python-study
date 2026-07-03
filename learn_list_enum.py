# ================================================================
# 教学脚本：列表推导式 + enumerate()
# 现实类比：你有一个水果摊，每天要处理一堆水果清单
# ================================================================

# ================================================================
# 第一部分：列表推导式
# 作用：从旧列表生成新列表，一行代替 for + append
# 语法：[表达式 for 变量 in 旧列表 if 条件]
# ================================================================

print("=" * 55)
print("第一部分：列表推导式")
print("=" * 55)

# 原始数据：你摊上的水果价格
prices = [5, 12, 8, 20, 3, 15]

# ---- 场景 1：全部涨价 1 块 ----
# 传统写法：
# new_prices = []
# for p in prices:
#     new_prices.append(p + 1)

# 列表推导式：
new_prices = [p + 1 for p in prices]
print(f"原价：{prices}")
print(f"涨价1块：{new_prices}")

# ---- 场景 2：只挑出贵的（超过 10 块的） ----
# if 加在 for 后面 → 筛选
expensive = [p for p in prices if p > 10]
print(f"\n原价：{prices}")
print(f"超过10块的：{expensive}")

# ---- 场景 3：贵的打折，便宜的维持原价 ----
# if-else 加在 for 前面 → 条件变换
adjusted = [p * 0.8 if p > 10 else p for p in prices]
print(f"\n原价：{prices}")
print(f"贵的打8折：{adjusted}")

# ---- 场景 4：把字符串转成整数 ----
# 常用于读取文件后清洗数据
str_numbers = ["3", "15", "7", "22"]
int_numbers = [int(s) for s in str_numbers]
print(f"\n字符串列表：{str_numbers}")
print(f"转成数字：{int_numbers}")

# ---- 总结对比 ----
print("\n--- 列表推导式对照表 ---")
print("格式：[表达式 for 变量 in 列表]")
print("              ↑ 从哪拿")
print("        ↑ 叫什么     ")
print("  ↑ 加工后变成啥       ")
print("加筛选：[表达式 for 变量 in 列表 if 条件]")
print("加判断：[值A if 条件 else 值B for 变量 in 列表]")

# ================================================================
# 第二部分：enumerate()
# 作用：循环时同时拿到"第几个"和"值"
# 语法：for 索引, 值 in enumerate(列表)
# ================================================================

print("\n" + "=" * 55)
print("第二部分：enumerate()")
print("=" * 55)

fruits = ["苹果", "香蕉", "橘子", "葡萄"]

# ---- 场景 1：给商品编号 ----
# 传统写法：
# i = 0
# for f in fruits:
#     print(f"{i+1}. {f}")
#     i += 1

# enumerate 写法：
for i, f in enumerate(fruits):
    print(f"{i+1}. {f}")
# i 自动从 0 开始，每轮加 1

# ---- 场景 2：从 1 开始编号 ----
print()
for i, f in enumerate(fruits, start=1):
    print(f"第{i}个水果：{f}")

# ---- 场景 3：遍历时修改原列表 ----
products = ["鼠标", "键盘", "显示器", "耳机"]
for i, name in enumerate(products):
    products[i] = f"{i+1}. {name}"
print(f"\n编号后：{products}")

# ---- 场景 4：enumerate 用于查找 ----
# 找出价格低于 10 块的商品在列表中的位置
prices = [15, 8, 12, 5, 20]
for i, p in enumerate(prices):
    if p < 10:
        print(f"找到便宜货：索引{i}，价格{p}")

# ---- 总结对比 ----
print("\n--- enumerate() 对照表 ---")
print("传统写法：                         ")
print("  i = 0                            ")
print("  for item in list:                ")
print("      print(i, item)               ")
print("      i += 1                       ")
print("                                   ")
print("enumerate 写法：                   ")
print("  for i, item in enumerate(list):  ")
print("      print(i, item)               ")
print("                                   ")
print("  ↑ 变量1 = 索引（第几个）          ")
print("      ↑ 变量2 = 元素（值）         ")

# ================================================================
# 第三部分：两个一起用
# ================================================================

print("\n" + "=" * 55)
print("第三部分：组合实战")
print("=" * 55)

# 案例：找出打折商品并编号
prices = [5, 12, 8, 20, 3, 15]

# 先用列表推导式筛出打折商品（原价超过10块，打8折）
discounted = [round(p * 0.8, 1) for p in prices if p > 10]
print(f"打折商品价格：{discounted}")

# 再用 enumerate 给它们编号
for i, price in enumerate(discounted, start=1):
    print(f"  特价{i}：{price}元")
