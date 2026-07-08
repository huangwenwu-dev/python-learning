# 第六周笔记：[SQLite 数据库入门]

## 📁 本周文件清单
| 文件 | 练的是什么 |
|------|-----------|
| school.db | Day1：手动建的第一个库+表（students）|
| school.db | Day2: 手写SQL建 scores 表 + 练 INSERT/NOT NULL|
| scores.db | Day3: (INSERT)和查(SELECT)|
| scores.db | Day4: (UPDATE/修改)、(DELETE/删除)、聚合函数
| students.db | Day5: 建 students+scores 两表、INNER JOIN 关联查询 |
| student_scores.db | Day6: 完整CRUD+AVG+参数化查询(学生成绩库) |
| 01_学生成绩库.py | Day6: 完整CRUD+平均分+参数化查询实战 |
| 07_xxx.py | |

## 一、[本周核心知识点A] 速查（我要吃透的）
| 维度 | 文件/JSON | 数据库 |
|---|---|---|
| 查询 | 自己写循环逐条筛, 慢| 一句SQL查出来, 快|
| 关系 | 多类数据关联很乱 | 表与表能清晰关联 |
| 适用场景| 数据少, 结构简单 | 数据量大或关系复杂 |
| 类型 | 存什么 | 例子 | 对应Python |
|---|---|---|---|
| INTEGER | 整数 | id、年龄 | int |
| TEXT | 字符串/文本 | 姓名/科目名 | str |
| REAL | 小数(浮点数) | 身高、分数85.5 | float |
| 关键词 | 作用 | 形状 | 易错点 |
|---|---|---|---|
| INSERT INTO | 插数据 | INSERT INTO 表 (字段...) VALUES (值...); | id不填, 文本要引号 |
| SELECT | 查数据 | SELECT 字段 FROM 表; | *查全部 |
| WHERE | 筛选 | ... WHERE 条件; | 相等用单个 =，别写 == |
| ORDER BY | 排序 | ... ORDER BY 字段 [DESC];| 默认从低到高, 带DESC从高到低 |
| LIMIT | 取前几条 | ... LIMIT | 放最后 |
| 关键词 | 作用 | 形状 | 易错点 |
|---|---|---|---|
| UPDATE | 改已有数据 | `UPDATE 表 SET 字段=新值 WHERE 条件;` | 忘加WHERE会改全表 |
| DELETE | 删整行 | `DELETE FROM 表 WHERE 条件;` | 忘加WHERE会删全表；删的是整行不是某个值 |
| COUNT/AVG/MAX/MIN/SUM | 对一整列做统计，汇总成一个数 | `SELECT AVG(字段) FROM 表;` | 和"逐行查"不是一回事，是"整列算一个数" |
| GROUP BY | 按字段分组，每组分别统计 | `SELECT 字段, AVG(x) FROM 表 GROUP BY 字段;` | GROUP BY后SELECT里乱加字段（只能放分组字段+聚合函数）|
| 外键(FK) | 一表指向另一表主键的字段 | 关联两表 | `scores.student_id` 指向 `students.id` |
| INNER JOIN | 把两表按关联字段拼起来查 | 一次查出跨表信息 | `FROM A INNER JOIN B ON A.id=B.a_id` |
| 表名.字段 | 指明字段来自哪张表 | 避免同名字段混淆 | `students.name`,`scores.score` |
| 维度 | 语法 | 易错点 |
|---|---|---|
| 建表跳过重复 | `CREATE TABLE IF NOT EXISTS 表 (...)` | 不加这个，脚本跑第二次就报table already exists |
| 建表逗号规则 | 字段名 类型, 字段名 类型, 字段名 类型 | 名字和类型间是空格不是逗号；最后一个字段后不加逗号 |
| 插入(带占位) | `INSERT INTO 表 (字段1,字段2) VALUES (?, ?)` | 后面execute第二参数是元组，别把?原样抄进去 |
| 单值元组 | `(值,)` | 漏逗号就不是元组，是普通括号 |
| 改数据 | `UPDATE 表 SET 字段=? WHERE 条件=?` | 忘WHERE=改全表 |
| 删数据 | `DELETE FROM 表 WHERE 条件=?` | 忘WHERE=删全表，最危险 |
| 平均分 | `SELECT AVG(字段) FROM 表` | 配fetchone()[0]取数值，别用fetchall包一层列表 |
| 取单条结果 | `cursor.fetchone()` | 返回一个元组，如(91.5,)，取值要用索引[0] |
| 取多条结果 | `cursor.fetchall()` | 返回列表，每行是元组，配for遍历+索引取字段 |


## 二、[本周核心知识点B] 速查（重点，连未来）
| 概念 | 是什么 | Python类比 |
|---|---|---|
| 表(table) | 存一类数据 | 像一个装字典的列表 |
| 行(row) | 一条完整记录 | 像一个字典{"id":1,"name":"小明"} |
| 列(column) | 一个字段，类型固定 | 像所有字典里同一个key |
| 主键(primary key) | 每行唯一身份证，通常是id | 作用：能精确区分和增删改某一行 |
| 自增(AUTOINCREMENT) | id自动编号，省心不重复 | 写成 INTEGER PRIMARY KEY AUTOINCREMENT |
| 非空(NOT NULL) | 该字段插入时必须有值 | 写在"类型后面"：name TEXT NOT NULL |
| 聚合函数 | 把一整列汇总成一个数 | AVG(score) 算全班平均分 | 对应手写 sum(list)/len(list) |
| GROUP BY | 先按某字段"归堆"，再对每堆分别统计 | 按subject分组算各科平均分 | 对应手写按key分桶后分别算 |
| 数据冗余 | 一张表塞太多导致重复信息 | 像把班级通讯录和成绩单硬拼一张纸 |
| 外键(foreign key) | 存的是"别人家的主键" | 像身份证号出现在另一张登记表里,用来指认是谁 |
| JOIN 的本质 | 拿一张表的编号,去另一张表里找对应行 | 拿成绩表的"几号",去学生表里查"几号是谁" |
| 概念 | 是什么 | 作用 |
|---|---|---|
| 五步套路 | Python操作数据库固定顺序 | connect→cursor→execute→commit→close，缺一步就出错 |
| commit时机 | 提交对应哪次改动 | INSERT/UPDATE/DELETE各自跑完都单独commit，别攒到最后一起提交 |
| 参数化查询的本质 | ?占位+元组传值 | 防SQL注入，尤其涉及用户input()时是硬性要求，不能拼字符串 |
| WHERE的本质 | 限定操作作用范围的条件 | UPDATE/DELETE没WHERE=对表里每一行都执行，等于全表改/全表删 |
| 建表幂等性 | 建表这个动作理论上只该发生一次 | 脚本可能被重复运行，但CREATE TABLE不能重复执行，需要IF NOT EXISTS或跑完注释掉 |
| fetchone vs fetchall | 单条结果 vs 多条结果 | 按需选择：查一条(如按姓名查/AVG)用fetchone更简洁；查多条(遍历全表)用fetchall |


## 三、本周踩坑记录（写我真踩过的）
- （Day_ 踩的坑）→ 现象/原因/解决
- Day3: 分别写了 WHERE 一句、ORDER BY 一句，结果里数据全冒出来了/两句是独立的, 结果区只显示第1条的结果/两句SQL合成一句
- 
- 
- 

## 四、回头补的盲区
- （每天没搞懂的，当天先记一行，周末再回来啃）

## 五、承前启后（连未来）
- 这周的 ___ 将来用在 ___（开周写猜想，周末修正）