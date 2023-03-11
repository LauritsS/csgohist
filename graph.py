import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv('C:/Users/Maurits/Desktop/GIT Project/csgohist/skinverlauf.csv', encoding= 'unicode_escape')
print(df)

ax = sns.lineplot(x="timestamp", y="preis_eur", hue='weapon', data=df)
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

plt.show()