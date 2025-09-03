from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import pandas as pd
import time


# Path to geckodriver
service = Service("C:/Users/gameg/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe")  # Windows example

# Create Firefox driver (headless so no window pops up)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)

# Example Yahoo stats page (Josh Allen)
url = "https://sports.yahoo.com/nfl/stats/weekly/?sortStatId=PASSING_YARDS&selectedTable=1"
driver.get(url)
time.sleep(3)  # wait for JS to load

# Extract table rows
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
all_stats = []
for row in rows:
    cols = [c.text for c in row.find_elements(By.TAG_NAME, "td")]
    if cols:
        all_stats.append(cols)

driver.quit()

# Save to DataFrame
df = pd.DataFrame(all_stats)
print(df)
df.to_csv("player_stats.csv", index=False)


