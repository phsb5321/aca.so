from fastapi import FastAPI

from database import GraphDB


app = FastAPI()

db = GraphDB()
g = db.get_traversal()

@app.get("/")
async def root():
    return {"message": "Hello World"}
