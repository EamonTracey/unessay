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
    keywords = request.json.get("keywords", "")
    recommendations_df = recommend_recipes(keywords.split(","))
    recommendations_list = recommendations_df.to_dict(orient="records")
    return jsonify(recommendations_list)

if __name__ == "__main__":
    app.run(debug=True,port=8945)

