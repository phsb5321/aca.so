# app/services/books_services/create_read_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class CreateReadService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, read: ReadCreate) -> None:
        reader_id = read.reader_id
        book_id = read.book_id
        await self.db.create_edge("read", reader_id, book_id)
