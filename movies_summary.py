from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
import pendulum
from airflow.decorators import dag, task
import requests
import xmltodict
import json

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

# configure a dag


@dag(
    dag_id='movies_summary',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2023, 1, 6),
    catchup=False
)
def movies_summary():
    # create a db connection task
    create_database = SqliteOperator(
        task_id="create_table_sqlite",
        sql=r"""
    CREATE TABLE IF NOT EXISTS movies (
        id TEXT PRIMARY KEY
        , title TEXT
        , description TEXT
        , original_lang TEXT
        , vote_average TEXT
        , poster TEXT
        , release_date DATE
    )
    """,
        sqlite_conn_id="popmoviesid"
    )
    # get data from api

    @task()
    def get_movies():
        response = requests.get(url, headers=headers)
        data = response.text
        return data
    # connect operators
    popular_movies = get_movies()  # this is step nr2
    create_database.set_downstream(popular_movies)  # this is step nr1

    @task()
    def load_movies(movies):
        hook = SqliteHook(sqlite_conn_id="popmoviesid")
        new_movies = []
        movies_data = json.loads(movies)
        for movie in movies_data.get("results", []):
            new_movies.append([
                str(movie.get("id")),
                movie.get("title"),
                movie.get("overview"),
                movie.get("original_language"),
                str(movie.get("vote_average")),
                movie.get("poster_path"),
                movie.get("release_date")
            ])
        fields = ["id", "title", "description",
                  "original_lang", "vote_average", "poster", "release_date"]
        hook.insert_rows(table="movies", rows=new_movies, target_fields=fields)
    load_movies(popular_movies)  # this is step #3


summary = movies_summary()
