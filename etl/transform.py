import pandas as pd
import os
from pandas import DataFrame
from .extract_api import extract_from_api
from .extract_web_rttm import RottenTomatoesScraper
from .extract_web_imdb import extract_imdb_rating_and_director
from dotenv import load_dotenv

load_dotenv()

def _get_number_of_movies(default: int = 15) -> int:
    raw = os.getenv("NUMBER_OF_MOVIES_TO_SCRAP")
    try:
        if raw is None:
            return default
        return int(raw)
    except (ValueError, TypeError):
        return default    

def transform() -> DataFrame:
    number_movies = _get_number_of_movies()
    movies = extract_from_api(number_movies)
    df = pd.DataFrame(movies)

    df = df[["id", "title", "original_title", "popularity", "release_date", "vote_average"]]

    scraper = RottenTomatoesScraper()

    print("Iniciando scraping no Rotten Tomatoes...")
    try:
        df["rttm_critic_score"] = df["title"].apply(
            lambda x: scraper.extract_rttm_critic_score(x) or "N/A"
        )
    finally:
        scraper.close()

    print("Iniciando scraping no IMDB...")

    imdb_info = df["title"].apply(
        lambda x: extract_imdb_rating_and_director(x) or {}
    )

    df["imdb_rating"] = imdb_info.apply(lambda x: x.get("rating", "N/A"))
    df["director"] = imdb_info.apply(lambda x: x.get("director", "N/A"))

    # Reordering columns
    columns = [
        "id",
        "title",
        "original_title",
        "director",
        "popularity",
        "release_date",
        "vote_average",
        "rttm_critic_score",
        "imdb_rating"
    ]
    df = df[columns]

    return df