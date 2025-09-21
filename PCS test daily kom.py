import re
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# URL of the race startlist
url = "https://www.procyclingstats.com/race/vuelta-a-espana/2025/stage-16-kom/result/result"

# Fetch the page
headers = {"User-Agent": "Mozilla/5.0"}  # Pretend to be a browser
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

stage = soup.title.string

stagetitle = re.search(r"(Stage \d+)", stage)
#print(stagetitle)

if stagetitle:
    stagenr = stagetitle.group(1)
    #print(stagenr)  # -> Stage 16

all_rows = []

# Find the main startlist container
today_koms = soup.find_all("h4", string=re.compile(r"^KOM Sprint"))

#print(today_koms)

for h4 in today_koms:
    section_title = h4.get_text(strip=True)
    parts = section_title.split(") ", 1)
    climb_name = parts[1] if len(parts) > 1 else section_title
    #print(climb_name)

    table = h4.find_next("table")

    headers = [th.get("data-code", th.get_text(strip=True)) for th in table.find_all("th")]

    rows = []
    # only get tbody rows (skip header row)
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        rows.append(cells)

    if rows:
        df = pd.DataFrame(rows, columns=headers)
        df["Climb"] = climb_name
        all_rows.append(df)

# combine all climbs into one DataFrame
final_df = pd.concat(all_rows, ignore_index=True)

#print(final_df.head())  # ✅ should show all climbs stacked together

# Save to Excel
filename = "/Users/angelo/Desktop/python_work/Tour_de_France_Competition.xlsx"
sheet_name = 'KOM ' + stagenr

if os.path.exists(filename):
    with pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        final_df.to_excel(writer, sheet_name=sheet_name, index=False)
    print("✅ Updated existing file")
else:
    final_df.to_excel(filename, sheet_name=sheet_name, index=False)
    print("✅ Created new Excel file")