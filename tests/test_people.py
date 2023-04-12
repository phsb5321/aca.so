# tests/test_people.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, PersonUpdate
from app.services.people_services import PersonUseCases, Person

# Fixture to share an instance of PersonUseCases between tests and clean up the connection after all tests are run
@asynccontextmanager
async def person_use_cases():
    graph_database = GraphDB()
    use_cases = PersonUseCases(graph_database)
    try:
        yield use_cases
    finally:
        await graph_database.close_connection()

# Test the create_person method in PersonUseCases
@pytest.mark.asyncio
async def test_create_person():
    async with person_use_cases() as use_cases:
        # Call the create_person method with a new PersonCreate object
        created_person = await use_cases.create_person(PersonCreate(name="John Doe"))

        # Check if the returned Person object has the correct id and name
        assert isinstance(created_person.id, str)
        assert created_person.name == "John Doe"

# Test the update_person method in PersonUseCases
@pytest.mark.asyncio
async def test_update_person():
    async with person_use_cases() as use_cases:
        # Create a new person and update their name
        created_person = await use_cases.create_person(PersonCreate(name="Jane Doe"))
        updated_person = await use_cases.update_person(created_person.id, PersonUpdate(name="Jane Smith"))

        # Check if the returned Person object has the correct id and updated name
        assert updated_person.id == created_person.id
        assert updated_person.name == "Jane Smith"

# Test the delete_person method in PersonUseCases
@pytest.mark.asyncio
async def test_delete_person():
    async with person_use_cases() as use_cases:
        # Create a new person and delete them
        created_person = await use_cases.create_person(PersonCreate(name="John Doe"))
        deleted = await use_cases.delete_person(created_person.id)

        # Check if the delete_person method returns True for the deleted person
        assert deleted is True

# Test the get_person method in PersonUseCases
@pytest.mark.asyncio
async def test_get_person():
    async with person_use_cases() as use_cases:
        # Create a new person and retrieve them
        created_person = await use_cases.create_person(PersonCreate(name="John Doe"))
        retrieved_person = await use_cases.get_person(created_person.id)

        # Check if the retrieved Person object is the same as the created Person object
        assert retrieved_person.id == created_person.id
        assert retrieved_person.name == created_person.name

# Test the get_persons method in PersonUseCases
@pytest.mark.asyncio
async def test_get_persons():
    async with person_use_cases() as use_cases:
        # Create two new persons
        await use_cases.create_person(PersonCreate(name="John Doe"))
        await use_cases.create_person(PersonCreate(name="Jane Doe"))

        # Retrieve all persons with a limit of 2
        persons = await use_cases.get_persons(skip=0, limit=2)

        # Check if the returned list contains 2 Person objects
        assert len(persons) == 2
        assert isinstance(persons[0], Person)
        assert isinstance(persons[1], Person)
