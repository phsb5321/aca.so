# app/services/books_services/create_book_service.py
from typing import List
import uuid
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, Book


class CreateBookService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book: BookCreate, author_ids: List[int]) -> Book:
        # Convert the input BookCreate object to a dictionary
        book_properties = book.dict()

        # Generate a unique ID for the new book
        book_id = str(uuid.uuid4())
        book_properties["id"] = book_id

        # Create a new vertex in the graph database with the label "book" and the given properties
        new_vertex = await self.db.create_vertex("book", book_properties)

        # Add edges between the book vertex and its authors
        for author_id in author_ids:
            await self.db.create_edge("authored", author_id, book_id)

        # Retrieve the properties of the newly created vertex using its ID
        g = await self.db.get_traversal()
        response_dict = await g.V(new_vertex.id).valueMap().next()

        # Extract 'id' and 'title' properties from the response
        if 'id' in response_dict:
            response_dict["id"] = response_dict["id"][0]
        if 'title' in response_dict:
            response_dict["title"] = response_dict["title"][0]

        print(response_dict)

        # Create a Book object from the response dictionary
        response = Book(**response_dict)

        # Close the graph database connection
        await self.db.close_connection()
        return response
