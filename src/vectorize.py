import gensim
import numpy as np
import pandas as pd
import sklearn.feature_extraction

def main():
    # Load the recipes DataFrame.
    recipes_df = pd.read_csv("data/recipes_parsed.csv")

    # Gather the ingredients into a corpus.
    corpus = recipes_df["ingredients"].to_list()
    corpus = [sorted(ingredients.split()) for ingredients in corpus]

    # Utilize the word2vec model to capture word embeddings.
    # This transforms each ingredient (word) into a 100-dimensional vector.
    embeddings = gensim.models.word2vec.Word2Vec(
        corpus,
        vector_size=100,
        window=7,
        min_count=1
    )
    embeddings.save("models/ingredients.embedding")

    # Use TDIDF to determine the weight (importance) of each ingredient.
    corpus = [" ".join(i) for i in corpus]
    tfidf = sklearn.feature_extraction.text.TfidfVectorizer()
    tfidf.fit(corpus)
    ingredient_weight = {ingredient: tfidf.idf_[index] for ingredient, index in tfidf.vocabulary_.items()}

    # Transform each recipe into a single, normalized vector.
    # The vector of is computed by weighting the
    # word embeddings of the ingredients, and then
    # computing the mean across each dimension.
    recipe_vectors = []
    for ingredients in corpus:
        ingredients = ingredients.split()
        vectors_weighted = []
        for ingredient in ingredients:
            vectors_weighted.append(embeddings.wv.get_vector(ingredient) * ingredient_weight[ingredient])
        recipe_vector = np.array(vectors_weighted).mean(axis=0)
        recipe_vector /= np.linalg.norm(recipe_vector)
        recipe_vectors.append(recipe_vector)

    # Store the recipe vectors in a new DataFrame and save it.
    recipes_df["vector"] = recipe_vectors
    recipes_df.to_csv("data/recipes_vectorized.csv")

if __name__ == "__main__":
    main()
