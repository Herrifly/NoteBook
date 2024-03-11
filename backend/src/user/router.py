from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Body

from database import users, MongoClient
from user.schemas import Users, UserRead, User

router = APIRouter(
    tags=['user'],
    prefix='/user'

)


@router.get('/users/',
            response_description="List all users",
            response_model=Users)
async def get_users():

    users_list = list(users.find())

    return Users(users=users_list)


@router.get(
    "/users/{id}",
    response_description="Get a single user",
    response_model=UserRead,
    response_model_by_alias=False,
)
async def show_user(id: str):
    """
    Get the record for a specific user, looked up by `id`.
    """
    if (
            user := users.find_one({"_id": ObjectId(id)})
    ) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.post(
    "/users/",
    response_description="Add new user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: User = Body(...)):
    """
    Insert a new user record.

    A unique `id` will be created and provided in the response.
    """
    new_user = users.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = users.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


@router.delete("/users/{id}",
               response_description="Delete an user",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    """
    Get the record for a specific user, looked up by `id`.
    """
    result = users.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return

    raise HTTPException(status_code=404, detail=f"User {id} not found")
