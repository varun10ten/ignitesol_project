## Gutendex FastAPI Service

This project exposes a FastAPI-based HTTP API on top of the Project Gutenberg / Gutendex SQL dump.

### 1. Prepare the database

1. Install MySQL or MariaDB locally or on a server.
2. Create a database (for example `gutendex`).
3. Load the dump:

```bash
mysql -u YOUR_USER -p gutendex < data/gutendex.sql
```

4. Set the `DATABASE_URL` environment variable to point to your database, for example:

```bash
export DATABASE_URL="mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/gutendex"
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 4. API usage

- `GET /books` – list books matching zero or more filters.

Query parameters (all optional, multiple values allowed by repeating the parameter):

- `book_id` – Gutenberg book ID(s), e.g. `?book_id=1342&book_id=84`
- `language` – language code(s), e.g. `?language=en&language=fr`
- `mime_type` – MIME type(s), e.g. `?mime_type=text/plain&mime_type=application/epub+zip`
- `topic` – partial, case-insensitive match against subjects or bookshelves, e.g. `?topic=child`
- `author` – partial, case-insensitive match against author name, e.g. `?author=austen`
- `title` – partial, case-insensitive match against book title, e.g. `?title=pride`
- `page` – page number (1-based, default 1)
- `page_size` – page size (max 25, default 25)

Response JSON:

```json
{
  "count": 1234,
  "page": 1,
  "page_size": 25,
  "results": [
    {
      "id": 1,
      "gutenberg_id": 1342,
      "title": "Pride and Prejudice",
      "authors": [
        {"name": "Austen, Jane", "birth_year": 1775, "death_year": 1817}
      ],
      "genre": null,
      "languages": ["en"],
      "subjects": ["Courtship -- Fiction", "..."],
      "bookshelves": ["Best Books Ever Listings", "..."],
      "formats": [
        {"mime_type": "text/plain", "url": "https://..."},
        {"mime_type": "application/epub+zip", "url": "https://..."}
      ]
    }
  ]
}
```

To make the API publicly accessible, deploy this FastAPI app to a hosting platform that supports Python web apps (for example, a cloud VM, Fly.io, Render, Railway, etc.) and set the `DATABASE_URL` there pointing to a database that has the `gutendex.sql` loaded.


