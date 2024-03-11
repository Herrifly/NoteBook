from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Body
from pymongo import ReturnDocument

from database import notes
from note.schemas import Note, Notes, NotePatch

router = APIRouter(
    tags=['note'],
    prefix='/note'

)


@router.get('/notes/',
            response_description="List all notes",
            response_model=Notes)
async def get_notes():

    notes_list = list(notes.find())

    return Notes(notes=notes_list)


@router.get(
    "/notes/{id}",
    response_description="Get a single note",
    response_model=Note,
    response_model_by_alias=False,
)
async def show_note(id: str):
    """
    Get the record for a specific note, looked up by `id`.
    """
    if (
            note := notes.find_one({"_id": ObjectId(id)})
    ) is not None:
        return note

    raise HTTPException(status_code=404, detail=f"Note {id} not found")


@router.post(
    "/notes/",
    response_description="Add new note",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_note(note: Note = Body(...)):
    """
    Insert a new note record.

    A unique `id` will be created and provided in the response.
    """
    new_note = notes.insert_one(
        note.model_dump(by_alias=True, exclude=["id"])
    )
    created_note = notes.find_one(
        {"_id": new_note.inserted_id}
    )
    return created_note


@router.patch(
    "/notes/{id}",
    response_description="Update a note",
    response_model=Note,
    response_model_by_alias=False,
)
async def update_note(id: str, note: NotePatch = Body(...)):
    """
    Update individual fields of an existing note record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    note = {
        k: v for k, v in note.model_dump(by_alias=True).items() if v is not None
    }

    if len(note) >= 1:
        update_result = notes.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": note},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"note {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_note := notes.find_one({"_id": id})) is not None:
        return existing_note

    raise HTTPException(status_code=404, detail=f"note {id} not found")


@router.delete("/notes/{id}",
               response_description="Delete an note",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(id: str):
    """
    Get the record for a specific note, looked up by `id`.
    """
    result = notes.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return

    raise HTTPException(status_code=404, detail=f"note {id} not found")
