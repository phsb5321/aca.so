# app/services/books_services/update_book_service.py

import uuid
from typing import Optional

from app.database.gremlin import GraphDB
from app.database.models import BookCreate, BookUpdate, Book


class UpdateBookService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book_id: str, book_update: BookUpdate) -> Optional[Book]:
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
        for key, value in book_update.dict(exclude_unset=True).items():
            book_data[key] = value

        # Update the properties of the vertex in the graph database
        await g.V(book_id).property("title", book_data.get("title")).property("isbn", book_data.get("isbn")).property("stock", book_data.get("stock")).iterate()

        # Close the graph database connection
        await self.db.close_connection()

        # Create a Book object from the updated properties and return it
        book_data["id"] = book_id
        book_data["authors"] = []
        return Book(**book_data)
