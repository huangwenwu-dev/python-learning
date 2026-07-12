import pandas as pd

df = pd.read_csv("week8/clean_sales.csv")
# CSV 不存类型，read_csv 后日期会变回文本，必须重转 
df["下单日期"] = pd.to_datetime(df["下单日期"])

print(df.info())
print(df["销量"].sum())
# 按「地区」进行分组然后计算每个地区的销量总和
print(df.groupby("地区")["销量"].sum())

# 从「下单日期」中提取月份并创建新列「月份」
df["月份"] = df["下单日期"].dt.month
# 打印查看新增月份列是否正确
print(df)
# 创建新列「销售额」: 销售额 = 商品价格 × 销售数量
df["销售额"] = df["价格"] * df["销量"]
# 查看每条订单对应的销售金额
print(df["销售额"])

# 坑：sort_values 默认升序，找 Top 必须 ascending=False
print(df.groupby("地区")["销售额"].sum().sort_values(ascending=False).head(3))
# 按地区统计销售情况求和、求求平均、计数
print(df.groupby("地区")["销售额"].agg(["sum", "mean", "count"]))
# 按月份分组计算每个月的销售总额
print(df.groupby("月份")["销售额"].sum())
