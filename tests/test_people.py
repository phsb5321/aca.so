# test_usecases.py
import pytest
from app.database.gremlin import GraphDB
import asyncio
from app.database.models import PersonCreate
from app.services.people_services import PersonUseCases


@pytest.mark.asyncio
async def test_create_person():
    # Create a new instance of GraphDB and connect to a real database
    graph_database = GraphDB()
    people_repository = PersonUseCases(graph_database)

    try:
        # Call the create_person function
        created_person = await people_repository.create_person(PersonCreate(name="John Doe"))

        # Assert that the returned Person object has the correct id
        assert isinstance(created_person.id, str)

        # Assert that the returned Person object has the correct name
        assert created_person.name == "John Doe"

    finally:
        # Close the connection
        await graph_database.close_connection()
