from chefkoch import ChefKochAPI, DataParser
import os

if __name__ == '__main__':
    categories = ChefKochAPI.get_categories()

    # recipe_amount = 200
    # recipes = []
    category = categories[0]
    os.makedirs("Rezepte", exist_ok=True)
    for category in categories[0:]:
        if category.title == "Punsch Rezepte":
            category_recipes = ChefKochAPI.parse_recipes(category)
            path = "Rezepte/" + category.title.replace(" ", "-").replace("/", "-")
            DataParser.write_recipes_to_json(
                file_path=path,
                recipes=category_recipes,
                min_rating=5
                )
                
                
                
import json

file_path = "test.json"
with open(file_path) as file:
    raw_text = file.read()
content = json.loads(raw_text)