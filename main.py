import requests
from bs4 import BeautifulSoup
import json

from Foundation import AlleKategorien

alle_kategorien = AlleKategorien()

for kat, content in alle_kategorien.items():
    anz = content["Anzahl Rezepte"]
    print(f"Jetzt ist wieder Kategorie {kat} mit {anz} dran.")
    
    alle_rezept_urls = []
    for Seiten_URL in content["alle_Seiten_urls"]:
        response = requests.get(Seiten_URL)
        soup = BeautifulSoup(response.text, "lxml")

        rezepte = soup.find_all("a", {"class": "ds-recipe-card__link ds-teaser-link"})
        for rezept in rezepte:
            rezept_url = rezept.attrs["href"]
            alle_rezept_urls.append(rezept_url)   
        
    content["alle_Rezept_urls"] = alle_rezept_urls   


with open("AlleKategorien.json", 'w') as json_file:
    json.dump(alle_kategorien, json_file, indent=4)