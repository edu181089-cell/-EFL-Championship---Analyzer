import sqlite3
import matplotlib.pyplot as plt

# Connect to your existing database
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'championship_database.sqlite'))
cur = conn.cursor()

# Get standings ordered from bottom to top
cur.execute("SELECT team, points, position FROM Standings WHERE season = '2025' ORDER BY points ASC, position DESC")
rows = cur.fetchall()

teams = [row[0] for row in rows]
points = [row[1] for row in rows]
positions = [row[2] for row in rows]

# Color by position
total_teams = len(teams)
colors = []
for i in range(len(teams)):
    pos = positions[i]
    if pos <= 2:
        colors.append('green')
    elif pos <= 6:
        colors.append('lightgreen')
    elif pos >= 22:
        colors.append('red')
    else:
        colors.append('steelblue')

# Shorten team names for readability
teams = [t.replace(' FC', '').replace(' AFC', '').replace(' City', ' C.') for t in teams]

# Create the chart
fig, ax = plt.subplots(figsize=(12, 10))

min_bar = 0.3
visual_points = [max(p, min_bar) for p in points]
bars = ax.barh(teams, visual_points, color=colors)

# Set x axis to always show 0 to at least 10 so early season looks clean
max_points = max(visual_points) if max(visual_points) > 10 else 10
ax.set_xlim(0, max_points + 3)

ax.set_xlabel('Points', labelpad=10)
ax.set_title('EFL Championship 2025/26 Final Standings', pad=15)

# Add point values at end of each bar
for i, v in enumerate(points):
    display_val = str(v)
    bar_end = max(v, 0.3)
    ax.text(bar_end + 0.2, i, display_val, va='center', fontsize=9)

# Add legend
from matplotlib.patches import Patch
legend = [
    Patch(color='green', label='Automatic Promotion'),
    Patch(color='lightgreen', label='Playoff Places'),
    Patch(color='steelblue', label='Mid Table'),
    Patch(color='red', label='Relegation Zone')
]
ax.legend(handles=legend, loc='lower right')

plt.tight_layout()
plt.savefig('championship_standings.png', dpi=150, bbox_inches='tight')
plt.show()

print('Chart saved!')
conn.close()