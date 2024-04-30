import ast
import re
import string

import pandas as pd
import nltk

with open("data/unwords.txt") as fp:
    unwords = fp.read().splitlines()
def parse_ingredients(ingredients):
    # Remove anything inside parentheses.
    ingredients = [re.sub(r"\([^)]*\)", "", i) for i in ingredients]

    # Craft a list of words.
    ingredients = " ".join(ingredients).split()
    ingredients = list(set(ingredients))
    
    # Remove punctuation.
    ingredients = [i.translate(str.maketrans("", "", string.punctuation)) for i in ingredients]

    # Remove anything with wacky characters.
    ingredients = [i for i in ingredients if i.isalpha()]

    # Convert everything to lowercase.
    ingredients = [i.lower() for i in ingredients]

    # Lemmatize all the words.
    lemmatizer = nltk.stem.WordNetLemmatizer()
    ingredients = [lemmatizer.lemmatize(i) for i in ingredients]

    # Remove letters.
    ingredients = [i for i in ingredients if len(i) > 1]

    # Remove unwords.
    ingredients = [i for i in ingredients if i not in unwords]

    # Uniquify the ingredients.
    ingredients = list(set(ingredients))

    return ingredients

def main():
    # Load the recipes and ingredients.
    recipes_df = pd.read_csv("data/recipes.csv")
    ingredients_list = recipes_df["ingredients"].to_list()
    ingredients_list = [ast.literal_eval(i) for i in ingredients_list]

    # Parse the ingredients.
    ingredients_parsed_list = []
    for ingredients in ingredients_list:
        ingredients_parsed = parse_ingredients(ingredients)
        ingredients_parsed = " ".join(ingredients_parsed)
        ingredients_parsed_list.append(ingredients_parsed)
    recipes_df["ingredients"] = ingredients_parsed_list

    # Drop recipes with no ingredients.
    recipes_df = recipes_df.drop(recipes_df[recipes_df["ingredients"] == ""].index)
    recipes_df = recipes_df.dropna(subset=["ingredients"])

    # Remove "Recipe" from the name of each recipe.
    name_list = recipes_df["name"].to_list()
    name_list = [name.rstrip("Recipe").strip() for name in name_list]
    recipes_df["name"] = name_list

    # Write the DataFrame to a file (recipes_parsed.csv).
    recipes_df.to_csv("data/recipes_parsed.csv", index=False)

if __name__ == "__main__":
    main()
