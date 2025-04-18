from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import requests

app = Flask(__name__)
CORS(app, resources={r"/movies": {"origins": "*"}})  # Zezwalaj na wszystkie domeny dla prostoty

API_KEY = "5da8ff81"
CSV_PATH = "NetflixViewingHistory.csv"

def get_movie_details(title):
    try:
        print(f"Pobieram dane dla: {title}")
        url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data["Response"] == "True":
            return {
                "title": data.get("Title", title),
                "description": data.get("Plot", "Brak"),
                "genres": data.get("Genre", "Brak"),
                "release_date": data.get("Released", "Brak"),
                "poster": data.get("Poster", "")
            }
        print(f"Nie znaleziono: {title}")
        return {
            "title": title,
            "description": "Nie znaleziono",
            "genres": "Brak",
            "release_date": "Brak",
            "poster": ""
        }
    except Exception as e:
        print(f"Błąd dla {title}: {e}")
        return {
            "title": title,
            "description": "Błąd API",
            "genres": "Brak",
            "release_date": "Brak",
            "poster": ""
        }

@app.route("/movies", methods=["GET"])
def get_movies():
    try:
        df = pd.read_csv(CSV_PATH)
        print("CSV wczytany, liczba wierszy:", len(df))
        movies = [get_movie_details(title) for title in df["Title"]]
        return jsonify(movies)
    except FileNotFoundError:
        print("Błąd: Plik CSV nie znaleziony!")
        return jsonify({"error": "Plik CSV nie znaleziony!"}), 404
    except KeyError:
        print("Błąd: Brak kolumny 'Title' w CSV!")
        return jsonify({"error": "Brak kolumny 'Title' w CSV!"}), 400
    except Exception as e:
        print("Błąd:", e)
        return jsonify({"error": "Coś poszło nie tak!"}), 500