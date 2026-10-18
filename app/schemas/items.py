import uuid

from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    category: str | None
    image_url: str
    embedding: list[float] | None
    subcategory: str | None = None
    style: str | None = None
    color_hex: str | None = None
    processing_status: str = "ready"


class ItemSuggestResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    category: str
    image_url: str
    subcategory: str | None = None
    style: str | None = None
    color_hex: str | None = None


class OutfitSuggestionResponse(BaseModel):
    items: list[ItemSuggestResponse]
    score: float | None
    message: str | None = None


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
