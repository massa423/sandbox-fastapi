from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users() -> List[Dict]:
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me", tags=["users"])
async def read_user_me() -> Dict:
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str) -> Dict:
    return {"username": username}
