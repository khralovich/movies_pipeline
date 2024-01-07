import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")

# https://developer.themoviedb.org/reference/intro/getting-started
url = "https://api.themoviedb.org/3/movie/popular"
img_url = "https://image.tmdb.org/t/p/w1280"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}"
}

try:
    response = requests.get(url, headers=headers)
    print(response.text)
except NameError:
    print(NameError)
finally:
    print("The 'try except' is finished")
