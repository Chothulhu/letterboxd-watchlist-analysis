from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

data_frame = pd.read_csv(
    r"C:\Users\cho\Desktop\StatistikaProj\data\filmovi.csv"
)

links = np.asarray(data_frame["Letterboxd URI"])
length_rows = []
count = 0

for link in links:
    page_to_scrape = requests.get(link)

    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    p_tag = soup.find("p", class_="text-link text-footer")
    if p_tag:
        text = p_tag.get_text(strip=True)

        # filter for numeric characters
        minutes = "".join(filter(str.isdigit, text.split("mins")[0].strip()))

        length_rows.append(minutes)

    count = count + 1
    print("Count: ", count)

df = pd.DataFrame(length_rows)

output_file = "lengths.csv"
df.to_csv(output_file, index=False, header=False)

print(f"Lengths saved to {output_file}")
