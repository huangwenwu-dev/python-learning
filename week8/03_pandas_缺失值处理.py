import pandas as pd

df = pd.read_csv("week8/sales.csv")
print(df)
print(df.isnull())              #  返回一张同样大小的True/False表(True是缺失) 
print(df.isnull().sum())        #  统计每列有多少个缺失值 
print(df.info())                #  名字、类型有没有空值 

print(df.isnull().sum())
print(df.dropna())                #  删除含有 "任何缺失值" 的行
print(df.isnull().sum())
df = df.dropna(subset=["销量"])   # 只以"销量"是否缺失为准，删掉整行(接住返回值覆盖 df)  
print(df)
print(df.isnull().sum())

df["产品"] = df["产品"].fillna("未知")      # 文本列填占位词(接住返回值覆盖)
df["地区"] = df["地区"].fillna("未知")      # 文本列填占位词(接住返回值覆盖)
print(df)
print(df.isnull().sum())                    # 单价剩 1 —— 有意留的,不是漏了
print(df["销量"].sum())                     # 720.0,NaN 在隔壁列,碍不着