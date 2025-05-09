🎬 Movie Recommender System
A personalized movie recommendation system built using Python. This project combines both content-based filtering and collaborative filtering to suggest movies based on user preferences.

📌 Features
Content-Based Filtering using movie genres, tags, cast, and crew

Collaborative Filtering using user ratings (optional)

User-friendly interface to input movie name and get recommendations

Cast info, poster, and overview for each recommended movie

Built with Python and deployed using Streamlit / Flask

🛠️ Tech Stack
Python

Pandas, NumPy

Scikit-learn (TF-IDF, Nearest Neighbors, Cosine Similarity)

NLTK / spaCy (for text preprocessing)

TMDB API (for posters and movie metadata)

Streamlit / Flask (for UI)

🗂️ Project Structure
movie-recommender/
├── app.py                   # Main app script (Streamlit/Flask)
├── recommender.py           # Core recommendation logic
├── movies.csv               # Processed movie metadata
├── similarity.pkl           # Precomputed similarity matrix
├── tmdb_api.py              # Fetches posters & details via API
├── templates/               # HTML templates (if using Flask)
├── static/                  # CSS or images (if needed)
├── requirements.txt

📈 Recommendation Methods
✅ Content-Based Filtering
1.Combines features like genres, overview, keywords, cast, and crew
2.Converts them into a combined text "soup"
3.Uses TF-IDF or Count Vectorizer + Cosine Similarity to find similar movies

🔍 Example
Enter: "Inception"

Output Recommendations:

Interstellar

The Prestige

The Matrix

Shutter Island

Memento

Each recommendation shows:

🎞️ Movie title

🖼️ Poster

🧑 Cast (optional)

📝 Short overview

📦 Requirements
Python 3.7+

pandas, numpy, scikit-learn

requests

streamlit / flask

nltk (optional for stemming/lemmatization)
