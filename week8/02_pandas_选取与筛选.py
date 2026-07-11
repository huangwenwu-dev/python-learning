import pandas as pd

df2 = pd.read_csv("week8/sales.csv")        #  读 CSV 
print(df2.head())                           #  看前五行 
print(df2.tail())                           #  看后五行
print(df2.shape)                            #  看几行几列
print(df2.info())                           #  名字、类型有没有空值 
print(df2.describe())                       #  对数字列自动计算

print(df2["地区"])                          
a = df2["地区"]                             #  取一列 
print(type(a))                             #  返回Series
print(df2[["地区", "销量"]])
s = df2[["地区", "销量"]]                   #  取多列    
print(type(s))                             #  返回DataErame 

print(df2.iloc[1, 2])                       #  按位置取、取第2行销量 
print(df2.iloc[0: 3])                       #  取前三行(顾头不顾尾) 
print(df2.loc[1, "销量"])                   #  按标签取、取第2行销量 

print(df2["销量"] > 100)                    #  产生一列True/False 
print(df2[df2["销量"] > 100])               #  用True/False筛行 
print(df2[(df2["销量"] > 100) & (df2["地区"] == "北京")])   #  销量 > 100 且在北京(布尔筛选) 