import pytest
from database import GraphDB
import asyncio

import usecases.usecases as usecase
from models import PersonCreate


@pytest.mark.asyncio
async def test_create_person():
    # Create a new instance of GraphDB and connect to a real database
    db = GraphDB()

    try:
        # Call the create_person function
        created_person = await usecase.create_person(db, PersonCreate(name="John Doe"))

        # Assert that the returned Person object has the correct id
        assert isinstance(created_person.id, str)

        # Assert that the returned Person object has the correct name
        assert created_person.name == "John Doe"

    finally:
        # Close the connection
        await db.close_connection()
