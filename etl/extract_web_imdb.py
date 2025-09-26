import requests
from typing import Optional, Dict, List
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}

def search_imdb(movie_title: str) -> str | None:
    query = quote_plus(movie_title)
    url = f"https://www.imdb.com/find?q={query}&s=tt&ttype=ft&ref_=fn_ft"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    first_result = soup.select_one("a.ipc-metadata-list-summary-item__t")

    if first_result:
        print("Filme encontrado no IMDB!")
        imdb_id = first_result["href"].split("/")[2]
        print(f"imdb_id: {imdb_id}")
        return f"https://www.imdb.com/title/{imdb_id}/"
    return None

def extract_imdb_rating_and_director(movie_title: str) -> Optional[Dict[str, str]]:
    imdb_url = search_imdb(movie_title)

    if imdb_url:
        res = requests.get(imdb_url, headers=HEADERS)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        result: Dict[str, str] = {}

        rating_block = soup.select_one('div[data-testid="hero-rating-bar__aggregate-rating__score"]')
        if rating_block:
            rating_span = rating_block.find("span")
            if rating_span:
                result["rating"] = rating_span.get_text(strip=True)

        director_block = soup.select_one('div[class="ipc-metadata-list-item__content-container"]')
        if director_block:
            directors = [a.get_text(strip=True) for a in director_block.select('a')]
            if directors:
                result["director"] = ", ".join(directors)

        return result or None
    
    return None
