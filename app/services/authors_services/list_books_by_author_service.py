# app/services/books_services/list_books_by_author_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class ListBooksByAuthorService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
        g = await self.db.get_traversal()

        book_vertices = await g.V(author_id).out("authored").range(skip, skip + limit).toList()

        await self.db.close_connection()

        books = []
        for book_vertex in book_vertices:
            book_data = book_vertex.valueMap().next()
            book_data["id"] = book_vertex.id
            books.append(Book(**book_data))

        return books
