# tests/test_people_services/test_get_person_by_id_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate
from app.services import (
    CreatePersonService,
    GetPersonByIdService
)


# Fixture to share an instance of PersonUseCases between tests and clean up the connection after all tests are run
@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    get_person_by_id = GetPersonByIdService(graph_database)
    create_person = CreatePersonService(graph_database)
    try:
        yield (get_person_by_id, create_person)
    finally:
        await graph_database.close_connection()


# Test the get_person method in PersonUseCases
@pytest.mark.asyncio
async def test_get_person_by_id():
    async with generate_services() as (get_person_by_id, create_person):
        # Create a new person and retrieve them
        created_person = await create_person.execute(PersonCreate(name="John Doe"))
        retrieved_person = await get_person_by_id.execute(created_person.id)

        # Check if the retrieved Person object is the same as the created Person object
        assert retrieved_person.id == created_person.id
        assert retrieved_person.name == created_person.name
