import pandas as pd                     # 社区惯例缩写pd

data = {                                # 用字典建 DataFrame
    "日期": ["4月", "5月", "6月"],
    "地区": ["江西", "深圳", "浙江"],
    "产品": ["苹果", "香蕉", "西瓜"],
    "销量": [20, 30, 25]
    }
df = pd.DataFrame(data)                 # 字典转成表
print(df)
print(df["地区"])                       # 取一列
df.to_csv("week8/sales.csv", index=False)       # 存 CSV
df2 = pd.read_csv("week8/sales.csv")            # 读 CSV
print(df2)
print(df2.dtypes)                               # 看每列类型