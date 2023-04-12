# people_routes.py
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, PersonUpdate, Person
from app.services.people_services import PersonUseCases

router = APIRouter()


@router.post("/", response_model=Person)
async def create_person(person: PersonCreate):
    graph_database = GraphDB()
    people_repository = PersonUseCases(graph_database)
    response = await people_repository.create_person(person)
    return response


@router.get("/{person_id}", response_model=Person)
async def read_person(person_id: str):
    graph_database = GraphDB()
    people_repository = PersonUseCases(graph_database)
    person = await people_repository.get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.put("/{person_id}", response_model=Person)
async def update_person(person_id: str, person: PersonUpdate):
    graph_database = GraphDB()
    people_repository = PersonUseCases(graph_database)
    updated_person = await people_repository.update_person(person_id, person)
    if not updated_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated_person


@router.delete("/{person_id}")
async def delete_person(person_id: str):
    graph_database = GraphDB()
    people_repository = PersonUseCases(graph_database)
    result = await people_repository.delete_person(person_id)
    if not result:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"deleted": True}


@router.get("/", response_model=List[Person])
async def read_persons(skip: int = 0, limit: int = 100):
    graph_database = GraphDB()
    people_repository = PersonUseCases(graph_database)
    persons = await people_repository.get_persons(skip=skip, limit=limit)
    return persons
