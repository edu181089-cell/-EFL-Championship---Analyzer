import urllib.request
import sqlite3
import ssl
import json

from config import API_KEY

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_data(url):
    req = urllib.request.Request(url, headers={'X-Auth-Token': API_KEY})
    response = urllib.request.urlopen(req, context=ctx)
    return json.loads(response.read())

# -------------------------
# DATABASE SETUP
# -------------------------
conn = sqlite3.connect('championship_database.sqlite')
cur = conn.cursor()

# Standings table
cur.execute('DROP TABLE IF EXISTS Standings')
cur.execute('''
    CREATE TABLE Standings (
        position INTEGER,
        team TEXT,
        played INTEGER,
        won INTEGER,
        drawn INTEGER,
        lost INTEGER,
        goals_for INTEGER,
        goals_against INTEGER,
        goal_difference INTEGER,
        points INTEGER
    )
''')

# Matches table
cur.execute('DROP TABLE IF EXISTS Matches')
cur.execute('''
    CREATE TABLE Matches (
        match_id INTEGER PRIMARY KEY,
        matchday INTEGER,
        date TEXT,
        home_team TEXT,
        away_team TEXT,
        home_goals INTEGER,
        away_goals INTEGER,
        result TEXT
    )
''')

# -------------------------
# FETCH AND STORE STANDINGS
# -------------------------
print('Fetching standings...')
data = fetch_data('https://api.football-data.org/v4/competitions/ELC/standings')
table = data['standings'][0]['table']

for entry in table:
    cur.execute('''
        INSERT INTO Standings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry['position'],
        entry['team']['name'],
        entry['playedGames'],
        entry['won'],
        entry['draw'],
        entry['lost'],
        entry['goalsFor'],
        entry['goalsAgainst'],
        entry['goalDifference'],
        entry['points']
    ))

conn.commit()
print('Standings saved!')

# -------------------------
# FETCH AND STORE MATCHES
# -------------------------
print('Fetching matches...')
data = fetch_data('https://api.football-data.org/v4/competitions/ELC/matches?season=2025')
matches = data['matches']

stored = 0
for match in matches:
    # Only store finished matches
    if match['status'] != 'FINISHED':
        continue
    
    cur.execute('''
        INSERT OR IGNORE INTO Matches VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        match['id'],
        match['matchday'],
        match['utcDate'],
        match['homeTeam']['name'],
        match['awayTeam']['name'],
        match['score']['fullTime']['home'],
        match['score']['fullTime']['away'],
        match['score']['winner']
    ))
    stored += 1

conn.commit()
print(f'{stored} matches saved!')

# -------------------------
# ANALYSIS QUERIES
# -------------------------
print('\n--- TOP 6 ---')
for row in cur.execute('SELECT position, team, points, won, lost FROM Standings ORDER BY position LIMIT 6'):
    print(f'{row[0]}. {row[1]} - {row[2]} pts (W{row[3]} L{row[4]})')

print('\n--- BOTTOM 3 ---')
for row in cur.execute('SELECT position, team, points, goal_difference FROM Standings ORDER BY position DESC LIMIT 3'):
    print(f'{row[0]}. {row[1]} - {row[2]} pts (GD: {row[3]})')

print('\n--- HOME VS AWAY WINS ---')
for row in cur.execute("""
    SELECT 
        SUM(CASE WHEN result = 'HOME_TEAM' THEN 1 ELSE 0 END) as home_wins,
        SUM(CASE WHEN result = 'AWAY_TEAM' THEN 1 ELSE 0 END) as away_wins,
        SUM(CASE WHEN result = 'DRAW' THEN 1 ELSE 0 END) as draws
    FROM Matches
"""):
    print(f'Home wins: {row[0]} | Away wins: {row[1]} | Draws: {row[2]}')

print('\n--- HIGHEST SCORING MATCHES ---')
for row in cur.execute('''
    SELECT home_team, away_team, home_goals, away_goals, 
           (home_goals + away_goals) as total_goals
    FROM Matches 
    ORDER BY total_goals DESC 
    LIMIT 5
'''):
    print(f'{row[0]} {row[2]} - {row[3]} {row[1]} ({row[4]} goals)')

print('\n--- MOST HOME WINS ---')
for row in cur.execute("""
    SELECT home_team, COUNT(*) as home_wins
    FROM Matches
    WHERE result = 'HOME_TEAM'
    GROUP BY home_team
    ORDER BY home_wins DESC
    LIMIT 5
"""):
    print(f'{row[0]}: {row[1]} home wins')




cur.close()
conn.close()