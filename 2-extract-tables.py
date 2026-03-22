# Modules
import pandas as pd
import lxml
from os import listdir
import re
import numpy as np

# Following this guide, read html using pandas: https://stackoverflow.com/a/61448317
# Note: this is similar to how R uses the rvest package

# Single page test
page = 'pages-schedules/Air Force Falcons - schedule.html'
html_page = pd.read_html(page, header=1)
df_page = html_page[0] #Originally saved as list
df_page.head()

# regex to get team name in a column
res = re.search("pages-schedules/(.*) - schedule.html", page)
res.group(1)



# Tables from all pages
all_pages = listdir('pages-schedules/')
df = pd.DataFrame()

for page in all_pages:
  html_page = pd.read_html("pages-schedules/"+page, header=1)
  df_page = html_page[0]
  res = re.search("^(.*) - schedule.html", page)
  df_page['Team'] = res.group(1)
  df = pd.concat([df, df_page])


# Clean table
#   1) Filter out rows where different tables were joined
#   2) Extract the number of points from RESULT

# Step 1
df = df[(df['DATE'] != 'DATE') & (df["W-L (CONF)"].notna()) & ((df['RESULT'].str.startswith("W")) | (df['RESULT'].str.startswith("L")))][['Team', 'OPPONENT','DATE','RESULT']]




# Step 2
df[['winp', 'lossp']] = (
  df['RESULT']
  .str.extract(r'[WL](\d{1,3})-(\d{1,3})')
  .astype(int)
)
df['res'] = df['RESULT'].str.slice(0,1)

df['Points'] = np.where(df['res']=='W', df['winp'], df['lossp'])
df = df[['Team', 'DATE', 'Points']]

# Step 3: Save data
df.to_csv('basketball_data_espn.csv', index=False)

# Step 4: visualize points by team
import seaborn as sns
import matplotlib.pyplot as plt

sns.kdeplot (
  data=df, x='Points', hue='Team', fill=True, alpha=1/1000, legend=False, common_norm=False
)
plt.legend([], [], frameon=False)  # remove legend completely
plt.show()

