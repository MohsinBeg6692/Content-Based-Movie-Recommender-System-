import streamlit as st
import pandas as pd
import requests
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "ba464edb70e45722a72ec6935e1fc429"

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF6347;'>🎬 Ultimate Movie Recommender 🍿</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #00BFFF;'>Discover movies based on what you love!</h4>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    movies = pd.read_csv("tmdb_5000_movies.csv.zip")
    credits = pd.read_csv("tmdb_5000_credits.csv.zip")
    movies = movies.merge(credits, on='title')

    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'release_date']]
    movies.dropna(subset=['overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'release_date'], inplace=True)

    def convert(obj):
        try:
            return [i['name'] for i in ast.literal_eval(obj)]
        except:
            return []

    def castconvert(obj):
        try:
            return [i['name'] for i in ast.literal_eval(obj)[:3]]
        except:
            return []

    def director(obj):
        try:
            return [i['name'] for i in ast.literal_eval(obj) if i['job'] == 'Director']
        except:
            return []

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(castconvert)
    movies['crew'] = movies['crew'].apply(director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    for feature in ['genres', 'keywords', 'cast', 'crew']:
        movies[feature] = movies[feature].apply(lambda x: [str(i).replace(" ", "") for i in x])

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

    # Convert release_date to year safely
    movies['year'] = pd.to_datetime(movies['release_date'], errors='coerce').dt.year
    movies.dropna(subset=['year'], inplace=True)
    movies['year'] = movies['year'].astype(int)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)

    return movies, similarity

movies, similarity = load_data()

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    data = response.json()
    poster_path = data.get("poster_path", "")
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

def recommend(movie, genre_filter, rating_filter, year_range):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return [], []
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    filtered_movies = movies.copy()

    if genre_filter != 'All':
        filtered_movies = filtered_movies[filtered_movies['genres'].apply(lambda x: genre_filter in x)]

    filtered_movies = filtered_movies[
        (filtered_movies['vote_average'] >= rating_filter) &
        (filtered_movies['year'] >= year_range[0]) &
        (filtered_movies['year'] <= year_range[1])
    ]

    recommended_titles = []
    recommended_posters = []

    for i in distances[1:]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        if movie_title in filtered_movies['title'].values:
            recommended_titles.append(movie_title)
            recommended_posters.append(fetch_poster(movie_id))
        if len(recommended_titles) >= 5:
            break

    return recommended_titles, recommended_posters

selected_movie = st.selectbox("Select or Type a Movie Title", sorted(movies['title'].unique()))

# Genre filter (fixed safely)
all_genres = sorted(set(g for sublist in movies['genres'] for g in sublist))
genre_filter = st.selectbox("Filter by Genre", ['All'] + all_genres)

rating_filter = st.slider("Minimum Rating", 0.0, 10.0, 7.0, 0.5)
year_range = st.slider("Release Year Range", 1950, 2025, (2000, 2025))

if st.button("Recommend"):
    names, posters = recommend(selected_movie, genre_filter, rating_filter, year_range)
    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])
    else:
        st.warning("No matching movies found with the selected filters.")
