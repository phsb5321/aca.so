# app/services/books_services/create_authorship_service.py
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import (
    AuthorshipCreate,
    Person,
    Book,
    Authorship,
)
from app.services.books_services.get_book_by_id_service import GetBookByIdService
from app.services.people_services.get_person_by_id_service import GetPersonByIdService


class CreateAuthorshipService:
    def __init__(self, db: GraphDB, get_book_by_id: GetBookByIdService, get_person_by_id: GetPersonByIdService):
        self.db = db
        self.get_book_by_id = get_book_by_id
        self.get_person_by_id = get_person_by_id

    async def execute(self, authorship: AuthorshipCreate, ) -> Authorship:
        author_id = authorship.author_id
        book_id = authorship.book_id

        author_data = await self.get_person_by_id.execute(author_id)

        if not author_data:
            await self.db.close_connection()
            raise HTTPException(
                status_code=404, detail="Author not found")

        book_data = await self.get_book_by_id.execute(book_id)

        if not book_data:
            await self.db.close_connection()
            raise HTTPException(
                status_code=404, detail="Book not found")

        # Create the Authorship object and return it
        authorship_data = {"author": author_data, "book": book_data}
        return Authorship(**authorship_data)
