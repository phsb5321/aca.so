# app/services/readers_services/list_ratings_by_book_service.py
from typing import List
from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import Rating, Book, Person
from app.services.books_services.get_book_by_id_service import GetBookByIdService
from app.services.people_services.get_person_by_id_service import GetPersonByIdService
from gremlin_python.process.graph_traversal import identity


class ListRatingsByBookService:
    def __init__(self, db: GraphDB, get_book_by_id: GetBookByIdService, get_person_by_id: GetPersonByIdService):
        self.db = db
        self.get_book_by_id = get_book_by_id
        self.get_person_by_id = get_person_by_id

    async def execute(self, book_id: str, skip: int = 0, limit: int = 10) -> List[Rating]:
        # Get a traversal source for the graph database
        g = await self.db.get_traversal()

        # Get the book data by ID
        book_data = await self.get_book_by_id.execute(book_id)

        # If the book is not found, raise an HTTP exception
        if not book_data:
            raise HTTPException(status_code=404, detail="Book not found")

        # Get the rating edges and reader vertices for the book
        rating_edges_and_readers = (
            await g
            .V(book_id)  # Get the book vertex by ID
            .inE("rated")  # Get the rating edges
            .range(skip, skip + limit)  # Skip and limit the number of edges
            .as_("edge")  # Assign the rating edge to the "edge" variable
            .outV()  # Get the reader vertex
            # Project the rating edge and reader vertex
            .project("edge", "reader_vertex")
            # Assign the rating edge properties to the "edge" variable
            .by(identity().select("edge").valueMap())
            .by(identity().valueMap())  # Get the reader vertex properties
            .toList()  # Return the list of rating edges and reader vertices
        )

        # Create a list of Rating objects from the rating edges and reader vertices
        ratings = []
        for rating_data in rating_edges_and_readers:
            rating_edge = rating_data["edge"]
            reader_properties = rating_data["reader_vertex"]

            reader_id = reader_properties["id"][0]
            if reader_id is None:
                raise HTTPException(status_code=404, detail="Reader not found")

            reader = await self.get_person_by_id.execute(reader_id)

            # Create a dictionary of rating data for the Rating object
            rating_data = {
                "reader": reader,
                "score": rating_edge["score"],
                "comment": rating_edge["comment"],
                "book": book_data
            }

            # Append a new Rating object to the list of ratings
            ratings.append(Rating(**rating_data))

        # Close the graph database connection
        await self.db.close_connection()

        # Return the list of ratings
        return ratings
