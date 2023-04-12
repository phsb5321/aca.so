# app/services/books_services/list_readers_by_book_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class ListReadersByBookService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
        g = await self.db.get_traversal()

        reader_vertices = await g.V(book_id).in_("read").range(skip, skip + limit).toList()

        await self.db.close_connection()

        readers = []
        for reader_vertex in reader_vertices:
            reader_data = reader_vertex.valueMap().next()
            reader_data["id"] = reader_vertex.id
            readers.append(Person(**reader_data))

        return readers
