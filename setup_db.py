import sqlite3

# Import NBA season stats for the top 500 players of each season
from nba_api.stats.endpoints import leagueleaders 

# Import league-wide player stats for seasons 2018 to 2023 (will expand later)
seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23']

all_data = [] # List for seasons pulled
for season in seasons:
    print(f'Pulling {season}...') # Print statement for season pulled
    leaders = leagueleaders.LeagueLeaders(season=season) # Call NBA API for season stats
    df = leaders.get_data_frames()[0] # Get first table of player stats
    df['SEASON'] = season
    df['PPG'] = df['PTS'] / df['GP']
    df['APG'] = df['AST'] / df['GP']
    df['RPG'] = df['REB'] / df['GP']
    df['SPG'] = df['STL'] / df['GP']
    df['BPG'] = df['BLK'] / df['GP']
    df['MPG'] = df['MIN'] / df['GP']
    df['TOPG'] = df['TOV'] / df['GP']
    df['FPG'] = df['PF'] / df['GP']
    df['FGA_PG'] = df['FGA'] / df['GP']
    df['FGM_PG'] = df['FGM'] / df['GP']
    df['FG3A_PG'] = df['FG3A'] / df['GP']
    df['FG3M_PG'] = df['FG3M'] / df['GP']
    df['FTA_PG'] = df['FTA'] / df['GP']
    df['FTM_PG'] = df['FTM'] / df['GP']
    df['OREB_PG'] = df['OREB'] / df['GP']
    df['DREB_PG'] = df['DREB'] / df['GP']
    # Normalise player names to remove accents and special characters
    df['PLAYER_NORMALIZED'] = df['PLAYER'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
    all_data.append(df) 
# Combine all seasons into 1 DataFrame
import pandas as pd
combined = pd.concat(all_data, ignore_index= True)

# Save to SQLite
conn = sqlite3.connect('nba_stats.db') # Open connection to nba_stats.db
combined.to_sql('player_stats', conn, if_exists='replace', index=False) # Writes contents of combined into player_stats table in the database
conn.close()

print(f'Saved {len(combined)} rows to nba_stats.db')
print(f'Columns: {list(combined.columns)}')