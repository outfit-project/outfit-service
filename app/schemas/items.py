import uuid

from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    category: str
    image_url: str
    embedding: list[float] | None


class ItemSuggestResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    category: str
    image_url: str


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int