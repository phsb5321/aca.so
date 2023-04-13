# app/services/books_services/create_read_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, Read, ReadCreate
from app.services.people_services.get_person_by_id_service import GetPersonByIdService
from app.services.books_services.get_book_by_id_service import GetBookByIdService


class CreateReadService:
    def __init__(self, db: GraphDB, get_person_by_id: GetPersonByIdService, get_book_by_id: GetBookByIdService):
        self.db = db
        self.get_person_by_id = get_person_by_id
        self.get_book_by_id = get_book_by_id

    async def execute(self, read: ReadCreate) -> Read:
        # Get the reader and book data
        reader_data = await self.get_person_by_id.execute(read.reader_id)
        book_data = await self.get_book_by_id.execute(read.book_id)

        # If either the reader or the book is not found, raise a 404 HTTP exception
        if not reader_data or not book_data:
            await self.db.close_connection()
            raise HTTPException(
                status_code=404, detail="Reader or book not found")

        # Create a new edge labeled "read" between the reader vertex and the book vertex
        g = await self.db.get_traversal()
        read_edge = await g.V(read.reader_id).addE("read").to(g.V(read.book_id)).toList()

        # Check if the edge was created successfully
        if len(read_edge) == 0:
            await self.db.close_connection()
            raise HTTPException(
                status_code=500, detail="Failed to create read")

        # Close the graph database connection
        await self.db.close_connection()

        # Create a Read object from the created data and return it
        read_data = {
            "reader": reader_data,
            "book": book_data,
        }
        return Read(**read_data)
