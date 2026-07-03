"""
daily_work_log.py —— 每日工作记录 + 周报生成器

用法：
  手动记录：      python3 daily_work_log.py
  查看已有记录：  python3 daily_work_log.py report
  从 Obsidian 扫： python3 daily_work_log.py obsidian
"""

import os
import json
import sys
from datetime import datetime, date, timedelta


# 数据文件：所有记录都存在这个文件里
DATA_FILE = "work_log.json"


def load_records():
    """从文件里读取已有的记录。如果文件不存在，返回空列表。"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_records(records):
    """把记录列表保存到文件。"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_record():
    """记录模式：问你几个问题，存一条新记录。"""

    print("\n📝 记录今天的工作")
    print("-" * 30)

    # 日期自动填今天的，不用你输入
    today = date.today().isoformat()

    # input() = 在终端停下来，等你打字，回车确认
    project = input("项目名称（如 AI播客、AI宝儿、AI视频）: ")
    content = input("今天做了什么: ")
    status = input("状态（完成 / 进行中 / 计划）: ")

    record = {
        "日期": today,
        "项目": project,
        "内容": content,
        "状态": status,
    }

    records = load_records()
    records.append(record)
    save_records(records)

    print(f"\n✅ 已记录：{project} — {content}")


def generate_report():
    """周报模式：读出所有记录，按项目归类，打印周报。"""

    records = load_records()

    if not records:
        print("\n⚠ 还没有任何记录，先运行 python3 daily_work_log.py 添加记录吧。")
        return

    print("\n📊 周报汇总")
    print("=" * 40)

    # 从所有记录里，收集所有出现过的项目名称，去重
    # set 是 Python 的"集合"，自动去重
    project_names = set()
    for r in records:
        project_names.add(r["项目"])

    # 按项目逐个输出
    for name in sorted(project_names):
        print(f"\n【{name}】")

        # 只筛选出当前这个项目的记录
        for r in records:
            if r["项目"] == name:
                print(f"  · {r['日期']} | {r['内容']} | {r['状态']}")

    print("\n" + "=" * 40)
    print(f"共 {len(records)} 条记录，{len(project_names)} 个项目")


# ================================================================
# Obsidian 扫描模式
# 现实类比：不用你手动打字，脚本自己去你的 Obsidian 日记文件夹
# 翻出这周写了啥，帮你整理成周报
# ================================================================

# 你的 Obsidian 日记文件夹路径
# expanduser 会把 ~ 自动替换成你的用户目录 /Users/test
OBSIDIAN_PATH = os.path.expanduser("~/Documents/知识库/日记文档/工作相关/")


def get_this_week():
    """计算本周的周一和周日，返回两个日期。"""

    # .today() 拿今天的日期，.weekday() 返回星期几（周一是 0，周日是 6）
    today = date.today()

    # 周一 = 今天的日期 减去 今天距离周一差几天
    # 比如今天周三，weekday() = 2，就减 2 天，回到周一
    monday = today - timedelta(days=today.weekday())

    # 周日 = 周一 + 6 天
    sunday = monday + timedelta(days=6)

    return monday, sunday


def scan_obsidian():
    """从 Obsidian 日记文件夹里读取本周的笔记，生成周报。"""

    monday, sunday = get_this_week()

    print(f"\n📖 正在扫描 Obsidian 日记…（本周 {monday} ~ {sunday}）")
    print("-" * 55)

    # os.listdir() = 打开文件夹，列出所有文件
    all_files = os.listdir(OBSIDIAN_PATH)

    # 只保留 .md 结尾的文件
    md_files = []
    for f in all_files:
        if f.endswith(".md"):
            md_files.append(f)

    if not md_files:
        print("  ⚠ 日记文件夹里没有找到 .md 文件")
        return

    # 存放本周的笔记，按日期排序
    weekly_notes = []

    for filename in md_files:
        file_path = os.path.join(OBSIDIAN_PATH, filename)

        # os.path.getmtime() = 获取文件的"最后修改时间"
        # 返回的是一个时间戳（秒数），用 fromtimestamp 转成日期
        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        modified_date = modified_time.date()

        # os.path.getctime() = 获取文件的"创建时间"
        created_time = datetime.fromtimestamp(os.path.getctime(file_path))
        created_date = created_time.date()

        # 如果文件是本周创建或修改的，就纳入周报
        # 这样既包括本周刚写的日记，也包括本周更新过的旧文件
        is_this_week = (monday <= modified_date <= sunday) or (monday <= created_date <= sunday)

        if is_this_week:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            weekly_notes.append({
                "文件名": filename,
                "修改时间": modified_date,
                "内容": content.strip(),
            })

    # 如果没有找到本周的笔记
    if not weekly_notes:
        print("  ⚠ 这周还没有写过日记笔记")
        return

    # 按修改时间从早到晚排序
    # sort 的 key 参数告诉 Python："按修改时间来排，别按文件名排"
    weekly_notes.sort(key=lambda x: x["修改时间"])

    print(f"\n📊 本周共有 {len(weekly_notes)} 篇日记\n")

    # 逐个打印本周的笔记
    for note in weekly_notes:
        print(f"【{note['文件名']}】（{note['修改时间']}）")
        print(note["内容"])
        print("-" * 55)


def main():
    """入口：根据命令参数选择模式。"""

    # sys.argv 是"运行脚本时带的参数"
    # python3 daily_work_log.py               → sys.argv = ["daily_work_log.py"]
    # python3 daily_work_log.py report         → sys.argv = ["daily_work_log.py", "report"]
    # python3 daily_work_log.py obsidian       → sys.argv = ["daily_work_log.py", "obsidian"]
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        generate_report()
    elif len(sys.argv) > 1 and sys.argv[1] == "obsidian":
        scan_obsidian()
    else:
        add_record()


if __name__ == "__main__":
    main()
