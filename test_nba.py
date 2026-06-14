from nba_api.stats.endpoints import leagueleaders

# Pull top scorers from 2020-21 season
leaders = leagueleaders.LeagueLeaders(season='2020-21')
df = leaders.get_data_frames()[0]

# Show first 5 rows
print(df[['PLAYER', 'TEAM', 'GP', 'PTS', 'FG_PCT']].head())