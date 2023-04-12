# app/services/books_services/get_book_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class GetBookByIdService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book_id: str) -> Optional[Book]:
        g = await self.db.get_traversal()
        book_vertex = await g.V(book_id).valueMap().toList()
        await self.db.close_connection()

        if not book_vertex:
            return None

        book_data = book_vertex[0]
        book_data["id"] = book_id
        return Book(**book_data)
