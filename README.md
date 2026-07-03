# Python Study

Python 零基础学习仓库。

## 仓库信息

- **远端地址**：`https://github.com/dadjuba542-ai/python-study.git`
- **克隆到本地**：`git clone https://github.com/dadjuba542-ai/python-study.git`

## 文件说明

| 文件 | 说明 |
|---|---|
| `reader.py` | 批量读取 raw_data 文件夹 → 调 AI 提取卖点 → 逐个保存到 results/ + CSV 汇总 |
| `daily_work_log.py` | 工作日志：手动记周报 / 自动扫 Obsidian 日记 |
| `demo_list_enum.py` | 列表推导式 + enumerate() 演示案例 |
| `学习笔记_2026-07-02.md` | 7 月 2 日学习笔记 |
| `学习笔记_2026-07-03.md` | 7 月 3 日学习笔记（含 demo 知识点） |

## 常用命令

```bash
git pull origin main        # 拉取远端最新代码
git add .                   # 暂存所有修改
git commit -m "描述修改"     # 提交
git push origin main        # 推送
```

## 知识点速查

### 列表推导式
从列表生成新列表，一行搞定 for + append：
```python
[p * 0.8 for p in prices if p > 100]
# 等价于：
# new = []
# for p in prices:
#     if p > 100:
#         new.append(p * 0.8)
```

### enumerate()
循环时同时拿到"第几个"和"值"：
```python
for i, name in enumerate(["a", "b", "c"]):
    print(i, name)          # 0 a / 1 b / 2 c
for i, name in enumerate(..., start=1):  # 从1开始编号
```

### strip()
去掉字符串首尾空白：
```python
"  你好  ".strip()  →  "你好"
```

### set() 集合
自动去重：
```python
s = set()
s.add("A"); s.add("A")  # {"A"}，只保留一个
```

### sorted() 排序
```python
sorted(["B", "A", "C"])  # ["A", "B", "C"]
```

### glob 文件搜索
```python
glob.glob("文件夹/*.txt")  # 找出所有 .txt 文件
```
`*` = 任意文件名。

### lambda 临时函数
```python
列表.sort(key=lambda x: x["字段"])  # 按指定字段排序
```

### 日期操作
```python
from datetime import date, timedelta
today = date.today()
monday = today - timedelta(days=today.weekday())  # 本周一
```

### with open 自动关文件
```python
with open("文件", "r") as f:
    content = f.read()
# 缩进结束自动 close()
```

### API 调用模板
```python
headers = {"Authorization": "Bearer 密钥", "Content-Type": "application/json"}
payload = {"model": "模型名", "messages": [{"role": "user", "content": "内容"}]}
response = requests.post(API_URL, json=payload, headers=headers)
result = response.json()["choices"][0]["message"]["content"]
```

### 函数分而治之
```
main()
  ├─ check_environment()
  ├─ process_files()
  │    ├─ call_api()
  │    └─ ...
  └─ save_to_csv()
```
大问题拆小问题，每个函数只管一件事。
