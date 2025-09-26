import requests
import re
import unicodedata
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def make_slug(title: str) -> str:
    slug = title.lower()
    
    # Remover acentos
    slug = unicodedata.normalize("NFKD", slug)
    slug = slug.encode("ascii", "ignore").decode("ascii")
    
    # Substituir espaços e alguns caracteres por "_"
    slug = re.sub(r"[ \-:]", "_", slug)
    
    # Remover outros caracteres não alfanuméricos
    slug = re.sub(r"[^a-z0-9_]", "", slug)
    
    # Remover múltiplos underscores consecutivos
    slug = re.sub(r"_+", "_", slug)
    
    # Remover underscores no início e fim
    slug = slug.strip("_")
    
    return slug

special_cases = {
    "the_fantastic_4_first_steps": "the_fantastic_four_first_steps",
}

def url_exists(url: str) -> bool:
    try:
        r = requests.head(url, allow_redirects=True)
        return r.status_code == 200
    except requests.RequestException:
        return False

class RottenTomatoesScraper:
    def __init__(self):
        # Chrome headless config
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        # Put the PATH to your ChromeDriver
        service = Service("/usr/local/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=options)


    def extract_rttm_critic_score(self, movie_title: str) -> str | None:
        slug = make_slug(movie_title)
        slug = special_cases.get(slug, slug)

        url = f"https://www.rottentomatoes.com/m/{slug}"
        print(f"Tentando acessar: {url}")

        if not url_exists(url):
            print(f"URL inválida: {url}")
            return None

        try:
            self.driver.get(url)

            rt_text = self.driver.find_element(By.CSS_SELECTOR, 'rt-text[slot="criticsScore"]')

            shadow = self.driver.execute_script('return arguments[0].shadowRoot', rt_text)

            inner = shadow.find_element(By.CSS_SELECTOR, 'span')
            tomatometer = inner.text
            print(f"Tomatometer: {tomatometer}")
            return tomatometer
        except Exception as e:
            print("Erro ao extrair: ", e)
            return None

    def close(self):
        self.driver.quit()