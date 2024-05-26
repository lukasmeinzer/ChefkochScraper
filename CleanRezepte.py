import pandas as pd
import json
import numpy as np

with open("Rezepte.json", "r") as json_file:
    dict_content = json.load(json_file)
    
df_rows = []

for id, content in dict_content.items():
    to_df_dict = {}
    
    to_df_dict["id"] = id
    to_df_dict["Anspruch"] = content["Anspruch"].replace("\ue202\n", "").strip()
    to_df_dict["Upload"] = content["Upload"].replace("\ue916\n", "").strip()
    to_df_dict["Zutaten"] = content["Zutaten"]    
    to_df_dict["URL"] = content["url"]
    
    json_content = content["json_content"]
    to_df_dict["Bild URL"] = json_content["image"]
    to_df_dict["Typ"] = json_content["@type"]
    to_df_dict["Kategorie"] = json_content["recipeCategory"]
    to_df_dict["Name"] = json_content["name"]
    to_df_dict["Vorbereitungszeit"] = json_content["prepTime"]
    try:
        to_df_dict["Kochzeit"] = json_content["cookTime"]
    except:
        to_df_dict["Kochzeit"] = np.nan
    to_df_dict["Zeit"] = json_content["totalTime"]
    to_df_dict["Yield"] = json_content["recipeYield"]
    try:
        to_df_dict["Anzahl Bewertungen"] = json_content["aggregateRating"]["ratingCount"]
    except:
        to_df_dict["Anzahl Bewertungen"] = 0
    try:
        to_df_dict["Bewertung"] = json_content["aggregateRating"]["ratingValue"]
    except:
        to_df_dict["Bewertung"] = np.nan
    try:
        to_df_dict["Anzahl Reviews"] = json_content["aggregateRating"]["reviewCount"]
    except:
        to_df_dict["Anzahl Reviews"] = np.nan
    try:
        to_df_dict["schlechteste Bewertung"] = json_content["aggregateRating"]["worstRating"]
    except:
        to_df_dict["schlechteste Bewertung"] = np.nan
    try:
        to_df_dict["beste Bewertung"] = json_content["aggregateRating"]["bestRating"]
    except:
        to_df_dict["beste Bewertung"] = np.nan
    to_df_dict["Keywords"] = json_content["keywords"]
    
    try:
        nährwerte = json_content["nutrition"]
    except:
        pass
    try:
        to_df_dict["Nährwerte je Portion"] = nährwerte["servingSize"]
    except:
        to_df_dict["Nährwerte je Portion"] = np.nan    
    try:
        to_df_dict["Kalorien"] = nährwerte["calories"]
    except:
        to_df_dict["Kalorien"] = np.nan
    try:
        to_df_dict["Eiweiß"] = nährwerte["proteinContent"]
    except:
        to_df_dict["Eiweiß"] = np.nan        
    try:
        to_df_dict["Fett"] = nährwerte["fatContent"]
    except:
        to_df_dict["Fett"] = np.nan
    try:
        to_df_dict["Kohlenhydrate"] = nährwerte["carbohydrateContent"]
    except:
        to_df_dict["Kohlenhydrate"] = np.nan
    
    df_rows.append(to_df_dict)
    

df = pd.DataFrame(df_rows)


df = df.drop_duplicates("id")

Zeitspalten = ["Vorbereitungszeit", "Kochzeit", "Zeit"]

for Spalte in Zeitspalten:
    minuten = df[Spalte].str.split("H").str[-1].str.strip("M").astype(float)
    stunden = df[Spalte].str.split("H").str[0].str.split("DT").str[-1].astype(float)

    zeit_inMinuten = (stunden * 60) + minuten
    df[Spalte] = zeit_inMinuten
    
df["Upload"] = pd.to_datetime(df["Upload"], dayfirst=True)

df["Nährwerte je Portion"] = df["Nährwerte je Portion"].astype(int)

df["Kalorien"] = df["Kalorien"].str.strip(" kcal").astype(float)

df["Eiweiß (g)"] = df["Eiweiß"].str.strip("g").str.replace(",", ".").astype(float)

df["Fett (g)"]= df["Fett"].str.strip("g").str.replace(",", ".").astype(float)

df["Kohlenhydrate (g)"] = df["Kohlenhydrate"].str.strip("g").str.replace(",", ".").astype(float)

df.dtypes
