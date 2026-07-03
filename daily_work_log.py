"""
daily_work_log.py —— 每日工作记录 + 周报生成器

用法：
  手动记录：      python3 daily_work_log.py
  查看已有记录：  python3 daily_work_log.py report
  从 Obsidian 扫： python3 daily_work_log.py obsidian
"""

# os 模块：和电脑文件系统打交道（找文件、查修改时间、拼接路径）
import os

# json 模块：把数据存成 JSON 文件，或者从 JSON 文件读回来
import json

# sys 模块：读取运行脚本时输入的命令行参数（比如 report、obsidian）
import sys

# datetime 模块：获取当前日期时间、计算本周范围、转文件时间戳
from datetime import datetime, date, timedelta


# ================================================================
# 数据读写 —— 相当于准备一个抽屉，用来存和取每天的记录
# ================================================================

# 数据文件的名字。所有记录都存在这个文件里
DATA_FILE = "work_log.json"


def load_records():
    """从文件里读取已有的记录。如果文件不存在，返回空列表。"""
    try:
        # 尝试打开 work_log.json 文件，用只读模式 "r"
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            # json.load() = 把文件里的 JSON 内容转成 Python 列表
            return json.load(f)
    except FileNotFoundError:
        # 如果文件不存在（第一次运行），返回一个空列表
        return []


def save_records(records):
    """把记录列表保存到文件。"""
    # "w" = 覆盖写入模式，每次保存都会重写整个文件
    # ensure_ascii=False 保证中文正常显示，indent=2 让文件格式好看
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # json.dump() = 把 Python 列表转成 JSON 字符串，写入文件
        json.dump(records, f, ensure_ascii=False, indent=2)


# ================================================================
# 模式 1：手动记录
# 现实类比：在终端里回答几个问题，脚本帮你存下来
# ================================================================

def add_record():
    """记录模式：问你几个问题，存一条新记录。"""

    print("\n📝 记录今天的工作")
    print("-" * 30)

    # 日期是自动填的，不用你输入
    # .today() 拿今天的日期，.isoformat() 转成 "2026-07-03" 这种格式
    today = date.today().isoformat()

    # input() = 在终端停下来，等你打字，按回车键确认
    # 你输入的内容会存到等号左边的变量里
    project = input("项目名称（如 AI播客、AI宝儿、AI视频）: ")
    content = input("今天做了什么: ")
    status = input("状态（完成 / 进行中 / 计划）: ")

    # 把刚才输入的内容，打包成一个字典（相当于一张信息卡）
    record = {
        "日期": today,
        "项目": project,
        "内容": content,
        "状态": status,
    }

    # 先读取出已有的所有记录
    records = load_records()
    # 把新记录追加到列表末尾
    records.append(record)
    # 把更新后的列表存回文件
    save_records(records)

    print(f"\n✅ 已记录：{project} — {content}")


# ================================================================
# 模式 2：查看周报
# 现实类比：把之前存的所有记录读出来，按项目分组，打印给你看
# ================================================================

def generate_report():
    """周报模式：读出所有记录，按项目归类，打印周报。"""

    # 从文件里读出所有记录
    records = load_records()

    # 如果一条记录都没有，提醒用户先去记录
    if not records:
        print("\n⚠ 还没有任何记录，先运行 python3 daily_work_log.py 添加记录吧。")
        return

    print("\n📊 周报汇总")
    print("=" * 40)

    # 准备一个"集合"（set），用来装所有出现过的项目名字
    # set 的特点是：往里加重复的东西，它自动只保留一个
    project_names = set()

    # 遍历每一条记录，把它的项目名加入集合
    for r in records:
        project_names.add(r["项目"])

    # sorted() 把项目名按拼音排序，逐个输出
    for name in sorted(project_names):
        print(f"\n【{name}】")

        # 再遍历一次所有记录，只挑出属于当前这个项目的
        for r in records:
            if r["项目"] == name:
                # 打印：日期 | 内容 | 状态
                print(f"  · {r['日期']} | {r['内容']} | {r['状态']}")

    print("\n" + "=" * 40)
    # len() 数一数列里有多少条记录和多少个项目
    print(f"共 {len(records)} 条记录，{len(project_names)} 个项目")


# ================================================================
# 模式 3：从 Obsidian 扫描周报
# 现实类比：不用你手动输入，脚本自己去你的 Obsidian 日记文件夹里
# 翻出这周写了什么，直接展示给你看
# ================================================================

# 你的 Obsidian 日记文件夹路径
# expanduser 会自动把 ~ 替换成你的用户目录 /Users/test
OBSIDIAN_PATH = os.path.expanduser("~/Documents/知识库/日记文档/工作相关/")


def get_this_week():
    """计算本周的周一和周日，返回两个日期。"""

    # 获取今天的日期
    today = date.today()

    # .weekday() 返回今天是星期几，周一是 0，周日是 6
    # 比如今天周三，weekday() = 2，就减 2 天，回到周一
    monday = today - timedelta(days=today.weekday())

    # 周日 = 周一 + 6 天
    sunday = monday + timedelta(days=6)

    # 把周一和周日两个日期一起返回
    return monday, sunday


def scan_obsidian():
    """从 Obsidian 日记文件夹里读取本周的笔记，生成周报。"""

    # 拿到本周的周一和周日
    monday, sunday = get_this_week()

    print(f"\n📖 正在扫描 Obsidian 日记…（本周 {monday} ~ {sunday}）")
    print("-" * 55)

    # os.listdir() = 打开文件夹，列出里面的所有文件
    all_files = os.listdir(OBSIDIAN_PATH)

    # 只保留以 .md 结尾的文件，跳过其他文件
    md_files = []
    for f in all_files:
        if f.endswith(".md"):
            md_files.append(f)

    # 如果一个 .md 文件都没找到，提醒然后结束
    if not md_files:
        print("  ⚠ 日记文件夹里没有找到 .md 文件")
        return

    # 准备一个空列表，用来存放本周的笔记
    weekly_notes = []

    # 遍历每个 .md 文件，检查是不是本周的
    for filename in md_files:
        # os.path.join() = 把文件夹路径和文件名拼成完整路径
        file_path = os.path.join(OBSIDIAN_PATH, filename)

        # os.path.getmtime() = 获取文件的"最后修改时间"
        # 返回的是一个时间戳（秒数），用 fromtimestamp 转成年月日
        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        modified_date = modified_time.date()

        # os.path.getctime() = 获取文件的"创建时间"
        created_time = datetime.fromtimestamp(os.path.getctime(file_path))
        created_date = created_time.date()

        # 判断：修改时间或创建时间，只要有一个在本周范围内就算
        # 这样既包括本周新写的日记，也包括本周更新过的旧文件
        is_this_week = (monday <= modified_date <= sunday) or (monday <= created_date <= sunday)

        # 如果是本周的，就读出内容，存到列表里
        if is_this_week:
            # 打开文件，读取内容，"r" = 只读
            with open(file_path, "r", encoding="utf-8") as f:
                # .read() = 把文件内容全部读出来
                content = f.read()

            # 把文件名、修改时间、内容打包成一个字典，加入列表
            weekly_notes.append({
                "文件名": filename,
                "修改时间": modified_date,
                "内容": content.strip(),
            })

    # 如果一条本周的笔记都没找到
    if not weekly_notes:
        print("  ⚠ 这周还没有写过日记笔记")
        return

    # 按修改时间从早到晚排序
    # .sort() 是列表自带的排序功能
    # key=lambda x: x["修改时间"] 告诉 Python："按'修改时间'这个字段来排"
    weekly_notes.sort(key=lambda x: x["修改时间"])

    print(f"\n📊 本周共有 {len(weekly_notes)} 篇日记\n")

    # 逐个打印本周的笔记
    for note in weekly_notes:
        # 【文件名】（日期）
        print(f"【{note['文件名']}】（{note['修改时间']}）")
        # 笔记的具体内容
        print(note["内容"])
        # 一条分割线
        print("-" * 55)


# ================================================================
# 主程序入口 —— 流水线的总开关
# ================================================================

def main():
    """入口：根据命令参数选择模式。"""

    # sys.argv 是 Python 自动收集的"命令行参数"列表
    # 第一个参数永远是脚本自己的文件名
    # python3 daily_work_log.py               → sys.argv = ["daily_work_log.py"]
    # python3 daily_work_log.py report         → sys.argv = ["daily_work_log.py", "report"]
    # python3 daily_work_log.py obsidian       → sys.argv = ["daily_work_log.py", "obsidian"]

    # len(sys.argv) > 1 判断用户有没有输入额外的参数
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        generate_report()
    elif len(sys.argv) > 1 and sys.argv[1] == "obsidian":
        scan_obsidian()
    else:
        # 默认模式：没有输入参数，或者参数不认识，就走手动记录
        add_record()


# 启动开关：只有直接运行这个文件时才执行 main()
if __name__ == "__main__":
    main()
