# requests 是用来帮 Python 上网发消息的库，相当于"信使"。
# 等下要靠它把文字发给大模型，再把大模型回的答案带回来。
import requests

# os 模块可以读取电脑上的环境变量，用来安全地拿 API 密钥，不把密码写在代码里。
# 后面还要用它操作文件路径（取文件名、拼接路径）。
import os

# glob 是"全局查找"的意思，它可以帮你按规则搜文件。
# 比如让你一键找出 raw_data 文件夹下所有 .txt 文件。
import glob

# ------------------------------------------------------------
# 设置：API 信息（只设置一次，后面循环复用）
# ------------------------------------------------------------

# API 地址：大模型服务的网址。
API_URL = "https://api.deepseek.com/chat/completions"

# 模型名字：告诉服务器你想用哪个大模型来干活。
MODEL_NAME = "deepseek-chat"

# API 密钥：相当于你的"通行证"或"门禁卡"。
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "把你的API密钥写在这里")

# 系统提示词：告诉大模型"你是谁、该用什么身份来干活"。
SYSTEM_PROMPT = "你是一个资深的品牌文案，请提取以下内容的核心卖点，输出三条精简的短句"


# ------------------------------------------------------------
# 定义函数：把"调用 API"这件事打包成一个叫 call_api 的工具
# 以后每次要调用大模型，只要说 call_api(文字) 就行了，不用重复写一堆代码。
# def 是 define（定义）的缩写，意思是"我在定义一个函数/工具"。
# text 是"要发给大模型的原材料"。
# return 是"把结果送回来"。
# ------------------------------------------------------------
def call_api(text):
    # 组装要发给大模型的消息。
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]

    # 把上面所有信息打包成一个"请求包"（字典），准备让信使送出去。
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
    }

    # 请求头：告诉服务器"我带的通行证是这个，请放行"。
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # 让信使（requests）把请求包送到 API 地址，等回复。
    response = requests.post(API_URL, json=payload, headers=headers)

    # 把服务器的回复从"密文"变成 Python 能懂的"字典"。
    result = response.json()

    # 从层层包裹的回复中，把大模型真正写的那段话掏出来，然后返回。
    return result["choices"][0]["message"]["content"]


# ------------------------------------------------------------
# 主流程：遍历文件夹 + 循环处理
# ------------------------------------------------------------

# 检查当前目录下有没有叫 raw_data 的文件夹。
# exists 就是"存在吗"的意思，not exists 就是"不存在"。
if not os.path.exists("raw_data"):
    # 如果 raw_data 文件夹不存在，就在屏幕上提醒用户，然后退出程序。
    print("错误：当前目录下没有找到 raw_data 文件夹，请先创建它。")
    exit()

# 检查（或创建）一个叫 results 的文件夹，用来存放处理结果。
# makedirs 就是"创建多层目录"的意思。
if not os.path.exists("results"):
    os.makedirs("results")

# glob.glob 的意思是"按规则搜文件"。
# "raw_data/*.txt" 的意思是"raw_data 文件夹下，所有以 .txt 结尾的文件"。
# 这行代码会返回一个列表，里面装着每个文件的完整路径。
txt_files = glob.glob("raw_data/*.txt")

# 检查有没有找到任何 .txt 文件。
if not txt_files:
    print("raw_data 文件夹里没有找到任何 .txt 文件。")
    exit()

# for 循环：就像流水线传送带。
# 传送带上一件一件地送来文件（file_path），你一件一件地处理。
# "for 变量 in 列表" = "从列表里挨个取出每个东西，给变量，然后干活"。
for file_path in txt_files:
    # 在屏幕上打印当前正在处理哪个文件，让你知道进度。
    print(f"\n===== 正在处理: {file_path} =====")

    # 打开文件，读取里面所有的文字。
    # with 语句的意思是"帮我打开文件，用完之后自动关掉，不用我手动 close"。
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 把读到的内容打印到屏幕上，让你看一眼原材料。
    print(f"原文内容：\n{content}")

    # 调用刚才定义好的 call_api 函数，把文字发给大模型，拿到卖点结果。
    ai_text = call_api(content)

    # 把大模型返回的结果也打印到屏幕上。
    print(f"\nAI 生成的卖点：\n{ai_text}")

    # ------------------------------------------------------------
    # 生成输出文件名
    # ------------------------------------------------------------

    # os.path.basename 是"取文件名"的意思。
    # 比如从 "raw_data/产品A.txt" 中取出 "产品A.txt"。
    base_name = os.path.basename(file_path)

    # os.path.splitext 是"拆文件名和扩展名"的意思。
    # 比如把 "产品A.txt" 拆成 ("产品A", ".txt")，[0] 取前半部分 "产品A"。
    name_without_ext = os.path.splitext(base_name)[0]

    # 用 f-string 拼接出新文件名："产品A_卖点.txt"
    output_name = f"{name_without_ext}_卖点.txt"

    # os.path.join 是"拼接路径"的意思，不管 Windows 还是 Mac，它都能拼对分隔符。
    # 结果是 "results/产品A_卖点.txt"
    output_path = os.path.join("results", output_name)

    # 把大模型返回的卖点文字写入新文件。
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ai_text)

    # 在屏幕上告诉你文件已经存好了。
    print(f"已保存: {output_path}")

# for 循环结束后，打印一条汇总信息。
print("\n===== 全部处理完毕！=====")
