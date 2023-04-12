# app/services/books_services/delete_book_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class DeleteBookService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book_id: str) -> str:  # Update the return type to str
        # Get a graph traversal object
        g = await self.db.get_traversal()

        # Find the vertex with the given book_id
        book_vertex = await g.V(book_id).valueMap().toList()

        # If the vertex is not found, raise a 404 HTTP exception
        if not book_vertex:
            await self.db.close_connection()
            raise HTTPException(status_code=404, detail="Book not found")

        # Delete the vertex from the graph database
        await g.V(book_id).drop().iterate()

        # Close the graph database connection
        await self.db.close_connection()

        return book_id  # Return the book_id
