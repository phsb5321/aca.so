# people_services.py
import uuid
from typing import List, Optional
from fastapi import HTTPException
from gremlin_python.process.graph_traversal import identity

from app.database.gremlin import GraphDB
from gremlin_python.process.traversal import T
from app.database.models import PersonCreate, PersonUpdate, Person


class PersonUseCases:
    def __init__(self, db: GraphDB):
        self.db = db

    async def create_person(self, person: PersonCreate) -> Person:
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

    async def update_person(self, person_id: str, person: PersonUpdate) -> Optional[Person]:
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

    async def delete_person(self, person_id: str) -> bool:
        # Get a graph traversal object
        g = await self.db.get_traversal()

        # Find the vertex with the given person_id
        person_vertex = await g.V(person_id).valueMap().toList()

        # If the vertex is not found, return False
        if not person_vertex:
            await self.db.close_connection()
            return False

        # Delete the vertex from the graph database
        await g.V(person_id).drop().iterate()

        # Close the graph database connection
        await self.db.close_connection()
        return True

    async def get_person(self, person_id: str) -> Optional[Person]:
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

    async def get_persons(self, skip: int = 0, limit: int = 100) -> List[Person]:
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
