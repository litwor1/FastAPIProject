from typing import Any
from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

# ENDPOINTS

@router.get('/movies_extended')
def get_extended_movies():
    """
    Retrieve all movies from the extended database.
    """
    return execute_select('SELECT * FROM movie')


@router.get('/movies_extended/{movie_id}')
def get_single_movie(movie_id: int):
    """
    Retrieve a single movie by its unique ID.
    """
    rows = execute_select('SELECT * FROM movie WHERE id = ?', (movie_id,))
    if not rows:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
    return rows[0]


@router.post("/movies_extended")
def add_extended_movie(params: dict[str, Any]):
    """
    Add a new movie to the extended database.
    """
    try:
        args = (params["title"], params["director"], params["year"], params["description"])
        execute_modify(
            "INSERT INTO movie (title, director, year, description) VALUES (?, ?, ?, ?)",
            args
        )
        return {"message": f"Movie {params} added successfully"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"You are missing a required field: {e}")


@router.put("/movies_extended/{movie_id}")
def update_extended_movie(movie_id: int, params: dict[str, Any]):
    """
    Update details of an existing movie by ID.
    """
    try:
        args = (params["title"], params["director"], params["year"], params["description"], movie_id)

        row_count = execute_modify(
            "UPDATE movie SET title=?, director=?, year=?, description=? WHERE id=?",
            args
        )

        if not row_count:
            raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
        return {"message": "Movie updated successfully"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"You are missing a required field: {e}")


@router.delete("/movies_extended/{movie_id}")
def delete_extended_movie(movie_id: int):
    """
    Delete a specific movie from the database by ID.
    """
    row_count = execute_delete("DELETE FROM movie WHERE id = ?", (movie_id,))

    if not row_count:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found")
    return {"message": f"Deleted movie ID: {movie_id}"}


@router.delete("/movies_extended")
def delete_extended_all_movies():
    """
    Delete ALL movies from the extended database.
    """
    row_count = execute_delete("DELETE FROM movie")
    return {"message": f"Deleted all movies. Total removed: {row_count}"}


@router.get("/movies_extended_search")
def search_extended_movies(characteristic: str):
    """
    Search for movies by matching title or director.
    """
    search_term = "%" + characteristic + "%"
    rows = execute_select(
        "SELECT * FROM movie WHERE title LIKE ? OR director LIKE ?",
        (search_term, search_term)
    )

    if not rows:
        raise HTTPException(status_code=404, detail=f"Movie not found")
    return rows


@router.get('/actors')
def get_all_actors():
    """
    Retrieve all actors from the extended database.
    """
    return execute_select('SELECT * FROM actor')


@router.get("/actors/{actor_id:int}")
def search_actors(actor_id):
    """
    Retrieve a single actor by their unique ID.
    """
    rows = execute_select("SELECT * FROM actor WHERE id = ?", (actor_id,))
    if not rows:
        raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
    return rows[0]


@router.post("/actors")
def add_actor(params: dict[str, Any]):
    """
    Add a new actor.
    """
    try:
        args = (params["name"], params["surname"])
        execute_modify("INSERT INTO actor (name, surname) VALUES (?, ?)", args)
        return {"message": f"Actor {params} added successfully"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"You are missing a required field: {e}")


@router.put("/actors/{actor_id}")
def update_actors(actor_id: int, params: dict[str, Any]):
    """
    Update details of an existing actor by ID.
    """
    try:
        args = (params["name"], params["surname"], actor_id)
        row_count = execute_modify("UPDATE actor SET name=?, surname=? WHERE id=?", args)

        if not row_count:
            raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
        return {"message": "Actors updated successfully"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"You are missing a required field: {e}")


@router.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    """
    Delete a specific actor from the database by ID.
    """
    row_count = execute_delete("DELETE FROM actor WHERE id = ?", (actor_id,))

    if not row_count:
        raise HTTPException(status_code=404, detail=f"Actor with ID {actor_id} not found")
    return {"message": f"Actor with ID {actor_id} deleted successfully"}


@router.get("/movies_extended/{movie_id}/actors")
def get_actors_for_movie(movie_id: int):
    query = """
            SELECT actor.name, actor.surname
            FROM actor
                     JOIN movie_actor_through ON actor.id = movie_actor_through.actor_id
            WHERE movie_actor_through.movie_id = ?
            """
    rows = execute_select(query, (movie_id,))

    if not rows:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found or no actors assigned")
    return rows

# MAIN FUNCTIONS

def connect_to_db():
    db = sqlite3.connect('movies-extended.db')
    db.row_factory = sqlite3.Row
    return db


def execute_select(query: str, args: tuple = ()) -> list[dict]:
    """
    Manages select
    """
    db = connect_to_db()
    try:
        cursor = db.execute(query, args)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")
    finally:
        db.close()


def execute_modify(query: str, args: tuple = ()) -> int:
    """
    INSERT or UPDATE
    """
    db = connect_to_db()
    try:
        with db:
            cursor = db.execute(query, args)
        return cursor.rowcount
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")
    finally:
        db.close()


def execute_delete(query: str, args: tuple = ()) -> int:
    """
    DELETE
    """
    db = connect_to_db()
    try:
        with db:
            cursor = db.execute(query, args)
        return cursor.rowcount
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")
    finally:
        db.close()
