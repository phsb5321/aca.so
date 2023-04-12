# app/services/books_services/create_book_service.py
from typing import List
import uuid
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, Book, Person


class CreateBookService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book: BookCreate, authors: List[Person]) -> Book:
        # Convert the input BookCreate object to a dictionary
        book_properties = book.dict()

        # Generate a unique ID for the new book
        book_id = str(uuid.uuid4())
        book_properties["id"] = book_id

        # Create a new vertex in the graph database with the label "book" and the given properties
        new_vertex = await self.db.create_vertex("book", book_properties)

        # Create the author_ids list
        author_ids = [author.id for author in authors]

        # Add edges between the book vertex and its authors
        for author_id in author_ids:
            await self.db.create_edge("authored", author_id, book_id)

        # Retrieve the properties of the newly created vertex using its ID
        g = await self.db.get_traversal()
        response_dict = await g.V(new_vertex.id).valueMap().next()

        # For each element in the response dictionary, get the first element of the list
        for element in response_dict:
            response_dict[element] = response_dict[element][0]

        # Add the author_ids to the response dictionary
        response_dict["authors"] = authors

        # Create a Book object from the response dictionary
        response = Book(**response_dict)
        print(response)
        # Close the graph database connection
        await self.db.close_connection()
        return response
