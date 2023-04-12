# app/services/books_services/create_rating_service.py
from typing import List, Optional
import uuid
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating, ReadCreate


class CreateRatingService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, rating: RatingCreate) -> Rating:
        # Validate the input data using the RatingCreate schema
        try:
            rating_dict = rating.dict()
            RatingCreate(**rating_dict)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Get a graph traversal object
        g = await self.db.get_traversal()

        # Find the reader vertex and the book vertex
        reader_vertex = await g.V(rating.reader_id).toList()
        book_vertex = await g.V(rating.book_id).toList()

        # If either the reader or the book is not found, raise a 404 HTTP exception
        if not reader_vertex or not book_vertex:
            await self.db.close_connection()
            raise HTTPException(
                status_code=404, detail="Reader or book not found")

        # Create a new edge labeled "rated" between the reader vertex and the book vertex with the given rating properties
        edge_properties = {"score": rating.score, "comment": rating.comment}
        rated_edge = await g.V(rating.reader_id).addE("rated").to(g.V(rating.book_id)).property("score",
                                                                                                edge_properties[
                                                                                                    "score"]).property(
            "comment", edge_properties["comment"]).toList()

        # Close the graph database connection
        await self.db.close_connection()

        # Create a Rating object from the created data and return it
        rating_data = {
            "reader": Person(id=rating.reader_id, name=reader_vertex[0].get("name")),
            "score": rating.score,
            "comment": rating.comment,
        }
        return Rating(**rating_data)
