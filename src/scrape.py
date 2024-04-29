import json

from bs4 import BeautifulSoup
import pandas as pd
import requests

BASE_URL = "https://www.laurainthekitchen.com/"
RECIPE_SEARCH_URL = BASE_URL + "recipe-search.php?screen={}"

def get_recipe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", type="application/ld+json").text
    script.replace("<script type=\"application/ld+json\">", "")
    script.replace("</script>", "")
    recipe = json.loads(script, strict=False)
    return recipe

def get_recipe_urls(page):
    recipe_urls = []
    response = requests.get(RECIPE_SEARCH_URL.format(page))
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="cs-recipe-details-button")
    for div in divs:
        link = div.find("a")
        recipe_urls.append(link.get("href"))
    return recipe_urls

# Scrape all recipe URLs (pages 1 - 73)
recipe_urls = []
for page in range(1, 74):
    urls = get_recipe_urls(page)
    recipe_urls.extend(urls)

# Scrape the information from each recipe.
recipes = []
for recipe_url in recipe_urls:
    recipe = get_recipe(BASE_URL + recipe_url)
    recipe_clean = {}
    recipe_clean["name"] = recipe["name"].strip()
    recipe_clean["link"] = BASE_URL + recipe_url.strip()
    recipe_clean["image"] = recipe["image"].strip()
    recipe_clean["ingredients"] = list(map(str.strip, recipe["recipeIngredient"]))
    recipes.append(recipe_clean)

# Store recipe information in a DataFrame.
df = pd.DataFrame(recipes)

# Write the DataFrame to a file (recipes.csv).
df.to_csv("data/recipes.csv", index=False)
