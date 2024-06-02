from chefkoch import Recipe
import json
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import pickle
import pandas as pd

from db_inserter import table_into_db
from Kategorien import AlleKategorienSpeichern

AlleKategorienSpeichern()

with open("AlleKategorien.json", 'r') as json_file:
    kategorien = json.loads(json_file.read())

# Diese Links müssen alle gescraped werden:
alle_rezept_urls = []
for kat in kategorien.keys():
    alle_rezept_urls.extend(kategorien[kat]["alle_Rezept_urls"])
 
# Rezept-Objekte speichern
rezepte = []
for i, recipe_url in enumerate(alle_rezept_urls):
    print(f"{i}/{len(alle_rezept_urls)}", end="\r")
    recipe = Recipe(recipe_url)
    rezepte.append(recipe)

# Zwischenstand persistieren
with open("Rezepte.pkl", "wb") as handle:
    pickle.dump(rezepte, handle)

with open("Rezepte.pkl", "rb") as handle:
    rezepte = pickle.load(handle)

# Rezepte auslesen
attributes = [
    "id", "url", "image_url", "image_urls", "prep_time", "cook_time",
    "total_time", "difficulty", "ingredients", "calories", "keywords",
    "number_reviews", "number_ratings", "rating", "category"
]

def process_recipe(recipe):
    d = {}
    for attr in attributes:
        try:
            d[attr] = getattr(recipe, attr, None)
        except Exception:
            d[attr] = None
    return d

def process_recipes_parallel(recipes, num_workers=None):
    if num_workers is None:
        num_workers = cpu_count()

    with Pool(num_workers) as pool:
        processed_recipes = list(tqdm(pool.imap(process_recipe, recipes), total=len(recipes)))

    return processed_recipes

# Parallel Rezepte auslesen
processed_recipes = process_recipes_parallel(rezepte)

# Zwischenstand persistieren
with open("Rezepte_processed.pkl", "wb") as handle:
    pickle.dump(processed_recipes, handle)

with open("Rezepte_processed.pkl", "rb") as handle:
    rezepte = pickle.load(handle)

# Daten In Tabelle schreiben
df = pd.DataFrame(rezepte)

df["image_urls"] = df["image_urls"].apply(lambda x: ", ".join(x) if x != None else x)
df["ingredients"] = df["ingredients"].apply(lambda x: ", ".join(x) if x != None else x)
df["keywords"] = df["keywords"].apply(lambda x: ", ".join(x) if x != None else x)

df["prep_time"] = df["prep_time"].dt.total_seconds() / 60
df["cook_time"] = df["cook_time"].dt.total_seconds() / 60
df["total_time"] = df["total_time"].dt.total_seconds() / 60

# In DB schreiben!
table_into_db(df)