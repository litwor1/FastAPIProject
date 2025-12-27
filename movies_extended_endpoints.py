from typing import Any

from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()


@router.get('/movies_extended')
def get_extended_movies():
    try:
        with sqlite3.connect('movies-extended.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute('SELECT * FROM movie')
            rows = cursor.fetchall()

            output = [
                {
                    'id': row['id'],
                    'title': row['title'],
                    'director': row['director'],
                    'year': row['year'],
                    'description': row['description']
                }
                for row in rows
            ]
            return output

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")


@router.get('/movies_extended/{movie_id}')
def get_single_movie(movie_id: int):
    with sqlite3.connect('movies-extended.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        row = cursor.execute('SELECT * FROM movie WHERE id = ?', (movie_id,)).fetchone()

        if row:
            movie = {
                'id': row['id'],
                'title': row['title'],
                'director': row['director'],
                'year': row['year'],
                'description': row['description']
            }
        else:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")

    return movie


@router.post("/movies_extended")
def add_movie(params: dict[str, Any]):
    try:
        with sqlite3.connect('movies-extended.db') as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO movie (title, director, year, description) VALUES (?, ?, ?, ?)",
                (params["title"], params["director"], params["year"], params["description"])
            )
            db.commit()
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"You are missing a required field: {e}"
        )

    return {"message": f"Movie {params} added successfully"}


@router.put("/movies_extended/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    try:
        with sqlite3.connect('movies-extended.db') as db:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE movie SET title=?, director=?, year=?, description=? WHERE id=?",
                (params["title"], params["director"], params["year"], params["description"], movie_id)
            )
            db.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"You are missing a required field: {e}"
        )

    return {"message": "Movie updated successfully"}


@router.delete("/movies_extended/{movie_id}", status_code=204)
def delete_movie(movie_id: int):
    with sqlite3.connect('movies-extended.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM movie WHERE id = ?", (movie_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")

    return


@router.delete("/movies_extended")
def delete_all_movies():
    with sqlite3.connect('movies-extended.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM movie")
        db.commit()
        deleted_count = cursor.rowcount

    return {"message": f"Deleted all movies. Total removed: {deleted_count}"}


@router.get("/movies_extended_search")
def search_movies(characteristic: str):
    with sqlite3.connect('movies-extended.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM movie WHERE title LIKE ? OR director LIKE ?",
                              ("%" + characteristic + "%", "%" + characteristic + "%",)).fetchall()
        if rows:
            return [dict(row) for row in rows]
        else:
            return {'message': 'Movie not found'}
