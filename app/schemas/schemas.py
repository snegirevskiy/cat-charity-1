from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CharityProjectCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    full_amount: Optional[int] = Field(None, gt=0)


class CharityProjectDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None


class DonationCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    full_amount: int = Field(..., gt=0)
    comment: Optional[str] = None


class DonationDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime


class DonationFullInfoDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
