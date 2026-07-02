# ================================================================
# 导入工具包
# 现实类比：开工前先把要用的工具摆上桌
# ================================================================

# requests：让 Python 能上网给大模型发消息，相当于"信使"
import requests

# os：让 Python 能和你的电脑文件系统对话（创建文件夹、拼接路径等）
import os

# json：把大模型返回的 JSON 字符串转成 Python 能用的字典
import json

# csv：把数据写进表格文件，方便你用 Excel 打开
import csv

# glob：按规则搜文件，比如"找出所有 .txt 结尾的文件"
import glob


# ================================================================
# 设置区 —— 把要用到的信息集中写在最前面，方便以后修改
# 现实类比：你在机器上贴了一张操作说明书，参数都写在这张纸上
# ================================================================

# API 地址：大模型服务的网址。
# DeepSeek、OpenAI 都提供一个网址让你去"敲门"，换别的模型改这里就行。
API_URL = "https://api.deepseek.com/chat/completions"

# 模型名字：告诉服务器你想用哪个大模型来干活。
MODEL_NAME = "deepseek-chat"

# API 密钥：相当于你的"通行证"或"门禁卡"。
# 从环境变量读取，这样就不会把密码写在代码里。
# 如果你不知道怎么设环境变量，也可以直接把密钥字符串写在引号里替换这行。
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "把你的API密钥写在这里")

# 系统提示词：告诉大模型"你是谁、该用什么身份来干活"。
# 就像你跟一个实习生说："你现在是资深文案，按这个要求来做事。"
SYSTEM_PROMPT = "你是一个资深的品牌文案，请提取以下内容的核心卖点，输出三条精简的短句"


# ================================================================
# 函数 ①：检查环境 —— raw_data 文件夹在不在？
# 现实类比：开工前先看一眼工具箱在不在，不在就去买一个
# ================================================================

def check_environment():
    """检查 raw_data 文件夹是否存在，不存在就创建并提示。"""

    # os.path.exists("raw_data") 就像你问电脑："这个文件夹存在吗？"
    if not os.path.exists("raw_data"):

        # os.makedirs() 相当于你在桌面右键 -> 新建文件夹，取名叫 raw_data
        os.makedirs("raw_data")

        print("=" * 55)
        print("  还没建 raw_data 文件夹，已经帮你自动创建好了。")
        print("  请往里面放入 .txt 格式的产品资料，然后重新运行脚本。")
        print("=" * 55)

        # exit() 让程序停在这里，等你放好文件再运行
        exit()
    else:
        print("  ✓ raw_data 文件夹已就绪，开始干活！\n")


# ================================================================
# 函数 ②：调用大模型 API
# 现实类比：你雇了一个 24 小时在线的品牌文案专家。
# 你把产品资料发给他，他按固定格式回你一段卖点文案。
# ================================================================

def call_api(text):
    """把文字发给大模型，返回 AI 写的卖点文案。失败返回 None。"""

    # 组装要发给大模型的消息。
    # 消息分两种角色：
    #   - system：给大模型定调子、下指令（相当于"老板交代任务"）
    #   - user：用户实际要处理的内容（相当于"老板给的原材料"）
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]

    # 把上面所有信息打包成一个"请求包"（字典），准备让信使送出去。
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,  # 控制创造力：0 最保守，1 最放飞
    }

    # 请求头（HTTP headers）：告诉服务器"我带的通行证是这个，请放行"。
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # 以下是"尝试做某事，如果翻车了就处理错误"的固定写法。
    try:
        # 让信使（requests）把请求包送到 API 地址，等回复。
        # timeout=60 意思是"最多等 60 秒，超时不候"。
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)

        # 检查服务器有没有报错（就像快递到了先看外包装有没有破损）。
        response.raise_for_status()

        # 把服务器的回复从"密文"变成 Python 能懂的"字典"（json 格式解析）。
        result = response.json()

        # 从层层包裹的回复中，把大模型真正写的那段话掏出来。
        # 字典结构是：result -> choices[0] -> message -> content
        ai_text = result["choices"][0]["message"]["content"]

        print("  ✓ AI 分析完成！")
        return ai_text

    # 以下是各种"翻车"情况的处理

    except requests.exceptions.Timeout:
        print("  ✗ 请求超时：AI 60 秒没响应，请检查网络或稍后重试")
        return None

    except requests.exceptions.RequestException as e:
        print(f"  ✗ 网络请求失败：{e}")
        return None


# ================================================================
# 函数 ③：处理所有文件 —— 遍历文件夹，逐个读、逐个调 AI
# 现实类比：打开文件夹，把里面的 .txt 文件一个一个拿出来，
# 每份都读一遍，然后交给 AI 专家分析。
# ================================================================

def process_files():
    """遍历 raw_data 下所有 .txt 文件，逐个读取并调用 AI 分析。"""

    # 检查（或创建）一个叫 results 的文件夹，用来存放处理结果。
    if not os.path.exists("results"):
        os.makedirs("results")

    # glob.glob 的意思是"按规则搜文件"。
    # "raw_data/*.txt" = "raw_data 文件夹下，所有以 .txt 结尾的文件"。
    # 这行代码会返回一个列表，里面装着每个文件的完整路径。
    txt_files = glob.glob("raw_data/*.txt")

    # 如果文件夹里一个 .txt 文件都没有，提醒用户然后结束。
    if not txt_files:
        print("  ⚠ raw_data 文件夹里没有 .txt 文件，请放入后再运行。")
        return [], []  # 返回两个空列表

    print(f"  📂 发现 {len(txt_files)} 个 .txt 文件，开始处理...\n")

    # 准备一个空篮子，用来装后面所有的分析结果（后面写 CSV 要用）。
    all_results = []

    # 准备一个空列表，记录每个文件对应的输出路径（方便最后汇总）。
    output_paths = []

    # for 循环：就像流水线传送带。
    # 传送带上一件一件地送来文件（file_path），你一件一件地处理。
    for file_path in txt_files:
        print(f"  📄 正在处理：{file_path}")

        # 打开文件，读取里面所有的文字。
        # with 语句的意思是"帮我打开文件，用完之后自动关掉，不用我手动 close"。
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 跳过内容全是空格或啥也没有的文件。
        if not content.strip():
            print("    ⚠ 文件内容为空，跳过")
            continue  # continue = 跳过当前这个，继续处理下一个

        # 调用 call_api 函数，把文字发给大模型，拿到卖点结果。
        ai_text = call_api(content)

        # 如果 AI 返回为空（翻车了），跳过这个文件。
        if not ai_text:
            print(f"    ❌ {file_path} 分析失败，跳过")
            continue

        # ------------------------------------------------------------
        # 生成输出文件名
        # os.path.basename 是"取文件名"的意思。
        # 比如从 "raw_data/产品A.txt" 中取出 "产品A.txt"。
        # os.path.splitext 是"拆文件名和扩展名"的意思。
        # 比如把 "产品A.txt" 拆成 ("产品A", ".txt")，[0] 取前半部分 "产品A"。
        # ------------------------------------------------------------
        base_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_name = f"{name_without_ext}_卖点.txt"
        output_path = os.path.join("results", output_name)

        # 把大模型返回的卖点文字写入新文件。
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ai_text)

        print(f"    ✅ 已保存: {output_path}")

        # 把这条记录装进篮子，后面用来生成汇总 CSV。
        all_results.append({
            "来源文件": base_name,
            "AI 生成的卖点": ai_text,
        })
        output_paths.append(output_path)

    return all_results, output_paths


# ================================================================
# 函数 ④：保存汇总 CSV
# 现实类比：把整理好的信息卡，逐行填进 Excel 表格
# ================================================================

def save_to_csv(results):
    """把所有 AI 分析结果汇总写入一个 CSV 文件。"""

    # 如果篮子是空的，就不用写表格了。
    if not results:
        print("\n  ⚠ 没有数据可保存，跳过 CSV 写入。")
        return

    # 最终产出的文件名——相当于你要交给老板的 Excel 表格。
    csv_filename = "summary.csv"

    # 表头：就像在 Excel 里先写好第一行。
    fieldnames = ["来源文件", "AI 生成的卖点"]

    print(f"\n  📊 正在生成汇总表格：{csv_filename}")

    # "w" = 写入模式，每次都新建文件（已有同名文件会被覆盖）。
    # newline="" 是写 CSV 的标准配置，防止多出空行。
    # encoding="utf-8-sig" 让 Excel 能正常显示中文。
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:

        # csv.DictWriter = 一个"表格填写助手"。
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 先写表头（第一行）。
        writer.writeheader()

        # 把每条数据写进表格的一行。
        for item in results:
            writer.writerow(item)

    print(f"  ✅ 成功写入 {len(results)} 条数据到 {csv_filename}")
    print(f"  📁 文件位置：{os.path.abspath(csv_filename)}")


# ================================================================
# 主程序入口 —— 按顺序执行 4 个步骤
# 现实类比：流水线的总开关，按顺序干活
# ================================================================

def main():
    """按顺序执行 4 个步骤。"""

    print()
    print("=" * 55)
    print("  产品卖点提取流水线 v2.0")
    print("  支持：逐个保存 + CSV 汇总")
    print("=" * 55)
    print()

    # 第 1 步：检查 raw_data 文件夹
    check_environment()

    # 第 2 + 3 步：读取所有文件，逐个调 AI 分析，保存到 results 文件夹
    results, output_paths = process_files()

    # 第 4 步：把全部结果汇总成一个 CSV 表格
    save_to_csv(results)

    # 打印最终汇总信息
    if output_paths:
        print(f"\n  ✅ 本次处理了 {len(output_paths)} 个文件")
        print(f"  📁 逐个保存的位置：results/ 文件夹")
        print(f"  📊 汇总表格：summary.csv")
    else:
        print("\n  ⚠ 没有文件被成功处理。")

    print("\n  🎉 搞定！\n")


# 这是 Python 程序的启动开关：
# 当运行这个 .py 文件时，Python 会从这里开始执行。
# if __name__ == "__main__" 的意思是"只有直接运行这个文件时才执行"，
# 如果别的文件把这脚本当工具包 import 进去，就不会自动跑 main()。
if __name__ == "__main__":
    main()
