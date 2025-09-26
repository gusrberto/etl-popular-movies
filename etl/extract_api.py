import requests
import os
import math
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/popular"

def extract_from_api(number_of_movies: int):
    movies = []
    page_size = 20
    total_pages = math.ceil(number_of_movies / page_size)

    for page in range(1, total_pages + 1):
        params = {
            "api_key": API_KEY,
            "page": page
        }
        res = requests.get(BASE_URL, params=params)
        res.raise_for_status()
        data = res.json()
        movies.extend(data["results"])

    return movies[:number_of_movies]
