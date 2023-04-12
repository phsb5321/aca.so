# tests/test_people_services/test_list_people_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import Person, PersonCreate
from app.services import (
    CreatePersonService,
    ListPeopleService
)


# Fixture to share an instance of PersonUseCases between tests and clean up the connection after all tests are run
@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_person = CreatePersonService(graph_database)
    list_people = ListPeopleService(graph_database)
    try:
        yield (create_person, list_people)
    finally:
        await graph_database.close_connection()


# Test the get_persons method in PersonUseCases
@pytest.mark.asyncio
async def test_list_people():
    async with generate_services() as (create_person, list_people):
        # Create two new persons
        await create_person.execute(PersonCreate(name="John Doe"))
        await create_person.execute(PersonCreate(name="Jane Doe"))

        # Retrieve all persons with a limit of 2
        persons = await list_people.execute(skip=0, limit=2)

        # Check if the returned list contains 2 Person objects
        assert len(persons) == 2
        assert isinstance(persons[0], Person)
        assert isinstance(persons[1], Person)
