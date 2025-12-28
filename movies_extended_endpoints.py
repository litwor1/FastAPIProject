from typing import Any
from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()


def connect_to_db():
    db = sqlite3.connect('movies-extended.db')
    db.row_factory = sqlite3.Row
    return db


@router.get('/movies_extended')
def get_extended_movies():
    """
    Retrieve all movies from the extended database.
    """
    db = connect_to_db()
    cursor = db.cursor()

    try:
        query = 'SELECT * FROM movie'
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")
    finally:
        db.close()


@router.get('/movies_extended/{movie_id}')
def get_single_movie(movie_id: int):
    """
    Retrieve a single movie by its unique ID.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = 'SELECT * FROM movie WHERE id = ?'
        row = cursor.execute(query, (movie_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
        return dict(row)
    finally:
        db.close()


@router.post("/movies_extended")
def add_extended_movie(params: dict[str, Any]):
    """
    Add a new movie to the extended database.
    Requires: title, director, year, description.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = "INSERT INTO movie (title, director, year, description) VALUES (?, ?, ?, ?)"
        cursor.execute(
            query,
            (params["title"], params["director"], params["year"], params["description"])
        )
        db.commit()
        return {"message": f"Movie {params} added successfully"}
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"You are missing a required field: {e}"
        )
    finally:
        db.close()


@router.put("/movies_extended/{movie_id}")
def update_extended_movie(movie_id: int, params: dict[str, Any]):
    """
    Update details of an existing movie by ID.
    Replaces all fields: title, director, year, description.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = "UPDATE movie SET title=?, director=?, year=?, description=? WHERE id=?"
        cursor.execute(
            query,
            (params["title"], params["director"], params["year"], params["description"], movie_id)
        )
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
        return {"message": "Movie updated successfully"}
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"You are missing a required field: {e}"
        )
    finally:
        db.close()


@router.delete("/movies_extended/{movie_id}", status_code=204)
def delete_extended_movie(movie_id: int):
    """
    Delete a specific movie from the database by ID.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = "DELETE FROM movie WHERE id = ?"
        cursor.execute(query, (movie_id,))
        db.commit()
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")

    finally:
        db.close()


@router.delete("/movies_extended")
def delete_extended_all_movies():
    """
    Delete ALL movies from the extended database.
    """
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM movie"
    cursor.execute(query)
    db.commit()
    deleted_count = cursor.rowcount
    db.close()
    return {"message": f"Deleted all movies. Total removed: {deleted_count}"}


@router.get("/movies_extended_search")
def search_extended_movies(characteristic: str):
    """
    Search for movies by matching title or director.
    """
    db = connect_to_db()
    cursor = db.cursor()
    query = "SELECT * FROM movie WHERE title LIKE ? OR director LIKE ?"
    rows = cursor.execute(query, ("%" + characteristic + "%", "%" + characteristic + "%",)).fetchall()
    if rows:
        return [dict(row) for row in rows]
    else:
        return {'message': 'Movie not found'}


@router.get('/actors')
def get_all_actors():
    """
    Retrieve all actors from the extended database.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = 'SELECT * FROM actor'
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")


@router.get("/actors/{actor_id:int}")
def search_actors(actor_id):
    """
    Retrieve a single actor by their unique ID.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = "SELECT * FROM actor WHERE id = ?"
        row = cursor.execute(query, (actor_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
        return dict(row)
    finally:
        db.close()


@router.post("/actors")
def add_actor(params: dict[str, Any]):
    """
    Add a new actor to the extended database (actors table).
    Requires: name, surname.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = "INSERT INTO actor (name, surname) VALUES (?, ?)"
        cursor.execute(
            query,
            (params["name"], params["surname"])
        )
        db.commit()
        return {"message": f"Actor {params} added successfully"}

    except KeyError as e:
        raise HTTPException(status_code=400)
    finally:
        db.close()


@router.put("/actors/{actor_id}")
def update_actors(actor_id: int, params: dict[str, Any]):
    """
    Update details of an existing actor by ID.
    Replaces both fields: name, surname.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = "UPDATE actor SET name=?, surname=? WHERE id=?"
        cursor.execute(query, (params["name"], params["surname"], actor_id))
        db.commit()
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
        return {"message": "Actors updated successfully"}

    except KeyError as e:
        raise HTTPException(status_code=400)
    finally:
        db.close()


@router.delete("/actors/{actor_id}", status_code=204)
def delete_actor(actor_id: int):
    """
    Delete a specific actor from the database by ID.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = "DELETE FROM actor WHERE id = ?"
        cursor.execute(query, (actor_id,))
        db.commit()
        if not cursor.rowcount:
            raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
    finally:
        db.close()


@router.get("/movies_extended/{movie_id}/actors")
def get_actors_for_movie(movie_id: int):
    """
    Fetches a list of actors for a specific movie identified by its ID.
    """
    db = connect_to_db()
    cursor = db.cursor()
    try:
        query = """
                SELECT actor.name, actor.surname
                FROM actor
                         JOIN movie_actor_through ON actor.id = movie_actor_through.actor_id
                WHERE movie_actor_through.movie_id = ? \
                """
        cursor.execute(query, (movie_id,))
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
        return [dict(row) for row in rows]
    finally:
        db.close()
