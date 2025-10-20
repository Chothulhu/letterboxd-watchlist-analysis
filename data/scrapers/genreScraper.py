from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


data_frame = pd.read_csv(
    r"C:\Users\cho\Desktop\StatistikaProj\data\filmovi.csv"
)


links = np.asarray(data_frame["Letterboxd URI"])
genre_rows = []
count = 0
# test_link= "https://boxd.it/4Ste"
for link in links:
    page_to_scrape = requests.get(link)

    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    genres = soup.select('a.text-slug[href^="/films/genre/"]')
    genre_list = [genre.get_text() for genre in genres]

    print(genre_list)

    genre_rows.append(str(genre_list))
    count = count + 1
    print("Count: ", count)

df = pd.DataFrame(genre_rows)

output_file = "genres.csv"
df.to_csv(output_file, index=False, header=False)

print(f"Genres saved to {output_file}")
