from typing import Any
from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()


@router.get('/movies_extended')
def get_extended_movies():
    """
    Retrieve all movies from the extended database.
    """
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
    """
    Retrieve a single movie by its unique ID.
    """
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
def add_extended_movie(params: dict[str, Any]):
    """
    Add a new movie to the extended database.
    Requires: title, director, year, description.
    """
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
def update_extended_movie(movie_id: int, params: dict[str, Any]):
    """
    Update details of an existing movie by ID.
    Replaces all fields: title, director, year, description.
    """
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
def delete_extended_movie(movie_id: int):
    """
    Delete a specific movie from the database by ID.
    """
    with sqlite3.connect('movies-extended.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM movie WHERE id = ?", (movie_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")

    return


@router.delete("/movies_extended")
def delete_extended_all_movies():
    """
    Delete ALL movies from the extended database.
    """
    with sqlite3.connect('movies-extended.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM movie")
        db.commit()
        deleted_count = cursor.rowcount

    return {"message": f"Deleted all movies. Total removed: {deleted_count}"}


@router.get("/movies_extended_search")
def search_extended_movies(characteristic: str):
    """
    Search for movies by matching title or director.
    """
    with sqlite3.connect('movies-extended.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM movie WHERE title LIKE ? OR director LIKE ?",
                              ("%" + characteristic + "%", "%" + characteristic + "%",)).fetchall()
        if rows:
            return [dict(row) for row in rows]
        else:
            return {'message': 'Movie not found'}


@router.get('/actors')
def get_all_actors():
    """
    Retrieve all actors from the extended database.
    """
    try:
        with sqlite3.connect('movies-extended.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute('SELECT * FROM actor')
            rows = cursor.fetchall()

            output = [
                {
                    'id': row['id'],
                    'name': row['name'],
                    'surname': row['surname'],
                }
                for row in rows
            ]
            return output

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")


@router.get("/actors/{actor_id:int}")
def search_actors(actor_id):
    """
    Retrieve a single actor by their unique ID.
    """
    with sqlite3.connect('movies-extended.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        row = cursor.execute("SELECT * FROM actor WHERE id = ?", (actor_id,)).fetchone()

        if row:
            return dict(row)
        else:
            return {'message': 'Movie not found'}


@router.post("/actors")
def add_actor(params: dict[str, Any]):
    """
    Add a new actor to the extended database (actors table).
    Requires: name, surname.
    """
    try:
        with sqlite3.connect('movies-extended.db') as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO actor (name, surname) VALUES (?, ?)",
                (params["name"], params["surname"])
            )
            db.commit()
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"You are missing a required field: {e}"
        )

    return {"message": f"Actor {params} added successfully"}


@router.put("/actors/{actor_id}")
def update_actors(actor_id: int, params: dict[str, Any]):
    """
    Update details of an existing actor by ID.
    Replaces both fields: name, surname.
    """
    try:
        with sqlite3.connect('movies-extended.db') as db:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE actor SET name=?, surname=? WHERE id=?",
                (params["name"], params["surname"], actor_id)
            )
            db.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"You are missing a required field: {e}"
        )

    return {"message": "Actors updated successfully"}


@router.delete("/actors/{actor_id}", status_code=204)
def delete_actor(actor_id: int):
    """
    Delete a specific actor from the database by ID.
    """
    with sqlite3.connect('movies-extended.db') as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM actor WHERE id = ?", (actor_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")

    return
