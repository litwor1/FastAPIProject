A RESTful API built with **FastAPI** for managing movie databases.

This project was created to practice FastAPI framework.

The project was created for ISSI labs, following the instructions at https://moodle.lab.ii.agh.edu.pl/mod/page/view.php?id=23330


## 🚀 Features

* **Dual Database Support:**
* **Basic Movies:** simple management of movies (Title, Year, Actors as string).
* **Extended Movies:** Relational management separating Movies and Actors, linked via a junction table.


* **CRUD Operations:** Create, Read, Update, and Delete endpoints for Movies and Actors.
* **Search Functionality:** Filter movies by title, director, or actor names.
* **Relational Queries:** Fetch all actors associated with a specific movie ID.
* **External API Integration:** Geocoding endpoint using OpenStreetMap (Nominatim).
* **Clean Architecture:** Refactored database logic using dedicated helper functions (`select`, `modify`, `delete`) with
  automatic transaction handling.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** FastAPI
* **Database:** SQLite3
* **Utilities:** Requests (for Geocoding)

## 📂 Project Structure

* `main.py`: The entry point of the application. Contains the basic `/movies` endpoints and mounts the extended router.
* `movies_extended_endpoints.py`: Contains the logic for the relational database (Movies, Actors, and their
  connections).
* `movies.db`: SQLite database for the basic implementation.
* `movies-extended.db`: SQLite database for the relational implementation.
* `*.http` files: HTTP request files for testing endpoints directly in VS Code or similar IDEs.

## ⚙️ Installation & Setup

1. **Clone the repository** (or download the files):

```bash
git clone https://github.com/litwor1/FastAPIProject.git
cd FastAPIProject

```

2. **Install dependencies**:
   The project includes a `requirements.txt` file, so you can install all necessary packages with one command:

```bash
pip install -r requirements.txt

```

3. **Run the Server**:

```bash
uvicorn main:app --reload

```


## 🔌 API Endpoints

### 🎬 Extended Movies (Relational)

| Method   | Endpoint                       | Description                             |
|----------|--------------------------------|-----------------------------------------|
| `GET`    | `/movies_extended`             | Get all movies                          |
| `GET`    | `/movies_extended/{id}`        | Get a single movie by ID                |
| `POST`   | `/movies_extended`             | Add a new movie                         |
| `PUT`    | `/movies_extended/{id}`        | Update movie details                    |
| `DELETE` | `/movies_extended/{id}`        | Delete a movie                          |
| `GET`    | `/movies_extended_search`      | Search movies by title or director      |
| `GET`    | `/movies_extended/{id}/actors` | **Get all actors for a specific movie** |

### 🎭 Actors

| Method   | Endpoint       | Description          |
|----------|----------------|----------------------|
| `GET`    | `/actors`      | Get all actors       |
| `GET`    | `/actors/{id}` | Get a single actor   |
| `POST`   | `/actors`      | Add a new actor      |
| `PUT`    | `/actors/{id}` | Update actor details |
| `DELETE` | `/actors/{id}` | Delete an actor      |

### 🎥 Basic Movies

| Method   | Endpoint       | Description                             |
|----------|----------------|-----------------------------------------|
| `GET`    | `/movies`      | Get all movies                          |
| `POST`   | `/movies`      | Add a new movie                         |
| `PUT`    | `/movies/{id}` | Update a movie                          |
| `DELETE` | `/movies/{id}` | Delete a movie                          |
| `GET`    | `/moviesearch` | Search movies by title or actors string |

### 🌍 Utilities

| Method | Endpoint   | Description                                              |
|--------|------------|----------------------------------------------------------|
| `GET`  | `/geocode` | Reverse geocoding (Lat/Lon to Address) via OpenStreetMap |
| `GET`  | `/sum`     | Simple integer addition                                  |

## 🧪 Testing

The project includes `.http` files for easy testing of API endpoints without a browser:

* `test_api.http`: Tests for the basic `/movies` endpoints.
* `test_actors.http`: Tests for actors and extended movie relationships.
* `test_extended_api.http`: Tests for the extended movie CRUD operations.