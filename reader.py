"""
reader.py —— 结构化卖点挖掘流水线

用法：
  1. 在当前目录放入 .txt 产品资料到 raw_data 文件夹
  2. 在 call_ai_api 函数里填上你的 API Key
  3. 终端运行：python3 reader.py
  4. 获得 final_selling_points.csv
"""

# os 模块：让 Python 能和你的电脑文件系统对话（创建文件夹、列出文件等）
import os

# json 模块：把 AI 返回的 JSON 字符串转成 Python 能用的字典
import json

# csv 模块：把数据写进表格文件，方便你用 Excel 打开
import csv

# requests 模块：让 Python 能上网给 AI 发消息
import requests


# ================================================================
# 第 1 步：前置检查
# 现实类比：你开工前先看一眼工具箱在不在，不在就去买一个
# ================================================================

def check_environment():
    """检查 raw_data 文件夹。不存在就创建并提示，然后退出。"""

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
# 第 2 步：AI 大脑封装
# 现实类比：你雇了一个 24 小时在线的大健康品牌专家。
# 你把产品资料发给他，他按固定格式回你一张信息卡。
# ================================================================

def call_ai_api(product_text):
    """把产品资料发给 AI，让它提取结构化数据。失败返回 None。"""

    # ---- ★ 必填：填入你的 API Key ----
    # API Key 相当于你的"会员卡号"，去 DeepSeek 官网注册后可在控制台找到
    API_KEY = "sk-your-api-key-here"

    # API 地址：AI 服务器的"门牌号"。想换别的接口改这里就行
    API_URL = "https://api.deepseek.com/v1/chat/completions"


    # 请求头：相当于寄快递时填的寄件人信息
    headers = {
        # "这是我的会员卡号，请放行"
        "Authorization": f"Bearer {API_KEY}",
        # "我发的内容是 JSON 格式"
        "Content-Type": "application/json",
    }


    # 消息体：相当于你给 AI 写的完整指令
    payload = {
        # 指定让哪个 AI 模型来干活
        "model": "deepseek-chat",
        "messages": [
            {
                # system 消息：给 AI 设定人设和行为规则
                # 相当于你告诉新员工："你是大健康专家，回复要用固定格式"
                "role": "system",
                "content": (
                    "你是一个大健康行业的资深品牌策划，请阅读产品资料，提取核心信息。"
                    "必须严格以 JSON 格式输出，包含三个键名：'产品名称'、'核心功效'、'适用人群'。"
                ),
            },
            {
                # user 消息：你真正想问的问题
                "role": "user",
                "content": f"请分析以下产品资料：\n\n{product_text}",
            },
        ],
        # response_format：强制 AI 返回 JSON，相当于告诉翻译"请说英文，不要说别的"
        "response_format": {"type": "json_object"},
        # temperature：数值越低，AI 越"老实"，越不会自由发挥
        "temperature": 0.3,
    }

    print("  → 正在呼叫 AI 大脑...")

    try:
        # requests.post()：把消息通过网线发到 AI 服务器，60 秒没回就不等了
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        # 检查 AI 服务器有没有报错，就像快递到了先看外包装有没有破损
        response.raise_for_status()

        # response.json()：把 AI 返回的 JSON 转成 Python 字典
        result = response.json()

        # 一层层"剥洋葱"，取到 AI 写的文字
        ai_message = result["choices"][0]["message"]["content"]

        # json.loads()：把 JSON 字符串正式转成 Python 字典
        structured_data = json.loads(ai_message)

        print("  ✓ AI 分析完成！")
        return structured_data

    # 以下是各种"翻车"情况的处理
    except requests.exceptions.Timeout:
        print("  ✗ 请求超时：AI 60 秒没响应，请检查网络或稍后重试")
        return None

    except requests.exceptions.RequestException as e:
        print(f"  ✗ 网络请求失败：{e}")
        return None

    except json.JSONDecodeError:
        print("  ✗ AI 返回的不是有效 JSON，请检查 API 连接或提示词")
        return None


# ================================================================
# 第 3 步：文件流水线
# 现实类比：你打开文件夹，把里面的 .txt 文件一个一个拿出来
# 读一遍，每份都交给 AI 专家分析。
# ================================================================

def process_files():
    """遍历 raw_data 下所有 .txt 文件，逐个读取并调用 AI 分析。"""

    # 准备一个空篮子，用来装后面所有的分析结果
    all_results = []

    # os.listdir("raw_data") = 打开文件夹，看看里面有哪些文件
    filenames = os.listdir("raw_data")

    # 从文件名列表里，只挑出以 .txt 结尾的那些
    txt_files = []
    for f in filenames:
        if f.endswith(".txt"):
            txt_files.append(f)

    # 如果文件夹里一个 .txt 文件都没有，提醒用户然后结束
    if not txt_files:
        print("  ⚠ raw_data 文件夹里没有 .txt 文件，请放入后再运行。")
        return all_results

    print(f"  📂 发现 {len(txt_files)} 个 .txt 文件，开始处理...\n")

    # for 循环：就像传送带，把文件名一个个送到你手上
    for filename in txt_files:
        print(f"  📄 正在处理：{filename}")

        # os.path.join() = 把文件夹路径和文件名拼成完整路径
        file_path = os.path.join("raw_data", filename)

        # open() 就像打开一本书，"r" 表示"只读，不修改"
        # encoding="utf-8" 是最通用的中文编码
        with open(file_path, "r", encoding="utf-8") as f:
            # .read() = 把整本书的内容一口气读完
            content = f.read()

        # 跳过内容全是空格或啥也没有的文件
        if not content.strip():
            print("    ⚠ 文件内容为空，跳过")
            # continue = 跳过当前这个，继续处理下一个文件
            continue

        # 把文件内容交给 AI 分析
        result = call_ai_api(content)

        if result:
            # 记下这个结果来自哪个文件，方便以后追溯
            result["来源文件"] = filename
            # append = 把结果放进篮子
            all_results.append(result)
            print(f"    ✅ {filename} 处理完成")
        else:
            print(f"    ❌ {filename} 分析失败，跳过")

    return all_results


# ================================================================
# 第 4 步：结构化保存
# 现实类比：把整理好的信息卡，逐行填进 Excel 表格
# ================================================================

def save_to_csv(results):
    """把 AI 分析结果写入 final_selling_points.csv。"""

    # 如果篮子是空的，就不用写表格了
    if not results:
        print("\n  ⚠ 没有数据可保存，跳过 CSV 写入。")
        return

    # 最终产出的文件名——相当于你要交给老板的 Excel 表格
    csv_filename = "final_selling_points.csv"

    # 表头：就像在 Excel 里先写好第一行
    fieldnames = ["产品名称", "核心功效", "适用人群", "来源文件"]

    print(f"  📊 正在写入表格：{csv_filename}")

    # "w" = 写入模式，每次都新建文件（已有同名文件会被覆盖）
    # newline="" 是写 CSV 的标准配置，防止多出空行
    # encoding="utf-8-sig" 让 Excel 能正常显示中文
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:

        # csv.DictWriter = 一个"表格填写助手"
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 先写表头（第一行）
        writer.writeheader()

        # enumerate() 给每条数据编号，start=1 表示从 1 开始
        for idx, item in enumerate(results, start=1):

            # writer.writerow() = 在表格里新开一行，填入数据
            # item.get("键名", "默认值")：如果这个键不存在，用"未知"代替
            writer.writerow({
                "产品名称": item.get("产品名称", "未知"),
                "核心功效": item.get("核心功效", "未知"),
                "适用人群": item.get("适用人群", "未知"),
                "来源文件": item.get("来源文件", "未知"),
            })

    # os.path.abspath() 显示文件的完整路径，方便你去文件夹里找到它
    print(f"  ✅ 成功写入 {len(results)} 条数据")
    print(f"  📁 文件位置：{os.path.abspath(csv_filename)}")


# ================================================================
# 主程序入口
# 现实类比：流水线的总开关，按顺序执行 4 个步骤
# ================================================================

def main():
    """按顺序执行 4 个步骤。"""

    print()
    print("=" * 55)
    print("  结构化卖点挖掘流水线 v1.0")
    print("=" * 55)
    print()

    # 第 1 步：检查 raw_data 文件夹
    check_environment()

    # 第 2 步 + 第 3 步：读文件并调 AI 分析
    results = process_files()

    # 第 4 步：把结果存成 CSV 表格
    save_to_csv(results)

    print("\n  🎉 搞定！打开 final_selling_points.csv 看看结果吧。\n")


# 这是 Python 程序的启动开关：
# 当运行这个 .py 文件时，从 main() 开始执行
if __name__ == "__main__":
    main()
