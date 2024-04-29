import ast
import re
import string

import pandas as pd
import nltk

units = {"c", "cc", "centimeter", "centimetre", "cm", "cubic", "cup", "deciliter", "decilitre", "f", "fl", "fluid", "g", "gal", "gallon", "gill", "gram", "gramme", "in", "inch", "kg", "kilogram", "kilogramme", "l", "lb", "liter", "litre", "m", "meter", "metre", "mg", "milligram", "milligramme", "milliliter", "millilitre", "millimeter", "millimetre", "ml", "mm", "ounce", "oz", "p", "pint", "pound", "pt", "q", "qt", "quart", "t", "tablespoon", "tbl", "tbs", "tbsp", "teaspoon", "tsp", "yard"}
remove = {"a", "about", "according", "active", "all", "amp", "an", "and", "any", "are", "around", "at", "baby", "bag", "baking", "ball", "balsamic", "basil", "bay", "beaten", "bell", "big", "bit", "bite", "bittersweet", "black", "boiled", "bone", "boneless", "bought", "box", "breadcrumb", "breast", "brown", "bunch", "but", "butter", "buttermilk", "can", "canned", "caper", "casing", "center", "cheese", "chive", "choice", "chopped", "chunk", "cleaned", "clove", "coarse", "cold", "coloring", "condensed", "confectioner", "container", "cooked", "cooking", "cored", "cornstarch", "couple", "cream", "cremini", "crumb", "crushed", "cube", "cubed", "cumin", "cut", "dash", "degree", "delicious", "deveined", "diced", "dill", "divided", "dough", "drained", "dried", "drizzle", "dry", "each", "egg", "enough", "envelope", "extra", "extract", "fat", "few", "fine", "finely", "flake", "floret", "flour", "for", "fresh", "freshly", "from", "frozen", "frying", "garnishing", "ginger", "gold", "grain", "granulated", "grated", "green", "ground", "half", "halved", "handful", "hard", "have", "head", "heavy", "herb", "homemade", "hot", "i", "ice", "if", "instant", "instruction", "into", "italian", "jar", "juice", "kalamata", "large", "leaf", "left", "lengthwise", "light", "like", "little", "lot", "low", "medium", "melted", "milk", "minced", "mini", "mix", "mixed", "moon", "more", "non", "not", "nutmeg", "of", "oil", "old", "olive", "on", "one", "onion", "optional", "or", "oregano", "other", "out", "pack", "package", "pan", "paprika", "parm", "parsley", "paste", "pastry", "patted", "peak", "peeled", "pepper", "piece", "pinch", "pitted", "plain", "plenty", "plus", "pounded", "powder", "powdered", "powerded", "prepared", "puff", "pure", "puree", "purpose", "quartered", "red", "regular", "removed", "rinsed", "ripe", "roasted", "roll", "room", "rosemary", "roughly", "russet", "salt", "sauce", "scoop", "seasoning", "seed", "seeded", "semisweet", "separated", "serve", "serving", "sesame", "sharp", "sheet", "short", "shortening", "shredded", "size", "skim", "skin", "skinless", "slice", "sliced", "small", "smashed", "smoked", "so", "soft", "softened", "sour", "spice", "splash", "spray", "sprig", "squeeze", "squeezed", "stalk", "starch", "stick", "stiff", "stock", "store", "strip", "such", "sugar", "sweet", "sweetened", "taste", "temperature", "that", "the", "their", "them", "they", "thick", "thigh", "thin", "thinly", "third", "thward", "thyme", "tiny", "to", "toasted", "topping", "torn", "total", "trimmed", "ttaste", "unsalted", "unsweetened", "up", "use", "vegetable", "very", "vinegar", "virgin", "w", "warm", "wash", "washed", "water", "wedge", "well", "whipped", "whipping", "whisked", "white", "whole", "with", "worcestershire", "yeast", "yellow", "yolk", "you", "your", "yukon", "zest"}
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

    # Remove units.
    ingredients = [i for i in ingredients if i not in units]

    # Remove silly words.
    ingredients = [i for i in ingredients if i not in remove]

    # Uniquify the ingredients.
    ingredients = list(set(ingredients))

    return ingredients

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
recipes_df.drop(recipes_df[recipes_df["ingredients"] == ""].index)

# Remove "Recipe" from the name of each recipe.
name_list = recipes_df["name"].to_list()
name_list = [name.rstrip("Recipe").strip() for name in name_list]
recipes_df["name"] = name_list

# Write the DataFrame to a file (recipes_parsed.csv).
recipes_df.to_csv("data/recipes_parsed.csv", index=False)
