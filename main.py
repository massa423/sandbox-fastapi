from fastapi import FastAPI, Query


app = FastAPI()


@app.post("/items/")
async def read_items(
    q: str = Query(
        None,
        alias="item-query",
        deprecated=True
    )
):
    query_items = {"q": q}
    return query_items
