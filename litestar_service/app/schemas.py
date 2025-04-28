from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from .models import OfferChoices


class OfferBase(BaseModel):
    uuid: UUID
    id: int
    url: Optional[str] = None
    is_active: bool
    name: OfferChoices
    sum_to: Optional[str] = None
    term_to: Optional[int] = None
    percent_rate: Optional[int] = None

    class Config:
        from_attributes = True


class OfferWallOfferBase(BaseModel):
    offer: OfferBase

    class Config:
        from_attributes = True


class OfferWallPopupOfferBase(BaseModel):
    offer: OfferBase

    class Config:
        from_attributes = True


class OfferWallBase(BaseModel):
    token: UUID
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str]

    class Config:
        from_attributes = True
