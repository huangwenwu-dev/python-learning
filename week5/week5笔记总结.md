# 第五周笔记：文件读写 + JSON

## 📁 本周文件清单
| 文件 | 练的是什么 |
|------|-----------|
| 01_read_读文件.py | "r"模式 read/readline/readlines区别 |
| 02_write_写文件.py | "w"/"a"模式区别 |
| 03_日志记录器.py | 文件读写基础 |
| 04_dict和json互转.py | dict"活对象" json"文本字符串" |
| 05_dump和load互转.py | 带s=string(字符串) 不带s=对文件 |
| 06_健壮的配置读取.py| 读文件不存在异常--FileNotFoundError  文件在内容不合法JSON--json.JSONDecodeError |
| 07_待办清单.py | JSON持久化 + 增删查 |

## 一、文件模式速查（我要吃透的）
| 模式 | 作用 | 关键点 |
|------|------|--------|
| 'r'  | 读文件 | 要带encoding='utf8',中文防乱码  |
| 'w'  | 写文件 | ⚠️ 会清空原文件（open 那一刻就空了） |
| 'a'  | 写文件 | 比如写日志,往后面追加内容  |
- `with open(...)`：为什么用？→ (自动关闭文件)
- 中文防乱码：必须带 `encoding='utf8'`
- `read()` 返回整段字符串/ `readline()` 当前这一行,读一行，光标往下走一格/ `readlines()`返回列表
- `write()` 的坑：→ (\n换行)

## 二、JSON 四方法速查（重点，连未来）
| 方法 | 对象（字符串/文件） | 方向 | 用途 |
|------|------|------|------|
| dumps | 字符串 | 想法→文字 | dict存进config.json |
| loads | 字符串 | 文字→想法 | config.json读回dict |
| dump  | 文件 | 内存→文件 | dict存进config.json |
| load  | 文件 | 文件→内存 | config.json读回dict |
- 记忆法：带 s = 字符串；不带 s = 对文件
- JSON vs dict 本质区别：→ ("文字" vs "活对象"；key 必须双引号；true/false/null)
- 中文 JSON 必加参数：`ensure_ascii=False`

## 三、本周踩坑记录（写我真踩过的）
- 中文乱码 → encoding='utf8'
- `'w'` 误覆盖 → 文件内容都清空
- `write` 不换行 → 字符串都挤在一起
- `dump` / `dumps` 搞混 → 带s对字符串, 不带s对文件
- 读不存在的 JSON 文件 → 会遇到哪两个异常？(FileNotFoundError, json.JSONDecodeError)，处理策略差在哪？(FileNotFoundError:config = Person 之后,用 'w' 把默认值 dump 进文件。JSONDecodeError:config = Person 之后就停)
- （你之前真踩过的：`for` 循环里放 `pop`/`input`、用 `"True"` 字符串 → 也写进来）

## 四、回头补的盲区
- 暂无