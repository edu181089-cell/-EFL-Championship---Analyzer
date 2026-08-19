import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'championship_database.sqlite'))
cur = conn.cursor()

# 2025/26 Championship Final Standings
# (position, team, season, played, won, drawn, lost, goals_for, goals_against, goal_difference, points)
standings_2025 = [
    (1, 'Coventry City FC', '2025', 46, 28, 11, 7, 97, 45, 52, 95),
    (2, 'Ipswich Town FC', '2025', 46, 23, 15, 8, 80, 47, 33, 84),
    (3, 'Millwall FC', '2025', 46, 24, 11, 11, 64, 49, 15, 83),
    (4, 'Southampton FC', '2025', 46, 22, 14, 10, 82, 56, 26, 80),
    (5, 'Middlesbrough FC', '2025', 46, 22, 14, 10, 72, 47, 25, 80),
    (6, 'Hull City AFC', '2025', 46, 21, 10, 15, 70, 66, 4, 73),
    (7, 'Wrexham AFC', '2025', 46, 19, 14, 13, 69, 65, 4, 71),
    (8, 'Derby County FC', '2025', 46, 20, 9, 17, 67, 59, 8, 69),
    (9, 'Norwich City FC', '2025', 46, 19, 8, 19, 63, 56, 7, 65),
    (10, 'Birmingham City FC', '2025', 46, 17, 13, 16, 57, 56, 1, 64),
    (11, 'Swansea City AFC', '2025', 46, 18, 10, 18, 57, 59, -2, 64),
    (12, 'Bristol City FC', '2025', 46, 17, 11, 18, 59, 59, 0, 62),
    (13, 'Sheffield United FC', '2025', 46, 18, 6, 22, 66, 66, 0, 60),
    (14, 'Preston North End FC', '2025', 46, 15, 15, 16, 55, 62, -7, 60),
    (15, 'Queens Park Rangers FC', '2025', 46, 16, 10, 20, 61, 73, -12, 58),
    (16, 'Watford FC', '2025', 46, 14, 15, 17, 53, 65, -12, 57),
    (17, 'Stoke City FC', '2025', 46, 15, 10, 21, 51, 56, -5, 55),
    (18, 'Portsmouth FC', '2025', 46, 14, 13, 19, 49, 64, -15, 55),
    (19, 'Charlton Athletic FC', '2025', 46, 13, 14, 19, 44, 58, -14, 53),
    (20, 'Blackburn Rovers FC', '2025', 46, 13, 13, 20, 42, 56, -14, 52),
    (21, 'West Bromwich Albion FC', '2025', 46, 13, 14, 19, 48, 58, -10, 51),
    (22, 'Oxford United FC', '2025', 46, 11, 14, 21, 45, 59, -14, 47),
    (23, 'Leicester City FC', '2025', 46, 12, 16, 18, 58, 68, -10, 46),
    (24, 'Sheffield Wednesday FC', '2025', 46, 2, 12, 32, 29, 89, -60, 0),
]

inserted = 0
for row in standings_2025:
    try:
        cur.execute('INSERT OR IGNORE INTO Standings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
        inserted += 1
    except Exception as e:
        print(f'Error inserting {row[1]}: {e}')

conn.commit()
print(f'{inserted} teams inserted for 2025/26 season!')
cur.close()
conn.close()