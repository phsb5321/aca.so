from typing import Optional
from gremlin_python.process.traversal import T
from app.database.models import Book, Person
from app.database.gremlin import GraphDB
from gremlin_python.process.graph_traversal import identity


class GetBookByIdService:
    def __init__(self, graph_database: GraphDB):
        self.db = graph_database

    async def execute(self, book_id: str) -> Optional[Book]:
        g = await self.db.get_traversal()

        # Get book vertex by ID
        book_vertex = await g.V(book_id).project("id", "properties").by(identity().id()).by(
            identity().valueMap()).toList()

        if not book_vertex:
            await self.db.close_connection()
            return None

        book_data = book_vertex[0]["properties"]

        # Extract the first element of the list for each element in the response dictionary
        for element in book_data:
            book_data[element] = book_data[element][0]

        # Get authors related to the book
        author_vertices = await g.V(book_id).inE('authored').outV().project("id", "properties").by(identity().id()).by(
            identity().valueMap()).toList()

        authors = []
        for author_data in author_vertices:
            properties = author_data["properties"]
            # Extract the first element of the list for each element in the response dictionary
            for element in properties:
                properties[element] = properties[element][0]
            authors.append(Person(**properties))

        # Add the authors to the book data
        book_data["authors"] = authors

        return Book(**book_data)
