# tests/test_people_services/test_update_person_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, PersonUpdate
from app.services import (
    CreatePersonService,
    UpdatePersonService
)


# Fixture to share an instance of PersonUseCases between tests and clean up the connection after all tests are run
@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    update_person = UpdatePersonService(graph_database)
    create_person = CreatePersonService(graph_database)
    try:
        yield (create_person, update_person)
    finally:
        await graph_database.close_connection()


# Test the update_person method in PersonUseCases
@pytest.mark.asyncio
async def test_update_person():
    async with generate_services() as (create_person, update_person):
        # Create a new person and update their name
        created_person = await create_person.execute(PersonCreate(name="Jane Doe"))
        updated_person = await update_person.execute(created_person.id, PersonUpdate(name="Jane Smith"))

        # Check if the returned Person object has the correct id and updated name
        assert updated_person.id == created_person.id
        assert updated_person.name == "Jane Smith"
