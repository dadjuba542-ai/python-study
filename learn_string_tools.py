# ================================================================
# 教学脚本：字符串工具箱
# 现实类比：你有一把瑞士军刀，专治各种文字处理
# ================================================================

print("=" * 55)
print("字符串工具箱 —— 处理文字的各种方法")
print("=" * 55)

# ================================================================
# 第一部分：切分与合并
# .split() = 按某个符号，把一句话切成列表
# .join()  = 把列表里的东西，用某个符号粘成一句话
# ================================================================

print("\n【第一部分：切分与合并】")

# ---- .split()：按指定符号切开 ----
sentence = "AI播客,AI宝儿,AI视频,咖啡灌肠"
print(f"原始字符串：{sentence}")

# .split(",") = 遇到逗号就切一刀，返回一个列表
items = sentence.split(",")
print(f"按逗号切开：{items}")

# .split() 不传参数时，按空白字符（空格/换行/制表符）切
text = "苹果  香蕉   橘子"
print(f"\n按空白切：'{text}'.split() → {text.split()}")

# ---- .join()：反过来，把列表粘成字符串 ----
fruits = ["苹果", "香蕉", "橘子"]

# " glue ".join(列表) = 用 glue 当胶水，把列表每一项粘起来
result = " | ".join(fruits)
print(f"\n列表：{fruits}")
print(f"用 '|' 粘起来：'{result}'")

# 常用技巧：列表转成逗号分隔的字符串
tags = ["Python", "教程", "编程"]
csv_line = ",".join(tags)
print(f"转成 CSV 一行：'{csv_line}'")

# ================================================================
# 第二部分：查找与判断
# .find()  = 找某个字在不在字符串里，在就返回位置
# .startswith() = 是不是以 XXX 开头
# .endswith()   = 是不是以 XXX 结尾
# .count()      = 数一数某个字出现几次
# ================================================================

print("\n【第二部分：查找与判断】")

filename = "学习笔记_2026-07-06_列表推导式与enumerate.md"

# ---- .endswith()：判断文件类型 ----
is_md = filename.endswith(".md")
print(f"文件名：{filename}")
print(f"是 .md 文件吗？{is_md}")

# ---- .startswith()：判断开头 ----
is_note = filename.startswith("学习笔记")
print(f"是学习笔记吗？{is_note}")

# ---- .find()：查找位置，找不到返回 -1 ----
pos = filename.find("2026")
print(f"'2026' 出现在第 {pos} 个位置")

# ---- .count()：统计出现次数 ----
count = filename.count("-")
print(f"文件名里有 {count} 个 '-'")

# ---- 筛选文件的应用场景 ----
files = [
    "周报_7月.md",
    "产品资料.txt",
    "周报_8月.md",
    "会议记录.txt",
    "周报_9月.md",
]

print("\n--- 场景：筛选出所有周报文件 ---")
# 配合列表推导式，一行筛选出所有周报
weekly = [f for f in files if f.startswith("周报") and f.endswith(".md")]
print(f"所有文件：{files}")
print(f"周报列表：{weekly}")

# ================================================================
# 第三部分：替换与清理
# .replace() = 把 A 替换成 B
# .strip()   = 去掉首尾多余的空格或符号
# .removeprefix() / .removesuffix() = 去掉开头或结尾的特定文字
# ================================================================

print("\n【第三部分：替换与清理】")

# ---- .replace()：替换 ----
original = "AI播客-第3期-2026-07-06"
print(f"原始：{original}")

# .replace("旧", "新") = 把"旧"替换成"新"
cleaned = original.replace("-", "_")
print(f"把 '-' 换成 '_'：{cleaned}")

# 连续替换：先把年去掉，再把月日去掉
simple = original.replace("-2026", "").replace("-07", "")
print(f"去掉日期：{simple}")

# ---- .strip()：去首尾空白 ----
messy = "   《咖啡灌肠史》视频脚本  \n  "
print(f"\n有空格和换行的文字：'{messy}'")
print(f"去掉首尾空白后：'{messy.strip()}'")

# ---- .removeprefix() / .removesuffix()：去掉前缀/后缀 ----
url = "https://github.com/dadjuba542-ai/python-study"
print(f"\nURL：{url}")
print(f"去掉 https://：{url.removeprefix('https://')}")
print(f"去掉仓库名：{url.removesuffix('python-study')}")

# ================================================================
# 第四部分：切片 —— 从字符串里取一段
# 语法：字符串[起始:结束:步长]
# 现实类比：从一箱水果里，只拿第 2 到第 5 个
# ================================================================

print("\n【第四部分：切片】")

text = "ABCDEFGHIJK"
print(f"原始：{text}")
print(f"text[2:5]  （第 2 到第 5，不包括第 5）：'{text[2:5]}'")
print(f"text[:5]   （从开头到第 5）：'{text[:5]}'")
print(f"text[5:]   （从第 5 到末尾）：'{text[5:]}'")

# ---- 应用：从文件名取日期 ----
filename = "学习笔记_2026-07-06_列表推导式与enumerate.md"
# 先找到第一个数字的位置，再取 10 位（YYYY-MM-DD）
start = filename.find("2026")
date_part = filename[start:start+10]
print(f"\n从文件名取日期：{date_part}")

# ---- 应用：提取文件扩展名 ----
def get_extension(filename):
    """取文件后缀名"""
    dot_pos = filename.rfind(".")  # rfind = 从右边开始找
    return filename[dot_pos:]     # 从点号取到最后

print(f"后缀名：{get_extension('周报_7月.md')}")
print(f"后缀名：{get_extension('产品资料.txt')}")
print(f"后缀名：{get_extension('image.png')}")

# ================================================================
# 第五部分：组合实战 —— 解析周报文件名
# ================================================================

print("\n【第五部分：组合实战 —— 解析周报文件名】")

reports = [
    "周报_2026-07-06_AI播客.md",
    "周报_2026-07-06_AI宝儿.txt",
    "周报_2026-07-06_AI视频.md",
]

print("文件名拆解：")

for f in reports:
    # 1. 去掉 .md 或 .txt
    name = f.rsplit(".", 1)[0]     # rsplit = 从右边切，只切1刀
    # 2. 按 _ 切分
    parts = name.split("_")
    # 3. 取各个部分
    date = parts[1]
    project = parts[2]
    ext = f.split(".")[-1]
    print(f"  · 项目：{project} ｜ 日期：{date} ｜ 格式：{ext}")

# ================================================================
# 速查表
# ================================================================

print("\n" + "=" * 55)
print("字符串方法速查表")
print("=" * 55)
print("""
  .split("符号")    → 按符号切分成列表
  "胶水".join(列表)  → 用胶水把列表粘成字符串
  .find("文字")     → 查找文字位置（找不到返回 -1）
  .startswith("X")  → 是否以 X 开头
  .endswith("X")    → 是否以 X 结尾
  .count("X")       → X 出现几次
  .replace("旧","新") → 把旧文字替换成新文字
  .strip()          → 去掉首尾空白
  .removeprefix("X") → 去掉开头的 X
  .removesuffix("X") → 去掉结尾的 X
  字符串[起点:终点]  → 切取中间一段
  字符串[起点:终点:步长] → 跳着取
""")
