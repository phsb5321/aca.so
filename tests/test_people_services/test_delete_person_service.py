# tests/test_people_services/test_delete_person_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, PersonUpdate
from app.services import (
    CreatePersonService,
    UpdatePersonService,
    DeletePersonService,
    ListPeopleService,
    GetPersonByIdService
)


# Fixture to share an instance of PersonUseCases between tests and clean up the connection after all tests are run
@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_person = CreatePersonService(graph_database)
    delete_person = DeletePersonService(graph_database)
    try:
        yield (create_person, delete_person)
    finally:
        await graph_database.close_connection()


# Test the delete_person method in PersonUseCases
@ pytest.mark.asyncio
async def test_delete_person():
    async with generate_services() as (create_person, delete_person):
        # Create a new person and delete them
        created_person = await create_person.execute(PersonCreate(name="John Doe"))
        deleted = await delete_person.execute(created_person.id)

        # Check if the delete_person method returns True for the deleted person
        assert deleted is True
