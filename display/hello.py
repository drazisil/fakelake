# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
report_name = "daily_engaged_users_range_2019-01-23_2019-02-22"
df = pd.read_csv('data/discourse/discourse_{}.csv'.format(report_name))
print(df)

# Get current size
fig_size = plt.rcParams["figure.figsize"]

# Prints: [8.0, 6.0]
print("Current size: ", fig_size)

# Set figure width to 12 and height to 9
fig_height = fig_size[1]
fig_width = 10 * len(df['date'])
# fig_size[0] = fig_width
# fig_size[1] = fig_height * 2
fig_size[0] = 50
fig_size[1] = 6
plt.rcParams["figure.figsize"] = fig_size

# objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(df['date']))
# performance = [10, 8, 6, 4, 2, 1]

plt.bar(y_pos, df['count'], align='center', alpha=0.5)
plt.xticks(df['count'], df['date'])
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()
