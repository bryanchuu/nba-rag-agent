import time
import os
import wikipediaapi
import sqlite3

os.makedirs('bios', exist_ok=True)    # Make bios folder to store player info

folder_name = 'bios'

wiki = wikipediaapi.Wikipedia('NBARAGAgent/1.0', 'en')

conn = sqlite3.connect('nba_stats.db')
cursor = conn.cursor()

query = """
    SELECT PLAYER 
    FROM player_stats 
    GROUP BY PLAYER 
    ORDER BY SUM(PTS) DESC 
    LIMIT 500
"""
cursor.execute(query)

players = []

for row in cursor.fetchall():
    players.append(row[0]) 

conn.close()

for i, player in enumerate(players):
    print(f"[{i+1}/500] {player}")

    file_path = os.path.join(folder_name, f'{player}.txt')

    if not os.path.exists(file_path):

        page = wiki.page(f"{player} (basketball)")

        if not page.exists():
            page = wiki.page(player)  # fallback to just the name
            
        time.sleep(1)

        if page.exists():
            print(page.text[:500])

            with open(file_path, mode='w', encoding='utf-8') as file:
                file.write(page.text)
                
            print(f'Successfully wrote data to {player}.txt')
            
        else:
            print('Page not found')

    else:
        print('File already exists')   