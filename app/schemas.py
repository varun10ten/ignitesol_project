from typing import List, Optional

from pydantic import BaseModel


class AuthorSchema(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None


class FormatSchema(BaseModel):
    mime_type: str
    url: str


class BookSchema(BaseModel):
    id: int
    gutenberg_id: int
    title: str
    authors: List[AuthorSchema]
    genre: Optional[str] = None
    languages: List[str]
    subjects: List[str]
    bookshelves: List[str]
    formats: List[FormatSchema]

    class Config:
        orm_mode = True


class BookListResponse(BaseModel):
    count: int
    page: int
    page_size: int
    results: List[BookSchema]


