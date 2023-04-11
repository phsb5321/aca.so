from typing import List, Optional
import uuid
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, PersonUpdate, Person


class PersonUseCases:
    def __init__(self, db: GraphDB):
        self.db = db

    async def create_person(self, person: PersonCreate) -> Person:
        person_properties = person.dict()
        person_id = str(uuid.uuid4())
        person_properties["id"] = person_id
        # Use the async_create_vertex function
        new_vertex = await self.db.create_vertex("person", person_properties)

        # Get the properties of the created vertex using the vertex traversal
        g = await self.db.get_traversal()
        response_dict = await g.V(new_vertex.id).valueMap().next()

        if 'id' in response_dict:
            response_dict["id"] = response_dict["id"][0]
        if 'name' in response_dict:
            response_dict["name"] = response_dict["name"][0]

        response = Person(**response_dict)

        # Close the connection
        await self.db.close_connection()
        return response

    def update_person(self, person_id: int, person: PersonUpdate) -> Person:
        pass  # Implement update person logic

    def delete_person(self, person_id: int) -> None:
        pass  # Implement delete person logic

    def get_person(self, person_id: int) -> Optional[Person]:
        pass  # Implement get person logic

    def get_persons(self, skip: int = 0, limit: int = 10) -> List[Person]:
        pass  # Implement get persons logic
