from fastapi import FastAPI
import requests
import sqlite3
from typing import Any

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/sum")
def sum_ints(x: int = 0, y: int = 10):
    return x + y


@app.get("/geocode")
def geocode(lat: float, lon: float):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    headers = {"User-Agent": "PaulinaISSI/1.0"}
    response = requests.get(url, headers=headers)
    return response.json()


@app.get('/movies')
def get_movies():
    with sqlite3.connect('movies.db') as db:
        output = []
        cursor = db.cursor()
        cursor.execute('SELECT * FROM movies')
        for row in cursor:
            movie = {'id': f'{row[0]}', 'title': f'{row[1]}', 'year': f'{row[2]}', 'actors': f'{row[3]}', }
            output.append(movie)
        return output


@app.get('/movies/{movie_id}')
def get_single_movie(movie_id: int):
    with sqlite3.connect('movies.db') as db:
        cursor = db.cursor()
        row = cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()

        if row:
            movie = {
                'id': row[0],
                'title': row[1],
                'year': row[2],
                'actors': row[3]
            }
        else:
            movie = {'message': 'Movie not found'}

    return movie


@app.post("/movies")
def add_movie(params: dict[str, Any]):
    with sqlite3.connect('movies.db') as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
            (params["title"], params["year"], params["actors"])
        )
        db.commit()

    return {"message": f"Movie added successfully"}
