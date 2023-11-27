import pickle
import pandas as pd
import streamlit as st
import requests

# Function to fetch movie poster


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=dc1e4fe8a2116bb53fd189e2393e010c&language=en-US'.format(
        movie_id)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "No poster available"
    else:
        return "Failed to fetch poster"

# Function to recommend movies


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for j in movies_list:
        movie_id = movies.iloc[j[0]].movie_id
        recommended_movies.append(movies.iloc[j[0]].title)

        # Fetch poster with error handling
        poster = fetch_poster(movie_id)
        if poster != "No poster available" and poster != "Failed to fetch poster":
            recommended_movies_posters.append(poster)
        else:
            recommended_movies_posters.append("https://static.streamlit.io/examples/cat-jpg")  # or any default image

    return recommended_movies, recommended_movies_posters

# Set page config


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🍿",
    layout="wide",
)

# Load data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #f7f7f7;
            color: #333333;
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: #ecf0f1;
        }
        .sidebar .sidebar-content .block-container {
            margin-top: 2rem;
        }
        .sidebar .widget-components .button {
            background-color: #3498db;
            color: #ecf0f1;
        }
        .sidebar .widget-components .button:hover {
            background-color: #2980b9;
        }
        .main .block-container {
            margin-top: 2rem;
        }
        .main .element-container img {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
        }
        .main .element-container img:hover {
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and sidebar
st.title('Movie Recommendation System')
st.sidebar.header('User Options')

# User input for movie selection
selected_movie_name = st.sidebar.selectbox("Which movie do you like ? ❤️", movies['title'].values)

# Button for recommendations
if st.sidebar.button("Get Recommendations"):
    names, posters = recommend(selected_movie_name)

    # Display recommendations with enhanced styling
    st.subheader('🌟 Top 5 Recommendations')
    st.write("")  # Add some vertical space

    # Create a grid for recommendations
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i, col in enumerate(cols):
        with col:
            st.subheader(names[i])
            st.image(posters[i], use_column_width=True)
            st.write("")  # Add some vertical space
