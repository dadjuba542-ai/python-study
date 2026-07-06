# Python 学习笔记 — 列表推导式与 enumerate()

## 一、列表推导式

把一个 `for` 循环 + `append` 压缩成一行。

### 基础结构

```
[表达式  for 变量 in 列表]
[表达式  for 变量 in 列表  if 条件]
[值A  if 条件  else 值B  for 变量 in 列表]
```

从左到右读就是自然语言顺序：**"想要什么 → 从哪拿 → 筛掉谁"**

### 原理

```python
# 传统写法（3行）
new = []
for p in prices:
    new.append(p + 1)

# 推导式（1行）
new = [p + 1 for p in prices]
```

`[]` 相当于一个"自动收集篮"——每算出一个表达式，自动掉进篮子里，循环结束直接拿到完整列表。

### 与数学记法的对应

```
数学： { x²  |  x ∈ ℕ,  x > 10 }
Python：[x**2  for x in range(100)  if x > 10]

结构一致：表达式 → 变量来源 → 筛选条件
```

### 适用场景

| 适合 | 不适合 |
|---|---|
| 从旧列表造新列表 | 需要在循环里做多件事（打印+存文件等） |
| 一对一转换 | 只想改原列表，不需要新列表 |
| 筛选后转换 | |

## 二、enumerate() — 循环时自动编号

```python
for i, f in enumerate(fruits):
    print(f"{i+1}. {f}")
```

### 原理

`enumerate(fruits)` 把列表变成一系列**小对子**：

```
enumerate(["苹果", "香蕉", "橘子"])
→ (0, "苹果"), (1, "香蕉"), (2, "橘子")
   ↑ 编号         ↑ 原值
```

`for i, f in ...` 里的 `i, f` 是**解包**——Python 按位置自动把第 0 位给 `i`，第 1 位给 `f`。

### 按位置匹配，不按名字

```python
for a, b in enumerate(fruits):   # 换名字，效果一样
# a=0, b=苹果  a=1, b=香蕉  a=2, b=橘子
```

`enumerate` 永远按 **(编号, 值)** 的顺序给出，名字随便起。

### 指定起始编号

```python
for i, f in enumerate(fruits, start=1):
```

`start=1` 是**可选参数**（写名字指定，不写默认 0）。不是所有函数都有这种参数，每个函数在设计时定好了自己能接受哪些可选参数。

### enumerate + 推导式组合

```python
products = [f"{i+1}. {name}" for i, name in enumerate(products)]
```

## 三、字符串格式化 — 引号规则总结

```python
f"字符串列表：{str_numbers}"     # f + {} → 替换变量值
"字符串列表：str_numbers"        # 无 f → 原样打印
"字符串列表：{str_numbers}"      # 无 f + {} → 也是原样打印
f'字符串列表："{str_numbers}"'   # 外层单引号，内层双引号，变量替换
```

- `f` 前缀让 `{}` 生效，没 `f` 时 `{}` 只是普通文字
- `\n` 是换行符，无论有没有 `f` 都生效
- 要在字符串里写双引号，用单引号包外层

## 四、常见转换函数

| 写法 | 作用 | 例子 |
|---|---|---|
| `int(x)` | 转成整数 | `int("3")` → `3` |
| `str(x)` | 转成字符串 | `str(42)` → `"42"` |
| `float(x)` | 转成小数 | `float("3.14")` → `3.14` |
| `round(x, n)` | 四舍五入到 n 位小数 | `round(12.356, 1)` → `12.4` |

## 五、查函数说明的方法

忘了函数的参数时，终端直接查：

```bash
python3 -c "help(函数名)"
# 例：python3 -c "help(enumerate)"
```
