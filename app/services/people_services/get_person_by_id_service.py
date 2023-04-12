# app/services/people_services/get_person_service.py
import uuid
from typing import List, Optional
from fastapi import HTTPException  # TODO: implement custom exceptions
from gremlin_python.process.graph_traversal import identity

from app.database.gremlin import GraphDB
from gremlin_python.process.traversal import T
from app.database.models import PersonCreate, PersonUpdate, Person


class GetPersonByIdService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, person_id: str) -> Optional[Person]:
        # Get a graph traversal object
        g = await self.db.get_traversal()

        # Find the vertex with the given person_id
        person_vertex = await g.V(person_id).valueMap().toList()

        # Close the graph database connection
        await self.db.close_connection()

        # If the vertex is not found, return None
        if not person_vertex:
            return None

        # Create a Person object from the vertex properties and return it
        person_data = {k: v[0]
                       for k, v in person_vertex[0].items()}  # Change this line
        person_data["id"] = person_id
        return Person(**person_data)
