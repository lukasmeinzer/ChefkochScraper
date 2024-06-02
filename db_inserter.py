import pandas as pd
from sqlalchemy import create_engine
import os
import datetime 

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