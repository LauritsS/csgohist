import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Daten laden
df = pd.read_csv('C:/Users/Maurits/Desktop/GIT Project/csgohist/skinverlauf.csv', encoding= 'unicode_escape')
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Finden des letzten Wertes für jede Waffe
last_vals = df.groupby('weapon').tail(1)

# Berechnen der Sprünge
df['prev_val'] = df.groupby('weapon')['preis_eur'].shift(1)
df['jump'] = (df['preis_eur'] - df['prev_val']).abs()
df['threshold'] = df['preis_eur'] * 0.04  # 3.5% Schwankung

# Markieren der Sprünge, die größer als der Schwellenwert sind
df['jump_highlight'] = df['jump'] > df['threshold']

# Plot erstellen
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize=(12, 8))
sns.lineplot(x="timestamp", y="preis_eur", hue='weapon', data=df, ax=ax, palette="bright", linewidth=2.5, alpha=0.8)

# Annotationen hinzufügen
for i, row in last_vals.iterrows():
    ax.annotate(row['preis_eur'], xy=(row['timestamp'], row['preis_eur']), xytext=(10, 10), textcoords='offset points', fontsize=10, color='black')

# Markieren der Sprünge im Plot
for i, row in df[df['jump_highlight']].iterrows():
    ax.annotate(round(row['jump'], 2), xy=(row['timestamp'], row['preis_eur']), xytext=(10, -20), textcoords='offset points', fontsize=10, color='black', arrowprops=dict(arrowstyle='-|>', lw=1, color='black', alpha=0.8))

# X-Achsenbeschriftungen anpassen
ticks = df[df['jump_highlight']]['timestamp'].tolist()
ax.set_xticks(ticks)
ax.set_xticklabels(ticks, rotation=45, ha='right')

# Achsenbeschriftungen und Titel
plt.xlabel("Datum")
plt.ylabel("Preis in Euro")
plt.title("Preisverlauf von CS:GO Waffenskins")

# Legende aus dem Plot ziehen und separat platzieren
legend = ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., prop={'size': 8})
legend.set_title("Legende")

# Layout optimieren
plt.tight_layout()

# Plot anzeigen
plt.show()