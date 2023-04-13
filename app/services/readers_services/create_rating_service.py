from fastapi import HTTPException
from app.database.gremlin import GraphDB
from app.database.models import RatingCreate, Person, Book, Rating
from app.services.people_services.get_person_by_id_service import GetPersonByIdService
from app.services.books_services.get_book_by_id_service import GetBookByIdService


class CreateRatingService:
    def __init__(self, db: GraphDB, get_person_by_id: GetPersonByIdService, get_book_by_id: GetBookByIdService):
        self.db = db
        self.get_person_by_id = get_person_by_id
        self.get_book_by_id = get_book_by_id

    async def execute(self, rating: RatingCreate) -> Rating:
        # Validate the input data using the RatingCreate schema
        try:
            rating_dict = rating.dict()
            RatingCreate(**rating_dict)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Get the reader and book data
        reader_data = await self.get_person_by_id.execute(rating.reader_id)
        book_data = await self.get_book_by_id.execute(rating.book_id)

        # If either the reader or the book is not found, raise a 404 HTTP exception
        if not reader_data or not book_data:
            await self.db.close_connection()
            raise HTTPException(
                status_code=404, detail="Reader or book not found")

        # Create a new edge labeled "rated" between the reader vertex and the book vertex with the given rating properties
        g = await self.db.get_traversal()
        edge_properties = {"score": rating.score, "comment": rating.comment}
        rated_edge = await g.V(rating.reader_id).addE("rated").to(g.V(rating.book_id)).property("score",
                                                                                                edge_properties[
                                                                                                    "score"]).property(
            "comment", edge_properties["comment"]).toList()

        # Check if the edge was created successfully
        if len(rated_edge) == 0:
            await self.db.close_connection()
            raise HTTPException(
                status_code=500, detail="Failed to create rating")

        # Close the graph database connection
        await self.db.close_connection()

        # Create a Rating object from the created data and return it
        rating_data = {
            "reader": reader_data,
            "score": rating.score,
            "comment": rating.comment,
            "book": book_data,
        }
        return Rating(**rating_data)
