# app/services/books_services/list_books_by_author_service.py
from typing import List
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import Book, Person
from app.services.people_services.get_person_by_id_service import GetPersonByIdService


class ListBooksByAuthorService:
    def __init__(self, db: GraphDB, get_person_by_id: GetPersonByIdService):
        self.db = db
        self.get_person_by_id = get_person_by_id

    async def execute(self, author_id: str, skip: int = 0, limit: int = 10) -> List[Book]:
        # Get author data from id
        author_data = await self.get_person_by_id.execute(author_id)
        if not author_data:
            await self.db.close_connection()
            raise HTTPException(status_code=404, detail="Author not found")

        # Get books authored by author
        g = await self.db.get_traversal()
        book_vertices = (
            await g.V(author_id)
            .out("authored")
            .range(skip, skip + limit)
            .valueMap()
            .toList()
        )
        await self.db.close_connection()

        # Create book objects from retrieved book data
        books = []
        for book_data in book_vertices:
            for element in book_data:
                book_data[element] = book_data[element][0]
            books.append(Book(**book_data))

        return books
