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
