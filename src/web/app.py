import sys

import pandas as pd
from flask import Flask, render_template, request, jsonify

sys.path.append("src/core")
from engine import recommend_recipes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def get_recommendations():
    keywords = request.json.get("keywords", "").split(",")
    num_recipes = int(request.json.get("numRecipes", "4"))

    recommendations_df = recommend_recipes(keywords, n=num_recipes)
    recommendations_list = recommendations_df.to_dict(orient="records")
    return jsonify(recommendations_list)

if __name__ == "__main__":
    app.run(host="10.31.231.230", debug=True, port=3131)
