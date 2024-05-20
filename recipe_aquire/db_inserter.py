import json
import pandas as pd
from sqlalchemy import create_engine
import os
import datetime 

def Tabellarisieren(categories):
    df_list = []
    for category in categories:
        title = category.title.replace(" ", "-").replace("/", "-")
        file_path = f"Rezepte/{title}.json" 
        with open(file_path) as file:
            raw_text = file.read()
        content = json.loads(raw_text)

        df = pd.DataFrame(content)
    
        df_list.append(df)


    df_rezepte = pd.concat(df_list, axis=0).reset_index(drop=True)

    df_kategorien = pd.json_normalize(df_rezepte["category"]).rename(columns={"title": "Kategorie Titel", "url": "Kategorie URL", "recipe_amount": "Anzahl Rezepte in Kategorie"})


    df_rezepte = pd.concat([df_rezepte, df_kategorien], axis=1)

    df = (
        df_rezepte
        .drop(columns=["category"])
        .rename(columns={
            "name": "Name", 
            "ingredients": "Zutaten", 
            "text": "Text", 
            "instructions": "Anleitung", 
            "rating": "Bewertung", 
            "ratings_amount": "Anzahl Bewertungen", 
            "images": "Bilder URLs"
        })
        .dropna()
        .reset_index(drop=True)
        .drop_duplicates(["id", "Kategorie Titel"])
        .map(str)
    )
    return df


def table_into_db(
    df: pd.DataFrame, 
    db_name: str = "Rezepte",
    table_name: str = "Chefkoch"
    ):
    
    table_name = f"{current_kw()}_{table_name}"
    
    engine = create_engine(DbConnectionString(db_name))
    
    df.to_sql(f"{table_name}".lower(), engine, if_exists="replace", index=False)
    
    engine.dispose()
    

def DbConnectionString(db_name: str) -> str:
    connection_string = (
        "mysql+pymysql://"
        + os.getenv("DB_USER")
        + ":"
        + os.getenv("DB_PWD")
        + "@"
        + os.getenv("DB_HOST")
        + "/"
        + db_name
    ) 
    return connection_string


def current_kw() -> str:
    current_year = datetime.datetime.now().isocalendar()[0]
    current_week = datetime.datetime.now().isocalendar()[1]
    
    kw = str(current_year) + "_" + str(current_week)
    return kw