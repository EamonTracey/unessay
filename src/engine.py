import pickle

import gensim
import numpy as np
import pandas as pd

from parse_ingredients import parse_ingredients

recipes_df = pd.read_csv("data/recipes_parsed.csv")
embeddings = gensim.models.word2vec.Word2Vec.load("models/ingredients.embedding")
with open("models/ingredients.weight", "rb") as fp:
    ingredient_weight = pickle.load(fp)
with open("models/recipes.vector", "rb") as fp:
    recipe_vectors = pickle.load(fp)
def recommend_recipes(keywords, n=5):
    # Parse the input.
    keywords = parse_ingredients(keywords)

    # Convert the ingredient keywords into a vector.
    # Return None if none of the keywords are relevant.
    vectors_weighted = []
    for word in keywords:
        if word in embeddings.wv.index_to_key:
            vectors_weighted.append(embeddings.wv.get_vector(word) * ingredient_weight[word])
    if not vectors_weighted:
        return None
    keywords_vector = np.array(vectors_weighted).mean(axis=0)
    keywords_vector /= np.linalg.norm(keywords_vector)

    # Compute the similarity of the keywords with all recipes.
    # We do this via the dot product. Since the vectors are normalized,
    # the dot product computes the cosine of the angle between the vectors,
    # which is maximized when the vectors are closer together.
    similarities = [
        np.dot(keywords_vector, recipe_vector)
        for recipe_vector in recipe_vectors
    ]

    # Acquire the indices of the n most similar recipes.
    recommendations = np.argsort(similarities)[-n:][::-1]

    # Create a new DataFrame with the recommended recipes.
    recommendations_df = recipes_df.iloc[recommendations]
    recommendations_df.reset_index(drop=True)

    return recommendations_df
