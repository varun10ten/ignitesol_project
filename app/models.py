from sqlalchemy import Column, Integer, SmallInteger, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Author(Base):
    __tablename__ = "books_author"

    id = Column(Integer, primary_key=True)
    birth_year = Column(SmallInteger)
    death_year = Column(SmallInteger)
    name = Column(String(128), nullable=False)

    books = relationship("Book", secondary="books_book_authors", back_populates="authors")


class Book(Base):
    __tablename__ = "books_book"

    id = Column(Integer, primary_key=True)
    download_count = Column(Integer)
    gutenberg_id = Column(Integer, nullable=False)
    media_type = Column(String(16), nullable=False)
    title = Column(Text)

    authors = relationship("Author", secondary="books_book_authors", back_populates="books")
    subjects = relationship("Subject", secondary="books_book_subjects", back_populates="books")
    bookshelves = relationship("Bookshelf", secondary="books_book_bookshelves", back_populates="books")
    languages = relationship("Language", secondary="books_book_languages", back_populates="books")
    formats = relationship("Format", back_populates="book")


class BookAuthor(Base):
    __tablename__ = "books_book_authors"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("books_author.id"), nullable=False)


class BookBookshelf(Base):
    __tablename__ = "books_book_bookshelves"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"), nullable=False)
    bookshelf_id = Column(Integer, ForeignKey("books_bookshelf.id"), nullable=False)


class BookLanguage(Base):
    __tablename__ = "books_book_languages"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("books_language.id"), nullable=False)


class BookSubject(Base):
    __tablename__ = "books_book_subjects"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("books_subject.id"), nullable=False)


class Bookshelf(Base):
    __tablename__ = "books_bookshelf"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    books = relationship("Book", secondary="books_book_bookshelves", back_populates="bookshelves")


class Format(Base):
    __tablename__ = "books_format"

    id = Column(Integer, primary_key=True)
    mime_type = Column(String(32), nullable=False)
    url = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey("books_book.id"), nullable=False)

    book = relationship("Book", back_populates="formats")


class Language(Base):
    __tablename__ = "books_language"

    id = Column(Integer, primary_key=True)
    code = Column(String(4), nullable=False)

    books = relationship("Book", secondary="books_book_languages", back_populates="languages")


class Subject(Base):
    __tablename__ = "books_subject"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    books = relationship("Book", secondary="books_book_subjects", back_populates="subjects")


