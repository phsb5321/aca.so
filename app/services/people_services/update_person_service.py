# app/services/people_services/update_person_service.py
import uuid
from typing import List, Optional
from fastapi import HTTPException  # TODO: implement custom exceptions
from gremlin_python.process.graph_traversal import identity

from app.database.gremlin import GraphDB
from gremlin_python.process.traversal import T
from app.database.models import PersonCreate, PersonUpdate, Person


class UpdatePersonService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, person_id: str, person: PersonUpdate) -> Optional[Person]:
        # Get a graph traversal object
        g = await self.db.get_traversal()

        # Find the vertex with the given person_id
        person_vertex = await g.V(person_id).valueMap().toList()

        # If the vertex is not found, return None
        if not person_vertex:
            await self.db.close_connection()
            return None

        # Update the properties of the vertex with the new values from the input PersonUpdate object
        person_data = person_vertex[0]
        for key, value in person.dict(exclude_unset=True).items():
            person_data[key] = value

        # Update the name property of the vertex in the graph database
        await g.V(person_id).property("name", person_data["name"]).iterate()

        # Close the graph database connection
        await self.db.close_connection()

        # Create a Person object from the updated properties and return it
        person_data["id"] = person_id  # Change this line
        return Person(**person_data)
