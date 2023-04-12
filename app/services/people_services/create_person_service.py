# app/services/people_services/create_person_service.py
import uuid
from typing import List, Optional
from fastapi import HTTPException  # TODO: implement custom exceptions
from gremlin_python.process.graph_traversal import identity

from app.database.gremlin import GraphDB
from gremlin_python.process.traversal import T
from app.database.models import PersonCreate, PersonUpdate, Person


class CreatePersonService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, person: PersonCreate) -> Person:
        # Convert the input PersonCreate object to a dictionary
        person_properties = person.dict()

        # Generate a unique ID for the new person
        person_id = str(uuid.uuid4())
        person_properties["id"] = person_id

        # Create a new vertex in the graph database with the label "person" and the given properties
        new_vertex = await self.db.create_vertex("person", person_properties)

        # Retrieve the properties of the newly created vertex using its ID
        g = await self.db.get_traversal()
        response_dict = await g.V(new_vertex.id).valueMap().next()

        # Extract 'id' and 'name' properties from the response
        if 'id' in response_dict:
            response_dict["id"] = response_dict["id"][0]
        if 'name' in response_dict:
            response_dict["name"] = response_dict["name"][0]

        # Create a Person object from the response dictionary
        response = Person(**response_dict)

        # Close the graph database connection
        await self.db.close_connection()
        return response
