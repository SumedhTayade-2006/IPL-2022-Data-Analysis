
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv(r"C:\Users\raahu\Music\IPL dataset.csv")
sns.set_theme(style="whitegrid")
os.makedirs("visualizations", exist_ok=True)

#analysing the structure of dataset
print(f"the overall row-columns in dataset: {df.shape}")
print(f"Names of all columns present in dataset:\n{df.columns}")
print("Data types and dataset information:")
df.info()
print(f"the starting five rows:\n{df.head()}")


#checking for missing values and duplicates
print(f"missing values:\n{df.isnull().sum()}")
print(f"duplicates in dataset:\n{df.duplicated().sum()}")


#A.checking which team made most runs in 2022:
team_runs = df.groupby('BattingTeam')['total_run'].sum().sort_values(ascending=False)
print(f"which team made most total_runs in 2022:\n{team_runs}")


#B.Find the top 10 run-scoring batsmen:
batsman_runs = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(10)
print(f"the top 10 run-scoring batsmen:\n{batsman_runs}")


#C.Find the top 10 bowlers with the most wickets
bowler_wickets = df.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head(10)
print(f"the top 10 bowlers by wicket deliveries:\n{bowler_wickets}")


#D.Which type of dismissal occurred most frequently in IPL 2022?
print(f"type of dismissal occurred most frequently in IPL 2022:\n{df['kind'].value_counts()}")


#E.total runs scored by each team in each innings
print(f"total runs scored by each team in each innings in 2022:\n{df.groupby(['BattingTeam','innings'])['total_run'].sum()}")


#F.strike rate of each player
runs = df.groupby('batter')['batsman_run'].sum()

#excluding wides from balls faced
balls_faced = df[~df['extra_type'].isin(['wide', 'wides'])].groupby('batter').size()

player_stats = pd.DataFrame({
    'runs': runs,
    'balls_faced': balls_faced
}).fillna(0)

#only batsmen who faced at least 50 balls
player_stats = player_stats[player_stats['balls_faced'] >= 50]

player_stats['strike_rate'] = (player_stats['runs'] / player_stats['balls_faced']) * 100

print(f"top 10 players with highest strike rate:\n{player_stats['strike_rate'].sort_values(ascending=False).head(10)}")


#G.Which bowlers gave away the fewest runs per over
#excluding wides and no-balls from legal deliveries
illegal_types = ['wide', 'wides', 'no ball', 'no-ball', 'noball', 'noballs']

legal_deliveries = df[~df['extra_type'].isin(illegal_types)]

legal_balls = legal_deliveries.groupby('bowler').size()

#excluding byes and leg-byes from bowler's runs conceded
non_bowler_extras = ['byes', 'bye', 'legbyes', 'leg-byes']

extra_runs = df[df['extra_type'].isin(non_bowler_extras)].groupby('bowler')['extras_run'].sum()

totalruns_by_bowlers = (df.groupby('bowler')['total_run'].sum() - extra_runs).fillna(0)

new_df1 = pd.DataFrame({
    'totalruns_by_bowlers': totalruns_by_bowlers,
    'legal_balls': legal_balls
}).fillna(0)

#minimum 60 legal balls
new_df1 = new_df1[new_df1['legal_balls'] >= 60]

new_df1['economy_rate'] = new_df1['totalruns_by_bowlers'] / (new_df1['legal_balls'] / 6)

print(f"bowlers with the lowest economy rate:\n{new_df1.sort_values(by='economy_rate').head(10)}")


#H.the batsman who scored the most runs in a single match innings
print(f"the batsman who scored the most runs in a single innings:\n{df.groupby(['ID','batter','innings'])['batsman_run'].sum().sort_values(ascending=False).head(1)}")


#I.team_average runs per innings
new_df2 = df.groupby(['BattingTeam', 'innings', 'ID'])['total_run'].sum()

average_by_innings = new_df2.groupby('BattingTeam').mean()

print(f"the team with highest average runs in innings:\n{average_by_innings.sort_values(ascending=False)}")


#VISUALIZATION STARTS FROM BELOW

#J.Create a bar chart comparing the total runs scored by each team.
team_runs = team_runs.sort_values(ascending=False)

plt.figure(figsize=(11, 6))
sns.barplot(x=team_runs.index, y=team_runs.values)

plt.title("Total Runs Scored by Each Team - IPL 2022")
plt.xlabel("Teams")
plt.ylabel("Total Runs")
plt.xticks(rotation=35, ha='right')
plt.tight_layout()

plt.savefig("visualizations/team_total_runs.png", dpi=300)
plt.show()
plt.close()


#K.Top 10 run-scoring batsmen
plt.figure(figsize=(10, 6))

sns.barplot(x=batsman_runs.values, y=batsman_runs.index)

plt.title("Top 10 Run-Scoring Batsmen - IPL 2022")
plt.xlabel("Total Runs")
plt.ylabel("Batsmen")
plt.tight_layout()

plt.savefig("visualizations/top_batsmen.png", dpi=300)
plt.show()
plt.close()


#L.top 10 bowlers by wicket deliveries
plt.figure(figsize=(10, 6))

sns.barplot(x=bowler_wickets.values, y=bowler_wickets.index)

plt.title("Top 10 Bowlers by Wicket Deliveries - IPL 2022")
plt.xlabel("Wicket Deliveries")
plt.ylabel("Bowlers")
plt.tight_layout()

plt.savefig("visualizations/top_bowlers.png", dpi=300)
plt.show()
plt.close()


#M.Team-wise average runs per innings
tempdf1 = df.groupby(['BattingTeam', 'innings', 'ID'])['total_run'].sum()

tempdf1_avg = tempdf1.groupby(['BattingTeam', 'innings']).mean().reset_index()

plt.figure(figsize=(12, 6))

sns.barplot(
    data=tempdf1_avg,
    x='BattingTeam',
    y='total_run',
    hue='innings'
)

plt.title("Team-wise Average Runs per Innings - IPL 2022")
plt.xlabel("Teams")
plt.ylabel("Average Runs")
plt.xticks(rotation=35, ha='right')
plt.legend(title="Innings")
plt.tight_layout()

plt.savefig("visualizations/team_average_innings.png", dpi=300)
plt.show()
plt.close()


print(f"most common dismissal type:\n{df['kind'].value_counts()}")

print("\nAll analysis and visualizations completed successfully!")
