import requests
from bs4 import BeautifulSoup

base_url = "https://www.chefkoch.de"

def AlleKategorien():
    url = base_url + "/rezepte/"
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    alle_kategorien = soup.findAll("a", {"class": "sg-pill"})

    alle_kategorien = {
        kat.text.strip("\n"): {
            "start_url": kat.attrs["href"]
            }
        for kat in alle_kategorien
        }

    # Anzahl Rezepte rausfinden
    for kat, content in alle_kategorien.items():
        print(f"Aktuell ist Kategorie {kat} dran.")
        kat_url = base_url + content["start_url"]
    
        response = requests.get(kat_url)
    
        soup = BeautifulSoup(response.text, "lxml")
    
        Anzahl_Rezepte = int(soup.findAll("span", {"class": "ds-text-category"})[0].text.strip(" Rezepte").replace(".", ""))
        content["Anzahl Rezepte"] = Anzahl_Rezepte
    
    
        alle_urls = []
        for i in range(24): # Jede Kategorie kann 24 Seiten anzeigen
            url_splitter_1 = "/rs/s"
            thingies = content["start_url"].strip("/rs/s").split("t", maxsplit=1)
            url_splitter_2 = thingies[-1]
            neue_url = url_splitter_1 + str(i) + "t" + url_splitter_2
            alle_urls.append(base_url + neue_url)
        content["alle_Seiten_urls"] = alle_urls
   
    return alle_kategorien
