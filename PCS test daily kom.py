import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# URL of the race startlist
url = "https://www.procyclingstats.com/race/vuelta-a-espana/2025/stage-16-kom"

# Fetch the page
headers = {"User-Agent": "Mozilla/5.0"}  # Pretend to be a browser
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

# Find the main startlist container
vuelta = soup.find("div", class_="today hide")

# Find all team containers
#vueltateams = vuelta.find_all("div", class_="ridersCont")

#teams = {}
rows = []

for team in vuelta:
    # Team name
    rider_bib = team.find("td", class_="bibs")

    rows.append([rider_bib])

# 🔹 Build DataFrame in "long format"
df = pd.DataFrame(rows, columns=["Bib"])
print(df)
                  