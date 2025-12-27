from fastapi import FastAPI, HTTPException
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


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    with sqlite3.connect('movies.db') as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE movies SET title=?, year=?, actors=? WHERE id=?",
            (params["title"], params["year"], params["actors"], movie_id)
        )
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")

    return {"message": "Movie updated successfully"}


@app.delete("/movies/{movie_id}", status_code=204)  # 204 = No Content (sukces, ale bez treści)
def delete_movie(movie_id: int):
    with sqlite3.connect('movies.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")

    return


@app.delete("/movies")
def delete_all_movies():
    with sqlite3.connect('movies.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM movies")
        db.commit()
        deleted_count = cursor.rowcount

    return {"message": f"Deleted all movies. Total removed: {deleted_count}"}


@app.get("/moviesearch")
def search_movies(characteristic: str):
    with sqlite3.connect('movies.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM movies WHERE title LIKE ? OR actors LIKE ?",
                              ("%" + characteristic + "%", "%" + characteristic + "%",)).fetchall()
        if rows:
            return [dict(row) for row in rows]
        else:
            return {'message': 'Movie not found'}
