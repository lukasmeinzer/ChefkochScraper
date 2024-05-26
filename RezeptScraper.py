import json
from bs4 import BeautifulSoup
import requests

with open("AlleKategorien.json", 'r') as json_file:
    kategorien = json.loads(json_file.read())

# Diese Links müssen alle gescraped werden:
alle_rezept_urls = []
for kat in kategorien.keys():
    alle_rezept_urls.extend(kategorien[kat]["alle_Rezept_urls"])


# url = "https://www.chefkoch.de/rezepte/3244751482869808/Kartoffelduett-aus-Suesskartoffel-und-normaler-Kartoffel.html"

dict_content = {}
for i, url in enumerate(alle_rezept_urls):   
    print(f"{i}/{len(alle_rezept_urls)}", end='\r')
    rezept_content = {}
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")

    chefkoch_plus = soup.find('amp-img', {'alt': 'Chefkoch Plus Logo'})
    if chefkoch_plus:
        continue
    
    rezept_content["url"] = url
    
    # id
    id = url.strip("https://www.chefkoch.de/rezepte/").split("/", maxsplit=1)[0]
    rezept_content["id"] = id

    # Meta
    meta_infos = soup.find("div", "ds-mb-right")
    try:
        text = meta_infos.find("p", {"class": "recipe-text"}).text.strip().strip("\n")
        rezept_content["Meta Text"] = text
    except:
        pass
    
    Anspruch = meta_infos.find("span", {"class": "recipe-difficulty rds-recipe-meta__badge"}).text.strip().strip("\n")
    rezept_content["Anspruch"] = Anspruch

    Upload_Datum = meta_infos.find("span", {"class": "recipe-date rds-recipe-meta__badge"}).text.strip().strip("\n")
    rezept_content["Upload"] = Upload_Datum

    # Zutaten
    zutaten_tables = soup.find_all("table", {"class": "ingredients table-header"})

    Zutaten = []
    for zutaten_table in zutaten_tables:
        zeilen = zutaten_table.find_all("tr")

        for zeile in zeilen:
            try:
                Zutat = zeile.find_all("td")[-1].text.strip().strip("\n")
                Zutaten.append(Zutat)
            except:
                pass
        rezept_content["Zutaten"] = Zutaten
        
    json_content = soup.find_all("script", {"type":"application/ld+json"})[1].text

    dict_json_content = json.loads(json_content)

    rezept_content["json_content"] = dict_json_content
    
    dict_content[id] = rezept_content



with open("Rezepte.json", 'w') as json_file:
    json.dump(dict_content, json_file, indent=4)