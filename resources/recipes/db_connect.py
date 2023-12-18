import asyncpg
from fastapi import FastAPI

app = FastAPI()

# Replace these with your RDS instance details
DATABASE_URL = "postgresql://username:password@rds_endpoint:5432/db_name"

async def connect_to_db():
    return await asyncpg.connect(DATABASE_URL)

@app.on_event("startup")
async def startup():
    app.state.db = await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = "SELECT * FROM items WHERE id = $1"
    record = await app.state.db.fetchrow(query, item_id)
    return record