from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# League URLs and Names
leagues = [
    {"url": "https://matchcentre.footprintapp.net/tournaments/profile/tour/984#logs", "name": "Super League A"},
    {"url": "https://matchcentre.footprintapp.net/tournaments/profile/tour/985#logs", "name": "Super League B"},
    {"url": "https://matchcentre.footprintapp.net/tournaments/profile/tour/986#logs", "name": "Super League C"},
]

# Setup headless Chrome
options = Options()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for league in leagues:
    url = league["url"]
    league_name = league["name"]

    print(f"🔍 Scraping: {league_name}")
    driver.get(url)

    # Wait until the table loads
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ajaxLoadingTable24"))
        )
    except Exception as e:
        print(f"❌ Table didn't load for {league_name}: {e}")
        continue

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "ajaxLoadingTable24"})

    if not table:
        print(f"❌ Table not found in DOM for {league_name}")
        continue

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"footprint_logs_{league_name.replace(' ', '_')}_{timestamp}.csv"

    headers = ["Position", "League", "Team", "Club", "P", "W", "D", "L", "PA", "PF", "PD", "LP"]

    rows = table.find_all("tr")

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        position_counter = 1
        for row in rows[1:]:  # Skip header row
            cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]

            if len(cols) > 12:
                club = cols[0]
                p = cols[1]
                w = cols[2]
                d = cols[3]
                l = cols[4]
                pf = cols[9]
                pa = cols[10]
                pd = cols[11]
                lp = cols[12]

                writer.writerow([
                    position_counter,
                    league_name,
                    "1st team",
                    club,
                    p, w, d, l, pa, pf, pd, lp
                ])
                position_counter += 1

    print(f"✅ Exported: {filename}")
    time.sleep(2)  # polite delay between leagues

driver.quit()
