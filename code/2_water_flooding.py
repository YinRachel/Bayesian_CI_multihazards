import numpy as np
import matplotlib.pyplot as plt

# 模拟参数
n_simulations = 10000
system_capacity = 1000  # 系统的最大容量，单位可以是立方米水/天
demand_mean = 800       # 平均需求量
demand_std = 100        # 需求量的标准差
flood_mean = 100        # 平均洪水增加量
flood_std = 50          # 洪水增加量的标准差
failure_count = 0

# 进行模拟
for _ in range(n_simulations):
    demand = np.random.normal(demand_mean, demand_std)
    flood = np.random.normal(flood_mean, flood_std) if np.random.rand() < 0.1 else 0  # 假设有10%的概率发生洪水
    
    total_demand = demand + flood
    if total_demand > system_capacity:
        failure_count += 1

# 计算失败的概率
failure_probability = failure_count / n_simulations

print(f"Failure Probability: {failure_probability:.4f}")
plt.hist(total_demand, bins=50, alpha=0.75)
plt.title('Total Demand Distribution')
plt.xlabel('Total Water Demand (incl. Flood)')
plt.ylabel('Frequency')
plt.show()
