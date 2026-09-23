import os
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

ORDNER = os.path.dirname(os.path.abspath(__file__))
TOP_SPRUENGE = 3                    # markierte Sprünge pro Skin
MIN_ABSTAND = pd.Timedelta('30D')   # Sprünge pro Skin mindestens so weit auseinander
LUECKE = pd.Timedelta('2D')         # ab dieser Pause wird die Linie unterbrochen

# Daten laden
df = pd.read_csv(os.path.join(ORDNER, 'skinverlauf.csv'), encoding='unicode_escape')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp')


def groesste_spruenge(g):
    # Gleitender Median über 5 Messungen (~1 Std.) filtert einzelne Ausreißer-Angebote,
    # damit nur Preisänderungen zählen, die auch bestehen bleiben
    glatt = g['preis_eur'].rolling(5, center=True, min_periods=1).median()
    vorher = glatt.shift(1)
    spruenge = pd.DataFrame({
        'timestamp': g['timestamp'],
        'vorher': vorher,
        'nachher': glatt,
        'diff': glatt - vorher,
        'prozent': (glatt - vorher) / vorher * 100,
    })
    # Änderungen über eine Datenlücke hinweg sind keine Sprünge
    spruenge = spruenge[g['timestamp'].diff() < LUECKE].dropna()
    spruenge = spruenge.reindex(spruenge['prozent'].abs().sort_values(ascending=False).index)

    auswahl = []
    for _, s in spruenge.iterrows():
        if all(abs(s['timestamp'] - a['timestamp']) > MIN_ABSTAND for a in auswahl):
            auswahl.append(s)
        if len(auswahl) == TOP_SPRUENGE:
            break
    return auswahl


waffen = sorted(df['weapon'].unique())
spalten = 3
zeilen = -(-len(waffen) // spalten)
fig, axes = plt.subplots(zeilen, spalten, figsize=(20, 4.2 * zeilen), sharex=True)
axes = axes.flatten()
start, ende = df['timestamp'].min(), df['timestamp'].max()

print(f"{'Skin':50} {'Datum':16} {'vorher':>7} {'nachher':>7} {'Änderung':>14}")
for ax, waffe in zip(axes, waffen):
    g = df[df['weapon'] == waffe].reset_index(drop=True)

    # Linie bei Datenlücken unterbrechen statt gerade durchzuziehen
    x = g['timestamp'].copy()
    y = g['preis_eur'].astype(float).copy()
    luecken = x.diff() > LUECKE
    x_plot = pd.concat([x, x[luecken] - pd.Timedelta(seconds=1)]).sort_values()
    y_plot = y.reindex(x_plot.index)
    y_plot[x_plot.index.duplicated(keep='last')] = float('nan')
    ax.plot(x_plot.values, y_plot.values, color='#1f77b4', linewidth=0.6)

    for s in groesste_spruenge(g):
        farbe = '#2ca02c' if s['diff'] > 0 else '#d62728'
        ax.axvline(s['timestamp'], color=farbe, linewidth=0.8, alpha=0.5, linestyle='--')
        ax.plot(s['timestamp'], s['nachher'], 'o', color=farbe, markersize=5)
        ax.annotate(f"{s['diff']:+.0f} € ({s['prozent']:+.0f}%)\n{s['timestamp']:%d.%m.%y}",
                    xy=(s['timestamp'], s['nachher']), xytext=(6, 0), textcoords='offset points',
                    fontsize=8, color=farbe, fontweight='bold', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=farbe, alpha=0.85))
        print(f"{waffe[:50]:50} {s['timestamp']:%d.%m.%Y %H:%M} {s['vorher']:7.0f} {s['nachher']:7.0f} {s['diff']:+6.0f} € {s['prozent']:+5.0f}%")

    letzter = g.iloc[-1]
    ax.set_title(f"{waffe}\naktuell {letzter['preis_eur']} € ({letzter['timestamp']:%d.%m.%Y})", fontsize=10)
    ax.set_ylabel("Preis in Euro")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(start, ende)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.tick_params(axis='x', labelbottom=True, labelrotation=45, labelsize=8)

for ax in axes[len(waffen):]:
    ax.set_visible(False)

fig.suptitle(f"Preisverlauf CS:GO Skins ({start:%d.%m.%Y} – {ende:%d.%m.%Y}), "
             f"markiert: die {TOP_SPRUENGE} größten Sprünge pro Skin", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(ORDNER, 'graph.png'), dpi=150)
plt.show()
