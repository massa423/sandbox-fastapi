from fastapi import APIRouter, HTTPException
from typing import List, Dict

router = APIRouter()


@router.get("/")
async def read_items() -> List[Dict]:
    return [{"name": "Item Foo"}, {"name": "Item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str) -> Dict:
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {
        "description": "Operation forbidden"
    }},
)
async def update_item(item_id: str) -> Dict:
    if item_id != "foo":
        raise HTTPException(status_code=403,
                            detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}
