import requests
from bs4 import BeautifulSoup
import json

URL = "https://tradelands.worldsofnations.com/price-guide/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_prices():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    prices = {}

    # Find all tables on the page
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")[1:]  # Skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                name = cols[0].get_text(strip=True)
                price_text = cols[1].get_text(strip=True).replace(",", "").replace("$", "")
                try:
                    price = float(price_text)
                    prices[name] = price
                except ValueError:
                    continue  # Skip rows with invalid price formats

    return prices

if __name__ == "__main__":
    prices = scrape_prices()
    with open("prices.json", "w") as f:
        json.dump(prices, f, indent=2)
    print(f"✅ Scraped {len(prices)} materials and saved to prices.json")