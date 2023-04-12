# app/services/books_services/list_books_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from gremlin_python.process.graph_traversal import identity
from app.database.gremlin import GraphDB
from gremlin_python.process.traversal import P
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class ListBooksService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
        g = await self.db.get_traversal()

        if in_stock is not None:
            stock_query = P.gt(0) if in_stock else P.lte(0)
            book_vertices = await g.V().hasLabel("book").has("stock", stock_query).range(skip, skip + limit).project("id", "properties").by(identity().id()).by(identity().valueMap()).toList()
        else:
            book_vertices = await g.V().hasLabel("book").range(skip, skip + limit).project("id", "properties").by(identity().id()).by(identity().valueMap()).toList()

        books = []
        for book_data in book_vertices:
            properties = book_data["properties"]
            properties["id"] = book_data["id"]
            # Extract the first element of the list for each element in the response dictionary
            for element in properties:
                if element != "id":
                    properties[element] = properties[element][0]

            # Get authors related to the book
            author_vertices = await g.V(book_data["id"]).inE('authored').outV().project("id", "properties").by(identity().id()).by(identity().valueMap()).toList()

            authors = []
            for author_data in author_vertices:
                author_properties = author_data["properties"]
                author_properties["id"] = author_data["id"]
                # Extract the first element of the list for each element in the response dictionary
                for element in author_properties:
                    if element != "id":
                        author_properties[element] = author_properties[element][0]
                authors.append(Person(**author_properties))

            # Add the authors to the book data
            properties["authors"] = authors

            books.append(Book(**properties))

        await self.db.close_connection()

        return books
