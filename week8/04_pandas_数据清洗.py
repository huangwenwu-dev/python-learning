import pandas as pd

df = pd.read_csv("week8/dirty_data.csv")

# 1. 去重
df = df.drop_duplicates(subset=["订单号"])
print("去重后:", len(df))

# 2. 去空格 / 杂字符
df["地区"] = df["地区"].str.strip()
df["SALES"] = df["SALES"].str.replace("元", "")
print(df["地区"].unique())

# 3. 处理缺失
df = df.dropna(subset=["SALES"])            
df["价格"] = df["价格"].fillna(df["价格"].mean())       # 价格缺失,填平均价

# 4. 转类型
df["SALES"] = df["SALES"].astype(int)
df["下单日期"] = pd.to_datetime(df["下单日期"])

# 5. 改列名
df = df.rename(columns={"SALES": "销量"})

# 6. 复检
print(df)
print(df.info())
print(df.isnull().sum())
print(df.duplicated().sum())

df.to_csv("week8/clean_sales.csv", index=False)     #  干净数据复制到clean_sales.csv