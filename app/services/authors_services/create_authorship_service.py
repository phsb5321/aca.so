# app/services/books_services/create_authorship_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class CreateAuthorshipService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, authorship: AuthorshipCreate) -> None:
        author_id = authorship.author_id
        book_id = authorship.book_id
        await self.db.create_edge("authored", author_id, book_id)
