from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import pandas as pd
import time


# Path to geckodriver
service = Service("C:/Users/gameg/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe")  # Windows example

# Create Firefox driver (headless so no window pops up)
options = webdriver.FirefoxOptions()
#options.add_argument("--headless")

driver = webdriver.Firefox(service=service, options=options)

# Example Yahoo stats page (Josh Allen)
url = "https://sports.yahoo.com/nfl/stats/individual/?selectedTable=1&qualified=FALSE"
driver.get(url)
time.sleep(3)  # wait for JS to load

# Extract table rows
rowsData = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

all_stats = []
page_list = []

page = driver.find_elements(By.CSS_SELECTOR, "ul.ys-pagination")
curr_page = int(driver.find_element(By.CSS_SELECTOR, "ul.ys-pagination span.Fw\\(b\\)").text)


for i in page:
    page_list = [c.text for c in i.find_elements(By.CSS_SELECTOR, "li")]

for i in page_list:
    if curr_page != 1:
        pages = driver.find_element(By.LINK_TEXT, str(curr_page))
        pages.click()
        rowsData = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    
    for row in rowsData:
        name = [c.text for c in row.find_elements(By.TAG_NAME, "th")]
        cols = [c.text for c in row.find_elements(By.TAG_NAME, "td")]
        if cols:
            all_stats.append(name + cols)
    curr_page += 1

driver.quit()

#Save to DataFrame
df = pd.DataFrame(all_stats)
print(df)
df.to_csv("player_rushing_stats.csv", index=False)

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
