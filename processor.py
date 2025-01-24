import pandas as pd
import ast

def load_and_prepare_data():
    # Load datasets
    df_movies = pd.read_csv('new_movies.csv', low_memory=False)
    df_credits = pd.read_csv('new_credits.csv',low_memory=False)
    df_ratings = pd.read_csv('ratings.csv')

    # Merge datasets
    movies = df_movies.merge(df_credits, on='title')
    movies.rename(columns={"id": "movieId"}, inplace=True)
    movies = movies.merge(df_ratings, on='movieId')
    movies = movies[['movieId', 'title', 'overview', 'genres', 'keywords', 
                  'rating', 'release_date']]
    movies['rating']=movies['rating'].round(1)

    # Sample data for performance
    movies = movies.sample(n=2000, random_state=1)

    # Clean genres and convert release_date
    movies['genres'] = movies['genres'].apply(
        lambda x: [genre['name'] for genre in ast.literal_eval(x)] if isinstance(x, str) else [])
    movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
    movies['release_year'] = movies['release_date'].dt.year

    return movies

def calculate_kpis(filtered_movies):
    avg_rating = filtered_movies['rating'].mean()
    top_movies = filtered_movies.nlargest(5, 'rating')[['title', 'rating']]
    genre_counts = filtered_movies.explode('genres')['genres'].value_counts()
    return avg_rating, top_movies, genre_counts
