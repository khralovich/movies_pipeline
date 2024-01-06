import requests
import json
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


OMDB_API_KEY = os.getenv("OMDB_API_KEY")


request_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&y=2006&s=duna&plot=full"
response = requests.get(request_url)

print(response.json())
print(response.status_code)
