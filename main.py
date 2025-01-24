#main-5
import streamlit as st
from processor import load_and_prepare_data, calculate_kpis
import pandas as pd




# Load the data
@st.cache_data
def load_data():
    return load_and_prepare_data()

movies = load_data()

st.sidebar.image("logo.jpg",use_column_width=True)

# Sidebar filters
st.sidebar.header("Filters")
genre_filter = st.sidebar.multiselect("Select Genres", 
                                       options=sorted(set(genre for sublist in movies['genres'] for genre in sublist)))
year_range = st.sidebar.slider("Select Release Year Range", 
                                int(movies['release_year'].min()), 
                                int(movies['release_year'].max()), 
                                (1925, 2020))
rating_range = st.sidebar.slider("Select Rating Range", 
                                  float(movies['rating'].min()), 
                                  float(movies['rating'].max()), 
                                  (0.0, 4.5))

# Filter the data
filtered_movies = movies[
    (movies['release_year'].between(year_range[0], year_range[1])) &
    (movies['rating'].between(rating_range[0], rating_range[1])) &
    (movies['genres'].apply(lambda x: any(genre in x for genre in genre_filter) if genre_filter else True))
]

# Calculate KPIs
avg_rating, top_movies, genre_counts= calculate_kpis(filtered_movies)


# Main dashboard
st.title("🎥 Movie Ratings Dashboard")

# KPIs
st.subheader("Key Performance Indicators")



col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Average Rating", value=f"{avg_rating:.2f}")
with col2:
    st.metric(label="Total Movies", value=len(filtered_movies))
with col3:
    st.metric(label="Unique Genres", value=len(genre_counts))



# Top Rated Movies Table
st.subheader("Top Rated Movies")
st.table(top_movies)

# Genre Popularity Chart
st.subheader("Genre Popularity")
st.bar_chart(genre_counts.head(10),x_label="Genre",y_label="Number of Movies")


# Rating Distribution
st.subheader("Rating Distribution")
st.bar_chart(filtered_movies['rating'].value_counts().sort_index(),x_label="Rating",y_label="Number of Movies")

# Correlation between release year and ratings
st.subheader("Correlation: Rating vs Release Year")
st.line_chart(filtered_movies.groupby('release_year')['rating'].mean(),x_label="Release Year", y_label="Rating")





# Movie Recommendations by Genre
if genre_filter:
    st.subheader(f"Top Rated Movies in Selected Genres: {', '.join(genre_filter)}")
    recommended_movies = filtered_movies[filtered_movies['genres'].apply(
        lambda x: any(genre in x for genre in genre_filter))]
    st.write(recommended_movies[['title', 'rating']].nlargest(5, 'rating'))




current_year = pd.to_datetime("today").year
filtered_movies['age'] = current_year - filtered_movies['release_year']

# Plot Rating vs Age
st.subheader("Ratings and trends for different age")

# Group by age and calculate the average rating for each age group
rating_vs_age = filtered_movies.groupby('age')['rating'].mean()

# Create the line chart for Rating vs Age
st.area_chart(rating_vs_age,x_label='Age', y_label="Rating")