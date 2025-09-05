from queue import Full
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import sqlite3
import pandas as pd
import time

#Checks if variable is a float
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

#Loads the tables from the website
def load_tables():
    try:
        curr_page = driver.find_element(By.CSS_SELECTOR, "div.tc a.AnchorLink").text

        pages = driver.find_element(By.LINK_TEXT, curr_page)
        pages.click()
        time.sleep(3)
    except NoSuchElementException:   
        print("No more tables")

#Scrapes the data from the tables (Not Sorted)
def grab_data():
    stats = []
    for player in players:
        data = [c.text for c in player.find_elements(By.CSS_SELECTOR, "tr.Table__TR td.Table__TD")]
        if data:
            stats.append(data)
    return stats

#Organizes the stats data to be connected to each player
def stats_data(data):
    count = 0
    for stat in stat_data:
        if stat.isdigit() or is_float(stat) or count == 0:
            count += 1
        else:
            break
    stats = [stat_data[i:i+count] for i in range(0, len(stat_data), count)]
    return stats

# Path to geckodriver
service = Service("C:/Users/gameg/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe")  # Windows example

# Create Firefox driver (headless so no window pops up)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)

#ESPN player stats
url = "https://www.espn.com/nfl/stats/player"
driver.get(url)
time.sleep(3)  # wait for JS to load

load_tables()

players = driver.find_elements(By.CSS_SELECTOR, "table tbody")
stats = grab_data()

names_data = stats[0]
stat_data = stats[1]

names = [names_data[i] for i in range(1, len(names_data), 2)]

name_only = []

for name in names:
    fullname = name.split("\n")
    name_only.append(fullname)

stats = stats_data(stat_data)

player_data = []

for name, stat in zip(name_only, stats):
    player_data.append({"Names" : name, "Stats" : stat})

driver.quit()

# df = pd.DataFrame(player_data)
# print(df)

#--------------------------------------------------------------------

#Sqlite code
connection = sqlite3.connect("player_rushing_stats.db")
c = connection.cursor()

# Create a new table
c.execute('''
    CREATE TABLE IF NOT EXISTS passing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT,
        TEAM TEXT,
        POSITION TEXT,
        GAMES_PLAYED INTEGER,
        COMPLETIONS INTEGER,
        PASSING_ATTEMPTS INTEGER,
        COMPLETION_PERCENTAGE REAL,
        PASSING_YARDS INTEGER,
        YARDS_PER_PASS REAL,
        PASSING_YARDS_PER_GAME REAL,
        LONGEST_PASS INTEGER,
        PASSING_TOUCHDOWNS INTEGER,
        INTERCEPTIONS INTEGER,
        TOTAL_SACKS INTEGER,
        SACK_YARDS_LOST INTEGER,
        ADJUSTED_QBR REAL,
        PASSER_RATING REAL
    )
''')

# Insert records
for player in player_data:
    c.execute("INSERT INTO passing (NAME, TEAM, POSITION, GAMES_PLAYED, COMPLETIONS, PASSING_ATTEMPTS, COMPLETION_PERCENTAGE, PASSING_YARDS, YARDS_PER_PASS, PASSING_YARDS_PER_GAME, LONGEST_PASS, PASSING_TOUCHDOWNS, INTERCEPTIONS, TOTAL_SACKS, SACK_YARDS_LOST, ADJUSTED_QBR, PASSER_RATING) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
              (player["Names"][0],
               player["Names"][1],
              player["Stats"][0], 
              int(player["Stats"][1]), 
              int(player["Stats"][2]), 
              int(player["Stats"][3]), 
              float(player["Stats"][4]), 
              int(player["Stats"][5]), 
              float(player["Stats"][6]), 
              float(player["Stats"][7]), 
              int(player["Stats"][8]), 
              int(player["Stats"][9]), 
              int(player["Stats"][10]), 
              int(player["Stats"][11]), 
              int(player["Stats"][12]), 
              float(player["Stats"][13]), 
              float(player["Stats"][14])
              ))


connection.commit()
print("Data inserted successfully.")


c.execute("SELECT * FROM passing")

# Fetch all records
rows = c.fetchall()

print("Players:\n")
for row in rows:
    print(f"Player ID: {row[0]}, Name: {row[1]}, Team: {row[2]}, Position: {row[3]}, Games Played: {row[4]}, Completions: {row[5]}, Passing Attempts: {row[6]}, Completion Percentage: {row[7]}, Passing Yards: {row[8]}, Yards Per Pass: {row[9]}, Passing Yards Per Game: {row[10]}, Longest Pass: {row[11]}, Passing Touchdowns: {row[12]}, Interceptions: {row[13]}, Total Sacks: {row[14]}, Sack Yards Lost: {row[15]}, Adjusted Qbr: {row[16]}, Passer Rating: {row[17]}")

c.close()
connection.close()

#--------------------------------------------------------------------

#Player names
# players = driver.find_elements(By.CSS_SELECTOR, "table tbody")

# for player in players:
#     data = [c.text for c in player.find_elements(By.CSS_SELECTOR, "tr.Table__TR td.Table__TD a.AnchorLink")]
#     if data:
#         names.append(data)


#-------------------------------------------------------------------

#Saving to csv (Temporary)
# print(df)
# df.to_csv("player_passing_stats.csv", index=False)

#-------------------------------------------------------------------

#How to click and get the data
# for row in rowsData:
#     name = [c.text for c in row.find_elements(By.TAG_NAME, "th")]
#     cols = [c.text for c in row.find_elements(By.TAG_NAME, "td")]
#     if cols:
#         first_stats.append(name + cols)

# pages = driver.find_element(By.LINK_TEXT, "2")
# pages.click()

# rowsData = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# second_stats = []

# for row in rowsData:
#     name = [c.text for c in row.find_elements(By.TAG_NAME, "th")]
#     cols = [c.text for c in row.find_elements(By.TAG_NAME, "td")]
#     if cols:
#         second_stats.append(name + cols)
