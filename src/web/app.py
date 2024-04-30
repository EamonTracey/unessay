import sys

import pandas as pd
from flask import Flask, render_template, request, jsonify

sys.path.append("src/core")
from engine import recommend_recipes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/engine')
def engine():
    return render_template('engine.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    keywords = request.form['keywords'].split(',')
    # Call your function with the input keywords
    recipes_df = recommend_recipes(keywords)
    if recipes_df is not None and not recipes_df.empty:
        recipes = recipes_df.to_dict('records')  # Convert DataFrame to list of dictionaries
        return jsonify({'recipes': recipes})
    else:
        return jsonify({'message': "No recipes found for the given keywords."})

if __name__ == '__main__':
    app.run(debug=True)

