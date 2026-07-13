import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

import pandas as pd
df = pd.read_csv("week8/clean_sales.csv")
df["下单日期"] = pd.to_datetime(df["下单日期"])

df["月份"] = df["下单日期"].dt.month
df["销售额"] = df["价格"] * df["销量"]
月销售额 = df.groupby("月份")["销售额"].sum()
print(月销售额)
print(df.groupby("月份")["销售额"].agg(["sum", "mean", "count"]))

plt.plot(月销售额.index, 月销售额.values)
plt.title("月销售额对比")
plt.xlabel("月份")
plt.ylabel("销售额")
plt.show()


# ============ 数据结论 ============
# （2月总额比1月跌77%左右，单量4 → 1，客单价基本持平，业绩趋势下跌
#  也可能数据样本太少，不足以下定论。3月因缺失销量被删，无有效数据）