from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

data_frame = pd.read_csv(
    r"C:\Users\cho\Desktop\StatistikaProj\data\filmovi.csv", encoding="utf-8"
)

links = np.asarray(data_frame["Letterboxd URI"])
rating_rows = []
count = 0

for link in links:
    try:
        page_to_scrape = requests.get(
            link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        # Pronađi ocenu (average rating)
        rating_tag = soup.select_one('meta[name="twitter:data2"]')
        if rating_tag:
            rating_text = rating_tag.get("content", "").split(" ")[0]
            try:
                rating = float(rating_text)
            except:
                rating = 0
        else:
            rating = 0

        print(rating)
        rating_rows.append(rating)

    except Exception as e:
        print(f"Greška za link: {link}, poruka: {e}")
        rating_rows.append(0)

    count += 1
    print("Count:", count)

df = pd.DataFrame(rating_rows)

output_file = "ratings.csv"
df.to_csv(output_file, index=False, header=False, encoding="utf-8-sig")

print(f"Ratings saved to {output_file}")
