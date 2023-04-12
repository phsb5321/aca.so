# app/services/books_services/list_ratings_by_book_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class ListRatingsByBookService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, book_id: int, skip: int = 0, limit: int = 10) -> List[Rating]:
        g = await self.db.get_traversal()

        rating_edges = await g.V(book_id).inE("rated").range(skip, skip + limit).toList()

        await self.db.close_connection()

        ratings = []
        for rating_edge in rating_edges:
            reader_vertex = await rating_edge.outV().next()
            reader = Person(id=reader_vertex.id, name=reader_vertex["name"])

            rating_data = {
                "reader": reader,
                "score": rating_edge["score"],
                "comment": rating_edge["comment"],
            }
            ratings.append(Rating(**rating_data))

        return ratings
