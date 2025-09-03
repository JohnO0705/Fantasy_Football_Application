from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import pandas as pd
import time

#Setting up Selenium
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

service = Service("C:/Users/gameg/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe")  # replace with your path
driver = webdriver.Firefox(service=service, options=options)

# --- Load Player Stats Page ---
url = "https://sports.yahoo.com/nfl/stats/weekly/?sortStatId=PASSING_YARDS&selectedTable=1"  # Example player
driver.get(url)

time.sleep(3)  # wait for JavaScript to load

# --- Grab Stats Table ---
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
all_stats = []

for row in rows:
    cols = [c.text for c in row.find_elements(By.TAG_NAME, "td")]
    if cols:
        all_stats.append(cols)

driver.quit()

# --- Save into DataFrame ---
df = pd.DataFrame(all_stats)
print(df)
df.to_csv("player_stats_rushing.csv", index=False)
