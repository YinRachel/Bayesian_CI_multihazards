import pandas as pd

# 创建一个简单的 DataFrame
df = pd.DataFrame(columns=['A', 'B'])

# 尝试追加一行
df = df.append({'A': 1, 'B': 2}, ignore_index=True)

# 打印结果来验证
print(df)