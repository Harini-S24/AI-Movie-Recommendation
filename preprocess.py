import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the movie data
df = pd.read_csv('movies.csv')

# Step 2: Fill missing descriptions with empty string
df['overview'] = df['overview'].fillna('')

# Step 3: Convert text to numbers using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(df['overview'])

# Step 4: Calculate similarity between movies
similarity = cosine_similarity(vectors)

# Step 5: Save movie data and similarity matrix as .pkl files
with open('movies.pkl', 'wb') as f:
    pickle.dump(df, f)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

print("Files created successfully!")