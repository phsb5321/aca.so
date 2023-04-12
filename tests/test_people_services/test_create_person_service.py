# tests/test_people_services/test_create_person_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate
from app.services import (
    CreatePersonService
)


# Fixture to share an instance of PersonUseCases between tests and clean up the connection after all tests are run
@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_person = CreatePersonService(graph_database)
    try:
        yield create_person
    finally:
        await graph_database.close_connection()


# Test the create_person method in PersonUseCases
@pytest.mark.asyncio
async def test_create_person():
    async with generate_services() as create_person:
        # Call the create_person method with a new PersonCreate object
        created_person = await create_person.execute(PersonCreate(name="John Doe"))

        # Check if the returned Person object has the correct id and name
        assert isinstance(created_person.id, str)
        assert created_person.name == "John Doe"
