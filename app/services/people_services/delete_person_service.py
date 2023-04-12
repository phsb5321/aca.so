# app/services/delete_person_service.py
import uuid
from typing import List, Optional
from fastapi import HTTPException  # TODO: implement custom exceptions
from gremlin_python.process.graph_traversal import identity

from app.database.gremlin import GraphDB
from gremlin_python.process.traversal import T
from app.database.models import PersonCreate, PersonUpdate, Person


class DeletePersonService:
    def __init__(self, db: GraphDB):
        self.db = db

    async def execute(self, person_id: str) -> bool:
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
