# 🎬 Content-Based Movie Recommendation System

A web-based movie recommender system built using **Python**, **Streamlit**, and **scikit-learn** that suggests similar movies based on content like genres, keywords, cast, and crew. It also fetches movie posters using the **TMDB API** for a visually rich experience.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-%F0%9F%A7%A1-lightgreen)

---

## 🚀 Features

- ✅ Content-based filtering using cosine similarity
- 🎭 Movie metadata processing: genres, keywords, cast, and crew
- 🖼️ Real-time movie poster retrieval using TMDB API
- 🔎 Search functionality with dropdown
- 🎛️ Filters for genres, cast, and more (if added)
- 📊 Clean and responsive UI built with Streamlit

---

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **scikit-learn**
- **Streamlit**
- **TMDB API**
- **CountVectorizer**

---

## 📂 Dataset

- [`tmdb_5000_movies.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- [`tmdb_5000_credits.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

These datasets are merged and preprocessed to generate relevant "tags" for recommendation.

---

## 🔗 Live Demo

https://bestmovierecommendor.streamlit.app/

---

## 📸 Screenshots

![Screenshot 2025-05-05 120733](https://github.com/user-attachments/assets/ac889877-a96a-4ce0-81af-c7f33bf34f55)

![Screenshot 2025-05-05 120243](https://github.com/user-attachments/assets/b9a3b7c0-1955-4b2a-8be5-dc94e62eb87e)

## 🧠 How It Works

1. **Data Preprocessing**:
   - The `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` datasets are merged on the title column.
   - Features like `genres`, `keywords`, `cast`, and `crew` are extracted using Python's `ast.literal_eval()` to convert JSON strings into Python objects.
   - The top 3 cast members and the director are extracted to reduce noise.
   - All these features are combined with the movie `overview` to form a new `tags` column.

2. **Text Vectorization**:
   - The `tags` column is transformed into numerical vectors using `CountVectorizer` from `scikit-learn`, which creates a matrix of token counts.
   - Only the top 5000 most frequent words are used and English stop words are removed to improve relevance.

3. **Similarity Calculation**:
   - Cosine similarity is calculated on the vectorized tags to determine how similar one movie is to others.
   - For a selected movie, the top 5 most similar movies are fetched (excluding the selected movie itself).

4. **Poster Retrieval**:
   - Each recommended movie's poster is fetched dynamically from **The Movie Database (TMDB)** using their API and displayed in the app.

---

## 🚀 Getting Started

Follow these steps to run the app locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
