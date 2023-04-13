# app/services/books_services/list_readers_by_book_service.py
from typing import List
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import Person, Read
from app.services.people_services.get_person_by_id_service import GetPersonByIdService


class ListReadersByBookService:
    def __init__(self, db: GraphDB, getPersonByIdService: GetPersonByIdService):
        self.db = db
        self.get_person_by_id = getPersonByIdService

    async def execute(self, book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
        g = await self.db.get_traversal()
        reader_vertices = (
            await g
            .V(book_id)  # Get the book vertex
            .in_("read")  # Get the read edge
            .range(skip, skip + limit)  # Skip and limit
            .valueMap(True)  # Get the vertex properties
            .toList()  # Return the list of vertices
        )

        # Create a list of Person objects from the reader vertices
        readers = []
        for reader_vertex in reader_vertices:
            reader_id = reader_vertex["id"][0]
            if reader_id is None:
                raise HTTPException(status_code=404, detail="Reader not found")

            reader = await self.get_person_by_id.execute(reader_id)

            # Append a new Person object to the list of readers
            readers.append(reader)

        # Close the graph database connection
        await self.db.close_connection()

        # Return the list of readers
        return readers
