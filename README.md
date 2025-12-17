## Gutendex FastAPI Service

This project exposes a FastAPI-based HTTP API on top of the Project Gutenberg / Gutendex SQL dump.

### 1. Prepare the database

1. Install MySQL locally or on a server.
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

And for the testing part we need to add /docs to the url. Eg:
http://127.0.0.1:8000/docs

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

So for that we need to make sure docker is installed in our system.
Then create the .env File.
# .env file content
MYSQL_DATABASE=gutendex
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=rootpassword

# This URL connects the FastAPI app to the MySQL container within the Docker network
DATABASE_URL="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@gutendex-mysql:3306/${MYSQL_DATABASE}"
2. Run Docker Compose
docker-compose up --build -d
Access the API
http://localhost:8000/docs --> swagger documentaion
# 📚 Gutendex FastAPI Service

This project exposes a FastAPI-based HTTP API for searching and filtering books, built on top of the Project Gutenberg / Gutendex SQL data dump.

## 🚀 Setup & Deployment

The recommended method is **Containerized Deployment** using Docker Compose.

### Option 1: 🐳 Containerized Deployment (Recommended)

#### 1. Prerequisites
Ensure **Docker Desktop** is installed and running, and no other process is using port 3306 (e.g., local MySQL).

#### 2. Environment Configuration
Create a file named **`.env`** in the project root:

```env
MYSQL_DATABASE=gutendex
MYSQL_USER=your_docker_user
MYSQL_PASSWORD=your_secure_password
MYSQL_ROOT_PASSWORD=your_root_password_for_mysql
DATABASE_URL="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@gutendex-mysql:3306/${MYSQL_DATABASE}"
docker-compose up --build -d

Option 2:
💻 Local Development
1. prepare the database
export DATABASE_URL="mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/gutendex"
2. install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
3. Run the API
uvicorn app.main:app --reload
🌐 API Usage
The API is available at http://127.0.0.1:8000.
Documentation

    Swagger UI: http://127.0.0.1:8000/docs
This is the consolidated guide for your project, starting from setting up your development environment to running the application using the recommended Docker Compose method.

I have included the environment setup, deployment commands, verification steps, and the complete README.md content in one frame.
🌟 Project Deployment and Setup Guide

This guide assumes you are starting from the project directory (C:\Users\varun\OneDrive\Desktop\New folder\ignite_sol_project).
Part 1: Prerequisites & Conflict Resolution
1. Install Docker Desktop

    Ensure Docker Desktop is installed and running on your Windows machine.

2. Stop Local MySQL (Critical)

    You must free up port 3306, which is used by the Dockerized MySQL container.

    Action: Go to Windows Services (services.msc), find the service named "MySQL80" (or similar), and Stop it.

3. Resolve Docker Context (Verification)

    Ensure your Docker client is pointing to the Linux engine:
    Bash

    docker context use desktop-linux

Part 2: Environment Setup & Deployment
1. Create the .env File

Create a file named .env in your project's root directory and define the credentials.
Code snippet

# .env file content
MYSQL_DATABASE=gutendex
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=rootpassword

# This URL connects the FastAPI app to the MySQL container within the Docker network
DATABASE_URL="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@gutendex-mysql:3306/${MYSQL_DATABASE}"

2. Run Docker Compose

This single command builds your application image, pulls the MySQL image, creates the network, and starts both services in the background.
Bash

docker-compose up --build -d

Part 3: Verification and API Access
1. Check Container Status

Verify that both containers are running without errors. The STATUS column should show Up....
Bash

docker ps

2. Access the API

Your FastAPI application is now running on port 8000 of your host machine.

    Swagger Documentation (Recommended Test Site):

    http://localhost:8000/docs

    Redoc Documentation:

    http://localhost:8000/redoc

3. Stop and Cleanup

To stop and remove all services (containers and network):
Bash

docker-compose down

To remove the data volume as well (deleting the database data):
Bash

docker-compose down --volumes

Part 4: Complete README.md
Markdown

# 📚 Gutendex FastAPI Service

This project exposes a FastAPI-based HTTP API for searching and filtering books, built on top of the Project Gutenberg / Gutendex SQL data dump.

## 🚀 Setup & Deployment

The recommended method is **Containerized Deployment** using Docker Compose.

### Option 1: 🐳 Containerized Deployment (Recommended)

#### 1. Prerequisites
Ensure **Docker Desktop** is installed and running, and no other process is using port 3306 (e.g., local MySQL).

#### 2. Environment Configuration
Create a file named **`.env`** in the project root:

```env
MYSQL_DATABASE=gutendex
MYSQL_USER=your_docker_user
MYSQL_PASSWORD=your_secure_password
MYSQL_ROOT_PASSWORD=your_root_password_for_mysql
DATABASE_URL="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@gutendex-mysql:3306/${MYSQL_DATABASE}"

3. Build and Run the Stack
Bash

docker-compose up --build -d

4. Cleanup

To stop and remove containers/network:
Bash

docker-compose down

Option 2: 💻 Local Development
1. Prepare the Database

    Install MySQL locally.

    Load the dump: mysql -u YOUR_USER -p gutendex < data/gutendex.sql

    Set the DATABASE_URL environment variable:

Bash

export DATABASE_URL="mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/gutendex"

2. Install Dependencies
Bash

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Run the API
Bash

uvicorn app.main:app --reload

🌐 API Usage

The API is available at http://127.0.0.1:8000.
Documentation

    Swagger UI: http://127.0.0.1:8000/docs

GET /books – List Books
Query Parameter	Description	Example
book_id	Gutenberg book ID(s).	?book_id=1342
language	Language code(s).	?language=en
topic	Partial match against subjects/bookshelves.	?topic=child
author	Partial match against author name.	?author=austen
title	Partial match against book title.	?title=pride
page	Page number (default 1).	?page=5
page_size	Page size (max 25, default 25).	?page_size=10

Response JSON Structure:
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
      "languages": ["en"],
      "subjects": ["Courtship -- Fiction", "..."],
      "formats": [
        {"mime_type": "text/plain", "url": "https://..."}
      ]
    }
  ]
}

