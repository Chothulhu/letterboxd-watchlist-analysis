from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


data_frame = pd.read_csv(
    r"C:\Users\cho\Desktop\StatistikaProj\data\filmovi.csv", encoding="utf-8"
)

links = np.asarray(data_frame["Letterboxd URI"])
cast_rows = []
count = 0

for link in links:
    try:
        page_to_scrape = requests.get(
            link, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        cast = soup.select('a[href^="/actor/"]')
        cast_list = [actor.get_text(strip=True) for actor in cast]

        top_3_cast = cast_list[:3]  # uzimamo samo prva 3 glumca
        formatted_cast = "|".join(top_3_cast)

        print(formatted_cast)
        cast_rows.append(formatted_cast)
    except Exception as e:
        print(f"Greška za link: {link}, poruka: {e}")
        cast_rows.append("")  # ako ne uspe

    count += 1
    print("Count:", count)

df = pd.DataFrame(cast_rows)

output_file = "cast.csv"
df.to_csv(output_file, index=False, header=False, encoding="utf-8-sig")

print(f"Cast saved to {output_file}")
