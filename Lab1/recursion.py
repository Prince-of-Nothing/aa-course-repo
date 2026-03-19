import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Naive Fibonacci (no memoization)
def nth_fibonacci(n):
    if n <= 1:
        return n
    return nth_fibonacci(n - 1) + nth_fibonacci(n - 2)

# Large Fibonacci values to compute
n_values = [20, 25, 30, 35, 40] 
execution_times = []

for n in n_values:
    start_time = time.time()
    nth_fibonacci(n)
    end_time = time.time()
    execution_times.append(end_time - start_time)

# Table display
table_data = np.zeros((1, len(n_values)))
table_data[0, :] = execution_times

df = pd.DataFrame(table_data, columns=n_values)
df.index = ["Execution Time"]

print(df)

# Plot performance graph
plt.figure(figsize=(10, 5))
plt.plot(n_values, execution_times, marker='o', linestyle='-')
plt.xlabel("Fibonacci Number (n)")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time of Naive Recursive Fibonacci")
plt.grid(True)
plt.show()