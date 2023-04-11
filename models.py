# models.py
from typing import List, Optional
from pydantic import BaseModel, Field


class PersonBase(BaseModel):
    name: str


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass


class Person(PersonBase):
    id: str

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    isbn: str
    stock: int


class BookCreate(BookBase):
    authors: List[str]


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: str
    authors: List[Person]
    average_rating: Optional[float]
    ratings_count: int

    class Config:
        orm_mode = True


class RatingCreate(BaseModel):
    book_id: str
    reader_id: str
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=256)


class Rating(BaseModel):
    reader: Person
    score: int
    comment: Optional[str]

    class Config:
        orm_mode = True
