import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# URL of the race startlist
url1 = "https://www.procyclingstats.com/race/vuelta-a-espana/2025/startlist"

# Fetch the page
headers = {"User-Agent": "Mozilla/5.0"}  # Pretend to be a browser
response = requests.get(url1, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

# Find the main startlist container
vuelta = soup.find("ul", class_="startlist_v4")

# Find all team containers
vueltateams = vuelta.find_all("div", class_="ridersCont")

#teams = {}
rows = []

for team in vueltateams:
    # Team name
    teamname = team.find("a", class_="team", href=True).text.strip()

    # Loop through riders (each <li>)
    for rider in team.find_all("li"):
        rider_link = rider.find("a", href=True)
        if rider_link and rider_link["href"].startswith("rider"):
            rider_name = rider_link.text.strip()

            # Bib number
            bib_tag = rider.find("span", class_="bib")
            bib = bib_tag.text.strip() if bib_tag else ""

            # Status: Inactive if li has class "dropout"
            status = "Inactive" if "dropout" in rider.get("class", []) else "Active"

            rows.append([bib, teamname, rider_name, status])

# 🔹 Build DataFrame in "long format"
df = pd.DataFrame(rows, columns=["Bib", "Team", "Rider", "Status"])

# Save to Excel (requires openpyxl)
filename = "Tour_de_France_Competition.xlsx"

if os.path.exists(filename):
    # File exists → append or replace a sheet
    with pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="Riders", index=False)
    print("✅ Rider list updated in existing file")
else:
    # File does not exist → create new one
    df.to_excel(filename, sheet_name="Riders", index=False)
    print("✅ New Excel file created with rider list")


'''
    # Rider names (text, not just hrefs)
    ridernames = [
        a.text.strip()
        for a in team.find_all("a", href=True)
        if a["href"].startswith("rider")
    ]
    for rider in ridernames:
        rows.append([teamname, rider])

#teams[teamname] = ridernames

# Print nicely
for team, riders in teams.items():
    print(team, "→", riders)

# Pretty print: each team + riders as a list
for team, riders in teams.items():
    print(f"\n{team}:")
    for rider in riders:
        print(f"  - {rider}")

# 🔹 Convert to a DataFrame
# Normalize dict into rows: one team per row, riders spread across columns
max_riders = max(len(riders) for riders in teams.values())
rows = []

for team, riders in teams.items():
    row = [team] + riders + [""] * (max_riders - len(riders))  # pad uneven lists
    rows.append(row)

# Column names: Team + Rider1, Rider2, ...
columns = ["Team"] + [f"Rider {i+1}" for i in range(max_riders)]
df = pd.DataFrame(rows, columns=columns)
'''
