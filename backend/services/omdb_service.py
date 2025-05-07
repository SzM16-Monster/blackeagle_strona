# -*- coding: utf-8 -*-
import requests
import logging
from urllib.parse import quote
from config import Config

logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def get_movie_from_omdb(title):
    url = f'http://www.omdbapi.com/?t={quote(title)}&apikey={Config.OMDB_API_KEY}'
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return data
            else:
                logging.warning(f"Movie not found in OMDB: {title}")
                return None
        else:
            logging.error(f"API error for {title}: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Request error for {title}: {e}")
        return None