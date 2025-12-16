from typing import List, Optional

from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from .database import get_db
from .models import Book, Author, Format, Language, Subject, Bookshelf
from .schemas import BookListResponse, BookSchema, AuthorSchema, FormatSchema


app = FastAPI(title="Gutendex Books API")


@app.get("/books", response_model=BookListResponse)
def list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=25),
    book_ids: Optional[List[int]] = Query(None, alias="book_id"),
    languages: Optional[List[str]] = Query(None, alias="language"),
    mime_types: Optional[List[str]] = Query(None, alias="mime_type"),
    topics: Optional[List[str]] = Query(None, alias="topic"),
    authors: Optional[List[str]] = Query(None, alias="author"),
    titles: Optional[List[str]] = Query(None, alias="title"),
    db: Session = Depends(get_db),
) -> BookListResponse:
    """
    Retrieve books with optional filters and pagination.

    - Multiple values per filter are allowed: /books?language=en&language=fr
    - Results are ordered by download_count descending.
    """
    query = db.query(Book)

    # Filter by Gutenberg book IDs
    if book_ids:
        query = query.filter(Book.gutenberg_id.in_(book_ids))

    # Filter by language codes
    if languages:
        lowered_langs = [code.lower() for code in languages]
        query = query.join(Book.languages).filter(func.lower(Language.code).in_(lowered_langs))

    # Filter by mime-types
    if mime_types:
        lowered_mimes = [m.lower() for m in mime_types]
        query = query.join(Book.formats).filter(func.lower(Format.mime_type).in_(lowered_mimes))

    # Filter by topic (subjects OR bookshelves, case-insensitive partial match)
    if topics:
        lowered_topics = [t.lower() for t in topics]
        topic_conditions = []
        for t in lowered_topics:
            like_pattern = f"%{t}%"
            topic_conditions.append(func.lower(Subject.name).like(like_pattern))
            topic_conditions.append(func.lower(Bookshelf.name).like(like_pattern))

        query = query.outerjoin(Book.subjects).outerjoin(Book.bookshelves).filter(
            or_(*topic_conditions)
        )

    # Filter by author name (partial, case-insensitive)
    if authors:
        lowered_authors = [a.lower() for a in authors]
        author_conditions = []
        for a in lowered_authors:
            like_pattern = f"%{a}%"
            author_conditions.append(func.lower(Author.name).like(like_pattern))

        query = query.join(Book.authors).filter(or_(*author_conditions))

    # Filter by title (partial, case-insensitive)
    if titles:
        lowered_titles = [t.lower() for t in titles]
        title_conditions = []
        for t in lowered_titles:
            like_pattern = f"%{t}%"
            title_conditions.append(func.lower(Book.title).like(like_pattern))

        query = query.filter(or_(*title_conditions))

    # Total count for pagination
    total_count = query.distinct(Book.id).count()

    # Pagination & ordering
    offset = (page - 1) * page_size
    # MySQL does not support "NULLS LAST"; emulate by sorting on null-flag first.
    books = (
        query.order_by(
            Book.download_count.is_(None),  # False (0) first, then True (1)
            Book.download_count.desc(),
            Book.id.asc(),
        )
        .offset(offset)
        .limit(page_size)
        .all()
    )

    # Manually build response objects to control nested structure
    results: List[BookSchema] = []
    for book in books:
        authors_data = [
            AuthorSchema(
                name=a.name,
                birth_year=a.birth_year,
                death_year=a.death_year,
            )
            for a in book.authors
        ]
        formats_data = [
            FormatSchema(
                mime_type=f.mime_type,
                url=f.url,
            )
            for f in book.formats
        ]
        languages_data = [lang.code for lang in book.languages]
        subjects_data = [subj.name for subj in book.subjects]
        bookshelves_data = [bs.name for bs in book.bookshelves]

        # Genre is not explicitly available in the Gutendex schema;
        # we expose it as None to satisfy the spec.
        genre = None

        results.append(
            BookSchema(
                id=book.id,
                gutenberg_id=book.gutenberg_id,
                title=book.title or "",
                authors=authors_data,
                genre=genre,
                languages=languages_data,
                subjects=subjects_data,
                bookshelves=bookshelves_data,
                formats=formats_data,
            )
        )

    return BookListResponse(
        count=total_count,
        page=page,
        page_size=page_size,
        results=results,
    )


@app.get("/")
def root():
    return {"message": "Gutendex Books API. Use /books to query the catalog."}


