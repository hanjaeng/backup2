from fastapi import APIRouter

router = APIRouter()    #fastapi_03과 연결

@router.get("/")
async def read_items():
    return {"message" : "Read all items"}

@router.get("/{itemId}")
async def read_item(itemId: int):
    return {"item_id": itemId}