# app/services/people_services/list_people_service.py
import uuid
from typing import List, Optional
from fastapi import HTTPException  # TODO: implement custom exceptions
from gremlin_python.process.graph_traversal import identity

from app.database.gremlin import GraphDB
from gremlin_python.process.traversal import T
from app.database.models import PersonCreate, PersonUpdate, Person


class ListPeopleService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, skip: int = 0, limit: int = 100) -> List[Person]:
        # Get a graph traversal object
        g = await self.db.get_traversal()

        # Find all vertices with the label "person", apply the specified range, and retrieve their properties
        person_vertices = await g.V().hasLabel("person").range(skip, skip + limit).project("id", "properties").by(identity().id()).by(identity().valueMap()).toList()

        # Close the graph database connection
        await self.db.close_connection()

        # Convert the list of vertex properties into a list of Person objects
        persons = []
        for person_data in person_vertices:
            properties = person_data["properties"]
            properties["id"] = person_data["id"]
            # Extract the string value of the name
            properties["name"] = properties["name"][0]
            persons.append(Person(**properties))

        return persons
