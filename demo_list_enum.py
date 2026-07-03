# ------------------------------------------------------------
# 案例：帮老板处理促销商品清单
# ------------------------------------------------------------

# 原始数据：一批商品的原始价格
prices = [99, 150, 200, 55, 300]

# ---- 列表推导式：批量打折 ----
# 老板说：超过 100 块的打 8 折，其他的不变
# 传统写法（不用列表推导式）：
# new_prices = []
# for p in prices:
#     if p > 100:
#         new_prices.append(p * 0.8)
#     else:
#         new_prices.append(p)
#
# 列表推导式写法（一行搞定）：
new_prices = [p * 0.8 if p > 100 else p for p in prices]
print(f"打折后价格：{new_prices}")

# ---- enumerate()：加序号打印 ----
# 把商品清单按编号打印出来
for i, price in enumerate(new_prices):
    print(f"商品 {i+1}：{price} 元")

# ---- 两个一起用：筛选 + 编号 ----
# 只列出打 8 折的商品（即降过价的）
discounted = [p for p in new_prices if p < 100]
print(f"\n实际打折的商品有 {len(discounted)} 个，降价后的价格：{discounted}")
for i, price in enumerate(discounted):
    print(f"  打折商品 {i+1}：{price} 元")

# ---- 进阶演示：用 enumerate 改造原列表 ----
# 给每个商品起个编号名
products = ["鼠标", "键盘", "显示器", "U盘", "耳机"]
for i, name in enumerate(products):
    products[i] = f"{i+1}. {name}"
print(f"\n编号后的商品列表：{products}")

# ---- enumerate 从指定数字开始 ----
for i, name in enumerate(products, start=1):
    print(f"第{i}个：{name}")
