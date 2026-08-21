import sqlite3
import matplotlib.pyplot as plt
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
plt.savefig(os.path.join(BASE_DIR, 'Championship 2025-2026 final standings.png'), dpi=150, bbox_inches='tight')
plt.show()
print('Standings chart saved!')

# -------------------------
# CHART 2 - HOME VS AWAY WINS PER TEAM
# -------------------------

cur.execute("""
    SELECT 
        team,
        SUM(home_wins) as home_wins,
        SUM(away_wins) as away_wins,
        SUM(draws) as draws
    FROM (
        -- Home matches
        SELECT 
            home_team as team,
            SUM(CASE WHEN result = 'HOME_TEAM' THEN 1 ELSE 0 END) as home_wins,
            0 as away_wins,
            SUM(CASE WHEN result = 'DRAW' THEN 1 ELSE 0 END) as draws
        FROM Matches
        GROUP BY home_team
        
        UNION ALL
        
        -- Away matches
        SELECT 
            away_team as team,
            0 as home_wins,
            SUM(CASE WHEN result = 'AWAY_TEAM' THEN 1 ELSE 0 END) as away_wins,
            0 as draws
        FROM Matches
        GROUP BY away_team
    )
    GROUP BY team
    ORDER BY home_wins DESC
""")
rows = cur.fetchall()

teams2 = [row[0].replace(' FC', '').replace(' AFC', '').replace(' City', ' C.') for row in rows]
home_wins = [row[1] for row in rows]
away_wins = [row[2] for row in rows]
draws = [row[3] for row in rows]

import numpy as np
x = np.arange(len(teams2))
width = 0.25

fig2, ax2 = plt.subplots(figsize=(14, 7))

ax2.bar(x - width, home_wins, width, label='Home Wins', color='steelblue')
ax2.bar(x, away_wins, width, label='Away Wins', color='orange')
ax2.bar(x + width, draws, width, label='Draws', color='lightgray')

ax2.set_xlabel('Team')
ax2.set_ylabel('Number of matches')
plt.savefig(os.path.join(BASE_DIR, 'championship_home_away.png'), dpi=150, bbox_inches='tight')
ax2.set_xticks(x)
ax2.set_xticklabels(teams2, rotation=45, ha='right', fontsize=8)
ax2.legend()

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'championship_home_away.png'), dpi=150, bbox_inches='tight')
plt.show()
print('Home/Away chart saved!')

conn.close()