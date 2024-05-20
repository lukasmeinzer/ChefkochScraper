from chefkoch import ChefKochAPI, DataParser
from db_inserter import Tabellarisieren, table_into_db
import os

if __name__ == '__main__':
    os.makedirs("Rezepte", exist_ok=True)
    
    categories = ChefKochAPI.get_categories()
    
    for category in categories[0:]:
        category_recipes = ChefKochAPI.parse_recipes(category)
        path = "Rezepte/" + category.title.replace(" ", "-").replace("/", "-")
        DataParser.write_recipes_to_json(
            file_path=path,
            recipes=category_recipes
            )
            
    # In DB schreiben
    df = Tabellarisieren(categories) 
    table_into_db(df)