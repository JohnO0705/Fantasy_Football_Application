from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import sqlite3
import time

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

# Path to geckodriver
service = Service("C:/Users/gameg/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe")  # Windows example

# Create Firefox driver (headless so no window pops up)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)

#Connect to sqlite table
connection = sqlite3.connect("projected_points_2025.db")
c = connection.cursor()

#ESPN player stats
url = "https://fantasy.espn.com/football/players/projections"
driver.get(url)
time.sleep(3)  # wait for JS to load

fullSeason = driver.find_element(By.XPATH, "(//select[@class='dropdown__select'])[3]")

fullSeason.click()

season = driver.find_element(By.XPATH, "(//option[@value='currSeason'])")

season.click()

time.sleep(3)

sortable = driver.find_element(By.CSS_SELECTOR, "div.ButtonGroup button.Button span")

sortable.click()

time.sleep(3)

#Collects Player Names
names_table = driver.find_elements(By.XPATH, "(//div[contains(@class, 'player-column__athlete')]//a)")

names_data = []

for players in names_table:
    if players.text != '':
        names_data.append(players.text)

# #Collects Player Team
teams_table = driver.find_elements(By.XPATH, "(//span[contains(@class, 'playerinfo__playerteam')])")

teams_data = []

for players in teams_table:
    teams_data.append(players.text)

#Collects Player Position
positions_table = driver.find_elements(By.XPATH, "(//span[contains(@class, 'playerinfo__playerpos')])")

positions_data = []

for players in positions_table:
    positions_data.append(players.text)

# #Collects Projected Points
points_table = driver.find_elements(By.CSS_SELECTOR, "table tbody")

points_data = []

for points in points_table:
    points_data = [c.text for c in driver.find_elements(By.CSS_SELECTOR, "tr td div.total")]


complete_players = []

for names, teams, positions, points in zip(names_data, teams_data, positions_data, points_data):
    complete_players.append({"Names" : names, "Teams" : teams, "Positions" : positions, "Projected Points" : points})

# Create a new table
c.execute('''
    CREATE TABLE IF NOT EXISTS points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT,
        TEAM TEXT,
        POSITION TEXT,
        PROJECTED_POINTS REAL
    )
''')


# Insert records
for player in complete_players:
    c.execute("INSERT INTO points (NAME, TEAM, POSITION, PROJECTED_POINTS) VALUES (?, ?, ?, ?)", 
            (player["Names"],
            player["Teams"],
            player["Positions"], 
            float(player["Projected Points"])
            ))


connection.commit()
driver.quit()
c.close()
connection.close()
print("Done")