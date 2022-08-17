from fastapi import FastAPI
app = FastAPI()

from db import initialize_db, generate_table


@app.get("/")
def root():
    ddb = generate_table()
    print(ddb)
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}