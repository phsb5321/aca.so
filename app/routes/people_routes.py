# app/routes/people_routes.py
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, PersonUpdate, Person
from app.services import (
    CreatePersonService,
    UpdatePersonService,
    DeletePersonService,
    ListPeopleService,
    GetPersonService
)

router = APIRouter()


@router.post("", response_model=Person)
async def create_person(person: PersonCreate):
    graph_database = GraphDB()
    people_repository = CreatePersonService(graph_database)
    response = await people_repository.execute(person)
    return response


@router.put("/{person_id}", response_model=Person)
async def update_person(person_id: str, person: PersonUpdate):
    graph_database = GraphDB()
    people_repository = UpdatePersonService(graph_database)
    updated_person = await people_repository.execute(person_id, person)
    if not updated_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated_person


@router.delete("/{person_id}")
async def delete_person(person_id: str):
    graph_database = GraphDB()
    people_repository = DeletePersonService(graph_database)
    result = await people_repository.execute(person_id)
    if not result:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"deleted": True}


@router.get("", response_model=List[Person])
async def list_people(skip: int = 0, limit: int = 100):
    graph_database = GraphDB()
    people_repository = ListPeopleService(graph_database)
    persons = await people_repository.execute(skip=skip, limit=limit)
    return persons


@router.get("/{person_id}", response_model=Person)
async def get_person_by_id(person_id: str):
    graph_database = GraphDB()
    people_repository = GetPersonService(graph_database)
    person = await people_repository.execute(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person
