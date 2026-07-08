# 🗄️ SQL 命令速查表

## 〇、Python 操作 sqlite3（五步套路）
- `conn = sqlite3.connect("x.db")` — 连接数据库（文件不存在就新建这个 .db）
- `cur = conn.cursor()` — 拿到游标，用它执行 SQL
- `cur.execute("SQL", (值,))` — 执行；用 ? 占位、值单独传，参数化防 SQL 注入
- `conn.commit()` — 增删改后必须，否则数据不落盘
- `conn.close()` — 关闭连接

## 一、建表（CREATE TABLE）
- `CREATE TABLE 表名 (字段 类型 约束, ...);` — 建表
- 类型：`INTEGER`（int）/ `TEXT`（str）/ `REAL`（float）
- 约束：`PRIMARY KEY` — 主键 ／ `NOT NULL` — 非空 ／ `AUTOINCREMENT` — 自增
- ⚠️ 每个字段内部用空格，字段之间用逗号，最后一个字段后不加逗号

## 二、增删改查（CRUD）
- `INSERT INTO 表名 (字段...) VALUES (值...);` — 增；自增 id 不用填
- `SELECT 字段 FROM 表名 WHERE 条件 ORDER BY 字段 [DESC] LIMIT n;` — 查
   （判断相等用 1个 =）
- `UPDATE 表名 SET 字段=值 WHERE 条件=?;` — 改
- `DELETE FROM 表名 WHERE 条件=?;` — 删

## 三、聚合 + 分组
- `SELECT AVG/COUNT/MAX/MIN/SUM(字段) FROM 表名;` — 汇总成一个值
- `SELECT 分组字段, AVG(字段) FROM 表名 GROUP BY subject;` — 按字段分组统计
   （"全班平均" vs "各科平均" 差的就是这个关键词）

## 四、多表 JOIN
- `SELECT 表A.字段, 表B.字段 FROM 表A INNER JOIN 表B ON 表A.关联字段 = 表B.关联字段;`
   （靠什么把两表关联起来？→ 外键）
- 为什么拆多张表：防数据冗余,浪费空间；外键是：别人的主键

## 五、我的三条红线（写清楚"为什么"）
- UPDATE/DELETE 必带 WHERE → 因为不带修改/删除整个表, 不可逆
- 增删改后必 commit → 否则数据不保存
- 查询用 ? 参数化 → 规避SQL注入风险

## 六、常见报错排查（我踩过的坑）
（用你笔记里"现象 / 原因 / 修复"的格式，从上面那串真实的坑里挑几个写）
- 现象：参数化查询里,元组占位没有替换成真实值(误写成 (?, ?) 而不是实际值) ／ 原因：字符串里的 ? 是占位符,元组里对应位置要填真实数据 ／ 修复：先写好SQL占位骨架,再逐个把元组里的 ? 换成变量或字面值
- ...