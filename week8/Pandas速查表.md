# Pandas 速查表

## 一、读取与查看
```python
pd.read_csv("x.csv", encoding="utf-8")   # 读取 CSV；乱码/报错 → 换 "gbk" 或 "utf-8-sig"
df.head() / df.tail()                    # 看前几行 / 后几行
df.shape                                 # 看行数和列数
df.info()                                # 看字段、非空数量、数据类型
                                         # ← 本周最重要的体检项：缺失值 + dtype
df.describe()                            # 数值列统计摘要：均值/标准差/最值/分位数
```

## 二、选择与筛选
```python
df["列"]                                 # 选一列（返回 Series）
df[["列1","列2"]]                        # 选多列（返回 DataFrame，双括号 = 传列表）
df.loc[行, "列名"]                       # 按标签 / 名字
df.iloc[行, 列]                          # 按位置 / 下标
df[df["销量"] > 100]                     # 布尔筛选
df[(条件1) & (条件2)]                    # ⚠️ 组合条件，每个条件必须加括号
```

## 三、清洗（⚠️ 铁律：清洗方法要接住返回值）
```python
df.isnull().sum()                        # 查每列缺多少
df = df.dropna(subset=["列"])            # subset= 只根据指定列是否缺失来删行
df["列"] = df["列"].fillna(值)           # ⚠️ 填充 = 制造数据，会影响均值/总和/结论
df = df.drop_duplicates(subset=["列"])   # 按指定列去重，默认保留第一条
                                         # 注意：duplicated() 查重复，drop_duplicates() 删重复，别混
df["列"] = df["列"].astype(int)          # ⚠️ 转之前必须先清干净：缺失值、空格、杂字符
df["日期"] = pd.to_datetime(df["日期"])  # 日期不用 astype；会解析格式，失败变 NaT
df["列"] = df["列"].str.strip()          # ⚠️ 空格看不见，但匹配/分组/去重全会出错
df = df.rename(columns={"旧":"新"})      # ⚠️ 改名后，后面的代码要用新列名（否则 KeyError）
```

## 四、分组聚合与排序
```python
df["月份"] = df["日期"].dt.month                    # ⚠️ 日期列必须先 to_datetime，否则 .dt 报错
月销售额 = df.groupby("月份")["销售额"].sum()       # 对应 SQL 的 GROUP BY
                                                    # ⚠️ 返回的是 Series，分组列变成了索引
月销售额.sort_values(ascending=False)               # ⚠️ Series 排序不写列名！写了 → KeyError
df.groupby("列")["列"].agg(["sum","mean"])          # 一次算多个统计量
df.sort_values("列", ascending=False).head(3)       # Top N ⚠️ 默认是升序
df["新列"] = df["列A"] * df["列B"]                  # 新增计算列
```

## 五、绘图
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']    # 解决中文显示（不设 → 全是方框）
plt.rcParams['axes.unicode_minus'] = False      # 解决负号显示
plt.plot(x, y, label="...")
plt.title() / plt.xlabel() / plt.ylabel() / plt.legend()
plt.show()                                      # ⚠️ 不写它，脚本里图不显示
```

## 六、我要记牢的三条（自己的话）

- **清洗方法要接住返回值**
  → 很多 Pandas 方法不改原表，只返回一张新表。
    **不赋值，清洗就等于没发生。**

- **删还是填，怎么判断**
  → 问的不是"这列重不重要"，而是：
    **这个缺失值会不会参与后面的运算？会怎样影响运算结果？**
    （备注不参与运算 → 缺 75% 也不管；SALES 要 astype → 必须管）

- **不报错的坑，比报错的坑可怕**
  → 空格没去掉 → `"北京"` 和 `"北京 "` 被 groupby 当成**两个不同的组**
  → `mean()` 遇到 NaN → 不报错，非空值之和 ÷ 非空值个数，**悄悄算出另一个平均数**
  → 忘了 `ascending=False` → 拿到的是**最小的几个**，代码不报错、图照样画

## 七、承前启后（清洗 → RAG）

清洗数据，是为了让 RAG 检索到的资料**准确、完整、格式统一**；
否则模型会基于脏数据，给出**看似合理、实际错误**的答案——
而且它不会告诉你数据脏了，它会很自信。

> 一句话：**RAG 的效果上限，由喂进去的数据质量决定。**
> 所以「洗数据」不是数据分析选修课，是 **Agent 开发的必修前置**。