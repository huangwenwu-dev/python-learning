# 第一周笔记：Python 基础

## 📁 本周文件清单
| 文件 | 练的是什么 |
|------|-----------|
| 01_hello_第一个程序.py | 第一行代码：print |
| 02_变量_数据类型.py | 变量、type、f-string、input、类型转换 |
| 03_列表.py | list 的 append/remove/遍历 |
| 04_字典.py | dict 增删改查、items 遍历 |
| 05_条件判断.py | if/elif/else、逻辑运算 or |
| 06_while循环.py | while/break、猜数字(固定答案版) |
| 07_综合_猜数字游戏.py | random+continue+防呆(capstone) |

## 一、基础语法速查（我要吃透的）
- 四种数据类型：`int` / `float` / `str` / `bool`；类型转换 `int()` / `str()` / `float()`
- 字符串：拼接、f-string `f"我叫{name}"`
- 列表：索引从 **0** 开始、切片 `[1:3]`（不含 3）、`append` / `remove`、`len()`
- 字典：键值对、增删改查、遍历
- 条件：比较运算符、`and` / `or` / `not`、`if` / `elif` / `else`
- 循环：`for` + `range()`、`while`、`break` / `continue`
- 综合：猜数字游戏（`import random`、`randint`）

## 二、关键直觉（一句话记牢）
- 变量 = 贴了标签的盒子，标签（名字）指向里面的值
- 列表是"有编号的格子"，编号从 0 开始；字典是"查字典"，用键找值
- `input()` 拿到的**永远是字符串**，要算数先 `int()` 转
- `range()` / 切片**不含**上界，`randint(1,100)` **两端都含**

## 三、本周踩坑记录
- 装 Python 忘勾 "Add to PATH" → 终端找不到 `python` 命令
- `=`（赋值）和 `==`（判断）写混
- `input()` 没转 `int()` 就拿去做算术 → 报错
- `if` / `for` / `while` 后忘冒号 `:` 或忘缩进

## 四、回头补的盲区
- 暂无 —— 基础语法已跑通（猜数字游戏能独立写出即过关）