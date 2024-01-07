from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
import pendulum
from airflow.decorators import dag, task
import requests
import xmltodict

import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")
url = "https://api.themoviedb.org/3/movie/popular?language=us-US&page=1&region=ISO%203166-2%3APL"
img_url = "https://image.tmdb.org/t/p/w1280"


headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}"
}


@dag(
    dag_id='movies_summary',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2023, 1, 6),
    catchup=False
)
def movies_summary():
    @task()
    def get_movies():
        response = requests.get(url, headers=headers)
        data = response.text
        return data

    movies = get_movies()


summary = movies_summary()
