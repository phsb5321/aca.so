# app/services/__init__.py

# Authors
from .authors_services.create_authorship_service import CreateAuthorshipService
from .authors_services.list_books_by_author_service import ListBooksByAuthorService

# Books
from .books_services.create_book_service import CreateBookService
from .books_services.delete_book_service import DeleteBookService
from .books_services.get_book_service import GetBookService
from .books_services.list_books_service import ListBooksService
from .books_services.update_book_service import UpdateBookService

# People
from .people_services.create_person_service import CreatePersonService
from .people_services.delete_person_service import DeletePersonService
from .people_services.get_person_service import GetPersonService
from .people_services.list_people_service import ListPeopleService
from .people_services.update_person_service import UpdatePersonService

# Readers
from .readers_services.create_rating_service import CreateRatingService
from .readers_services.create_read_service import CreateReadService
from .readers_services.list_ratings_by_book_service import ListRatingsByBookService
from .readers_services.list_readers_by_book_service import ListReadersByBookService

__all__ = [
    "CreateAuthorshipService",
    "ListBooksByAuthorService",
    "CreateBookService",
    "DeleteBookService",
    "GetBookService",
    "ListBooksService",
    "UpdateBookService",
    "CreatePersonService",
    "DeletePersonService",
    "GetPersonService",
    "ListPeopleService",
    "UpdatePersonService",
    "CreateRatingService",
    "CreateReadService",
    "ListRatingsByBookService",
    "ListReadersByBookService",
]
