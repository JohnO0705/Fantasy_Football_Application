from queue import Full
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import sqlite3
import string
import pandas as pd
import time

#Checks if variable is a float
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def is_digit_no_special(x):
    x = x.replace(",", "")
    return x.isdigit()

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
def grab_data(players):
    stats = []
    for player in players:
        data = []
        for c in player.find_elements(By.CSS_SELECTOR, "tr.Table__TR td.Table__TD"):
            text = c.text.replace(",", "")
            if text == "" or text is None:
                text = 0
            data.append(text)
        if data:
            stats.append(data)
    return stats

#Organizes the stats data to be connected to each player
def stats_data(stat_data):
    count = 0
    for stat in stat_data:
        if is_digit_no_special(stat) or is_float(stat) or count == 0:
            count += 1
        else:
            break
    stats = [stat_data[i:i+count] for i in range(0, len(stat_data), count)]
    return stats

#Sorts the data into lists for sqlite to use
def data_sorting():
    players = driver.find_elements(By.CSS_SELECTOR, "table tbody")
    stats = grab_data(players)

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
    
    return player_data

#Creates the passing table
def passing_table():
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

def rushing_table():
    # Create a new table
    c.execute('''
        CREATE TABLE IF NOT EXISTS rushing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            TEAM TEXT,
            POSITION TEXT,
            GAMES_PLAYED INTEGER,
            RUSHING_ATTEMPTS INTEGER,
            RUSHING_YARDS INTEGER,
            YARDS_PER_RUSH REAL,
            LONG_RUSHING INTEGER,
            TWENTY_PLUS_RUSHING_PLAYS INTEGER,
            RUSHING_TOUCHDOWNS INTEGER,
            RUSHING_YARDS_PER_GAME REAL,
            RUSHING_FUMBLES INTEGER,
            RUSHING_FUMBLES_LOST INTEGER,
            FIRST_DOWNS INTEGER
        )
    ''')

    # Insert records
    for player in player_data:
        c.execute("INSERT INTO rushing (NAME, TEAM, POSITION, GAMES_PLAYED, RUSHING_ATTEMPTS, RUSHING_YARDS, YARDS_PER_RUSH, LONG_RUSHING, TWENTY_PLUS_RUSHING_PLAYS, RUSHING_TOUCHDOWNS, RUSHING_YARDS_PER_GAME, RUSHING_FUMBLES, RUSHING_FUMBLES_LOST, FIRST_DOWNS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (player["Names"][0],
                player["Names"][1],
                player["Stats"][0], 
                int(player["Stats"][1]), 
                int(player["Stats"][2]), 
                int(player["Stats"][3]), 
                float(player["Stats"][4]), 
                int(player["Stats"][5]), 
                int(player["Stats"][6]), 
                int(player["Stats"][7]), 
                float(player["Stats"][8]), 
                int(player["Stats"][9]), 
                int(player["Stats"][10]), 
                int(player["Stats"][11])
                ))


    connection.commit()

def receiving_table():
    # Create a new table
    c.execute('''
        CREATE TABLE IF NOT EXISTS receiving (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            TEAM TEXT,
            POSITION TEXT,
            GAMES_PLAYED INTEGER,
            RECEPTIONS INTEGER,
            RECEIVING_TARGETS INTEGER,
            RECEIVING_YARDS INTEGER,
            YARDS_PER_RECEPTION REAL,
            RECEIVING_TOUCHDOWNS INTEGER,
            LONG_RECEPTION INTEGER,
            TWENTY_PLUS_RECEIVING_YARDS INTEGER,
            RECEIVING_YARDS_PER_GAME REAL,
            RECEIVING_FUMBLES INTEGER,
            RECEIVING_FUMBLES_LOST INTEGER,
            RECEIVING_YARDS_AFTER_CATCH INTEGER,
            RECEIVING_FIRST_DOWNS INTEGER
        )
    ''')

    # Insert records
    for player in player_data:
        c.execute("INSERT INTO receiving (NAME, TEAM, POSITION, GAMES_PLAYED, RECEPTIONS, RECEIVING_TARGETS, RECEIVING_YARDS, YARDS_PER_RECEPTION, RECEIVING_TOUCHDOWNS, LONG_RECEPTION, TWENTY_PLUS_RECEIVING_YARDS, RECEIVING_YARDS_PER_GAME, RECEIVING_FUMBLES, RECEIVING_FUMBLES_LOST, RECEIVING_YARDS_AFTER_CATCH, RECEIVING_FIRST_DOWNS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (player["Names"][0],
                player["Names"][1],
                player["Stats"][0], 
                int(player["Stats"][1]), 
                int(player["Stats"][2]), 
                int(player["Stats"][3]), 
                int(player["Stats"][4]), 
                float(player["Stats"][5]), 
                int(player["Stats"][6]), 
                int(player["Stats"][7]), 
                int(player["Stats"][8]), 
                float(player["Stats"][9]), 
                int(player["Stats"][10]), 
                int(player["Stats"][11]), 
                int(player["Stats"][12]), 
                int(player["Stats"][13])
                ))


    connection.commit()

# Path to geckodriver
service = Service("C:/Users/gameg/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe")  # Windows example

# Create Firefox driver (headless so no window pops up)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)

#Connect to sqlite table
connection = sqlite3.connect("player_stats_2024.db")
c = connection.cursor()

#ESPN player stats
url = "https://www.espn.com/nfl/stats/player/_/season/2024/seasontype/2"
driver.get(url)
time.sleep(3)  # wait for JS to load

tab = driver.find_element(By.CSS_SELECTOR, "div.ButtonGroup a.Button--active").text

load_tables()

for i in range(3):
    if tab == "Passing":
        player_data = data_sorting()
        passing_table()
        print("Data inserted successfully.")
        button = driver.find_element(By.LINK_TEXT, "Rushing")
        button.click()
        time.sleep(3)
        tab = driver.find_element(By.CSS_SELECTOR, "div.ButtonGroup a.Button--active").text
    elif tab == "Rushing":
        player_data = data_sorting()
        rushing_table()
        print("Data inserted successfully.")
        button = driver.find_element(By.LINK_TEXT, "Receiving")
        button.click()
        time.sleep(3)
        tab = driver.find_element(By.CSS_SELECTOR, "div.ButtonGroup a.Button--active").text
    elif tab == "Receiving":
        player_data = data_sorting()
        receiving_table()
        print("Data inserted successfully.")
        break

driver.quit()
c.close()
connection.close()
print("Done")

# # Fetch all records
# rows = c.fetchall()

# print("Players:\n")
# for row in rows:
#     print(f"Player ID: {row[0]}, Name: {row[1]}, Team: {row[2]}, Position: {row[3]}, Games Played: {row[4]}, Completions: {row[5]}, Passing Attempts: {row[6]}, Completion Percentage: {row[7]}, Passing Yards: {row[8]}, Yards Per Pass: {row[9]}, Passing Yards Per Game: {row[10]}, Longest Pass: {row[11]}, Passing Touchdowns: {row[12]}, Interceptions: {row[13]}, Total Sacks: {row[14]}, Sack Yards Lost: {row[15]}, Adjusted Qbr: {row[16]}, Passer Rating: {row[17]}")

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
