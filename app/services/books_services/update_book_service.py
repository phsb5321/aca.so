# app/services/books_services/update_book_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class UpdateBookService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book_id: str, book: BookUpdate) -> Optional[Book]:
        # Get a graph traversal object
        g = await self.db.get_traversal()

        # Find the vertex with the given book_id
        book_vertex = await g.V(book_id).valueMap().toList()

        # If the vertex is not found, return None
        if not book_vertex:
            await self.db.close_connection()
            return None

        # Update the properties of the vertex with the new values from the input BookUpdate object
        book_data = book_vertex[0]
        for key, value in book.dict(exclude_unset=True).items():
            book_data[key] = value

        # Update the title property of the vertex in the graph database
        await g.V(book_id).property("title", book_data["title"]).iterate()

        # Close the graph database connection
        await self.db.close_connection()

        # Create a Book object from the updated properties and return it
        book_data["id"] = book_id
        return Book(**book_data)
