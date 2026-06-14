import sqlite3

conn = sqlite3.connect('nba_stats.db')
cursor = conn.cursor()

# Test 1: Who scored the most points in 2020-21?
print("=== Top 5 scorers in 2020-21 ===")
cursor.execute("""
    SELECT PLAYER, TEAM, PTS 
    FROM player_stats 
    WHERE SEASON = '2020-21' 
    ORDER BY PTS DESC 
    LIMIT 5
""")
for row in cursor.fetchall():
    print(row)

# Test 2: LeBron's stats across all seasons
print("\n=== LeBron's stats by season ===")
cursor.execute("""
    SELECT SEASON, TEAM, PTS, REB, AST 
    FROM player_stats 
    WHERE PLAYER LIKE '%LeBron%'
""")
for row in cursor.fetchall():
    print(row)

conn.close()