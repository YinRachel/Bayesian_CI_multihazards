import numpy as np

# 设置模拟参数
n_simulations = 100000
failures = 0

# 故障概率
p_A = 0.05
p_B = 0.10
p_C = 0.03

# 执行模拟
for _ in range(n_simulations):
    # 对每个组件进行故障检测
    fail_A = np.random.rand() < p_A
    fail_B = np.random.rand() < p_B
    fail_C = np.random.rand() < p_C
    
    # 系统失败判断
    if fail_A or fail_B or fail_C:
        failures += 1

# 计算系统失效的概率
system_failure_probability = failures / n_simulations

print(f"System Failure Probability: {system_failure_probability:.4f}")
