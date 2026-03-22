# Import modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Start Page
main_url = 'https://www.espn.com/mens-college-basketball/teams'
headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15'
}

# Read main page
main_page = requests.get(main_url, headers = headers)
soup = BeautifulSoup(main_page.content, "html.parser")

# Obtain all team cells
team_cells = soup.find_all("div", class_='pl3')

# For each team cell, extract all links
df_team_links = pd.DataFrame()
for team in team_cells:
  
  # Get team name and links
  team_name = [team.h2.text]
  team_links = team.find_all('a', class_='AnchorLink', href = True)
  
  # Store each link into its own column
  row_data = []
  col_data = []
  for link in team_links:
    col_data.append(link.text)
    row_data.append(link['href'])
  
  # By default, the first column is the team name
  col_data[0] = 'Home'
  
  # Join row and column data into the main data frame
  df_team = pd.DataFrame([team_name+row_data], columns = ['Team'] + col_data)
  df_team_links = pd.concat([df_team_links, df_team], ignore_index=True)

# Verify correct 
print(df_team_links)

# For each team, save the schedule page for the current season
# (Saving pages so I don't have to rerun and risk IP banning)

teams = df_team_links['Team'].to_list()
schedules = df_team_links['Schedule'].to_list()
home_url = 'https://www.espn.com'


for i in range(0,len(df_team_links)):
  team = teams[i]
  link = schedules[i]
  tmp_page = requests.get(home_url + link, headers=headers)
  
  with open(f'pages-schedules/{team} - schedule.html', 'w', encoding='utf') as f:
    f.write(tmp_page.text)
  
  # Wait 1 second before each request
  time.sleep(0.5)
  
print('Script 1 complete!')
