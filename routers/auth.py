from fastapi import APIRouter

router = APIRouter()


@router.post("/auth")
def get_user():
    return {"id": 1, "username": "testuser", "email": "testuser@example.com"}
