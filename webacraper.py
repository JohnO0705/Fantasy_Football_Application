from queue import Full
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import sqlite3
import pandas as pd
import time


# Path to geckodriver
service = Service("C:/Users/gameg/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe")  # Windows example

# Create Firefox driver (headless so no window pops up)
options = webdriver.FirefoxOptions()
#options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)

# Example Yahoo stats page (Josh Allen)
url = "https://www.espn.com/nfl/stats/player"
driver.get(url)
time.sleep(3)  # wait for JS to load

stats = []
players = []

# players = driver.find_elements(By.CSS_SELECTOR, "table tbody")

# for player in players:
#     data = [c.text for c in player.find_elements(By.CSS_SELECTOR, "tr.Table__TR td.Table__TD a.AnchorLink")]
#     if data:
#         names.append(data)

players = driver.find_elements(By.CSS_SELECTOR, "table tbody")

for player in players:
    data = [c.text for c in player.find_elements(By.CSS_SELECTOR, "tr.Table__TR td.Table__TD")]
    if data:
        stats.append(data)

names_data = stats[0]
stats_data = stats[1]

names = [names_data[i] for i in range(1, len(names_data), 2)]



driver.quit()

# df = pd.DataFrame(stats)
print(stats)

# try:
#     curr_page = driver.find_element(By.CSS_SELECTOR, "div.tc a.AnchorLink").text

#     pages = driver.find_element(By.LINK_TEXT, curr_page)
#     pages.click()
#     time.sleep(3)
# except NoSuchElementException:   
#     print("Exception Caught")

# Extract table rows
# rowsData = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# all_stats = []
# page_list = []

# page = driver.find_elements(By.CSS_SELECTOR, "ul.ys-pagination")
# curr_page = int(driver.find_element(By.CSS_SELECTOR, "ul.ys-pagination span.Fw\\(b\\)").text)

#--------------------------------------------------------------------

#Sqlite code
# connection = sqlite3.connect("player_rushing_stats.db")
# c = connection.cursor()

# # Create a new table
# c.execute('''
#     CREATE TABLE IF NOT EXISTS rushing (
#         FIND INTEGER PRIMARY KEY NOT NULL,
#         FNAME TEXT NOT NULL,
#         COST INTEGER NOT NULL,
#         WEIGHT INTEGER
#     )
# ''')

# # Insert records
# c.execute("INSERT INTO hotel (FIND, FNAME, COST, WEIGHT) VALUES (1, 'Cakes', 800, 10)")
# c.execute("INSERT INTO hotel (FIND, FNAME, COST, WEIGHT) VALUES (2, 'Biscuits', 100, 20)")
# c.execute("INSERT INTO hotel (FIND, FNAME, COST, WEIGHT) VALUES (3, 'Chocos', 1000, 30)")

# connection.commit()
# print("Data inserted successfully.")
# connection.close()


# c.execute("SELECT * FROM hotel")

# # Fetch all records
# rows = c.fetchall()

# print("All Food Items:\n")
# for row in rows:
#     print(f"Food ID: {row[0]}, Name: {row[1]}, Cost: {row[2]}, Weight: {row[3]}")

# c.close()

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
