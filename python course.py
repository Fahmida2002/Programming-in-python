import pandas as pd
import numpy as np


path = "/content/drive/MyDrive/dataset/ODI.csv"

df = pd.read_csv(path)

df.shape[0]
df = df.iloc[:-86194, :].reset_index(drop = True)
df.tail()
duplicates = df[df.duplicated()]
duplicates
# df.shape[0]
class ODIAnalysis:
  def __init__(self, path):
    self.df = pd.read_csv(path)
    self.top_scorers = {}
    self._preprocessing()

  def _preprocessing(self):
    self.df = self.df.iloc[:-86194, :].reset_index(drop=True)
    self.df = self.df.replace('-', np.nan)

    numeric_cols = [
        'Innings Runs Scored Num',
        'Innings Boundary Sixes',
        'Innings Boundary Fours',
        'Innings Balls Faced',
        'Innings Batting Strike Rate'
    ]

    for col in numeric_cols:
        self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

  def top_scorer(self):
    self.index = self.df['Innings Runs Scored Num'].idxmax()
    print("Top Scorer : ")
    print('-'*20)
    print("Player:", self.df.loc[self.index, 'Innings Player'])
    print("Runs:", self.df.loc[self.index, 'Innings Runs Scored Num'])

  def lowest_scorer(self):
    self.index = self.df['Innings Runs Scored Num'].idxmin()
    print("Lowest Scorer : ")
    print('-'*20)
    print("Player:", self.df.loc[self.index, 'Innings Player'])
    print("Runs:", self.df.loc[self.index, 'Innings Runs Scored Num'])


  #Top 5 scorers (bbased on runs)
  def top_five_scorers_dict(self):
    top_df = self.df.sort_values(by='Innings Runs Scored Num', ascending=False).head(5)
    self.top_scorers = {}
    print("Top 5 Scorers : ")
    print('-'*20)
    for index, row in top_df.iterrows():
        player = row['Innings Player']
        runs = row['Innings Runs Scored Num']
        self.top_scorers[player] = runs
    return self.top_scorers

  #Average Strike Rate
  def avg_strike_rate(self):
   return self.df['Innings Batting Strike Rate'].mean()

  #total no. of sixes hit
  def total_six(self):
    return self.df['Innings Boundary Sixes'].sum()

  #total no. of fours hit
  def total_fours(self):
    return self.df['Innings Boundary Fours'].sum()


  #player summary

  def player_summary(self, name):
    player_df = self.df[self.df['Innings Player'] == name]

    if player_df.empty:
        return "Player not found"

    total_runs = player_df['Innings Runs Scored Num'].sum()
    total_sixes = player_df['Innings Boundary Sixes'].sum()
    total_fours = player_df['Innings Boundary Fours'].sum()
    total_balls = player_df['Innings Balls Faced'].sum()

    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    summary = {
        'Player': name,
        'Total Runs': int(total_runs),
        'Total Sixes': int(total_sixes),
        'Total Fours': int(total_fours),
        'Strike Rate': round(strike_rate, 2)
    }

    return summary
odi = ODIAnalysis(path)

# odi.preprocessing()

odi.top_five_scorers_dict()

print(odi.top_scorers)


print("Average Strike Rate :")
avg = odi.avg_strike_rate()

print(avg)

print("Total Runs :")
total_runs = odi.total_six()
print(total_runs)

print("Total Sixes :")
total_sixes = odi.total_fours()
print(total_sixes)

print(odi.player_summary("JE Root"))
