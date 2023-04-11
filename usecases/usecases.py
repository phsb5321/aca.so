# usecases.py
from typing import List, Optional
from database import GraphDB
from models import BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating
import uuid


async def create_person(db: GraphDB, person: PersonCreate) -> Person:
    person_properties = person.dict()
    person_id = str(uuid.uuid4())
    person_properties["id"] = person_id
    # Use the async_create_vertex function
    new_vertex = await db.create_vertex("person", person_properties)

    # Get the properties of the created vertex using the vertex traversal
    g = await db.get_traversal()
    response_dict = await g.V(new_vertex.id).valueMap().next()

    if 'id' in response_dict:
        response_dict["id"] = response_dict["id"][0]
    if 'name' in response_dict:
        response_dict["name"] = response_dict["name"][0]

    response = Person(**response_dict)

    # Close the connection
    await db.close_connection()
    return response


def update_person(person_id: int, person: PersonUpdate) -> Person:
    pass  # Implement update person logic


def delete_person(person_id: int) -> None:
    pass  # Implement delete person logic


def get_person(person_id: int) -> Optional[Person]:
    pass  # Implement get person logic


def get_persons(skip: int = 0, limit: int = 10) -> List[Person]:
    pass  # Implement get persons logic


def create_book(book: BookCreate) -> Book:
    pass  # Implement create book logic


def update_book(book_id: int, book: BookUpdate) -> Book:
    pass  # Implement update book logic


def delete_book(book_id: int) -> None:
    pass  # Implement delete book logic


def get_book(book_id: int) -> Optional[Book]:
    pass  # Implement get book logic


def get_books(skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
    pass  # Implement get books logic


def get_books_by_author(author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
    pass  # Implement get books by author logic


def get_readers_by_book(book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
    pass  # Implement get readers by book logic


def get_ratings_by_book(book_id: int, skip: int = 0, limit: int = 10) -> List[Rating]:
    pass  # Implement get ratings by book logic


def create_rating(rating: RatingCreate) -> Rating:
    pass  # Implement create rating logic
