from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

MIN_NAME_LENGTH = 5
MAX_NAME_LENGTH = 100
MIN_DESCRIPTION_LENGTH = 10
MIN_AMOUNT = 0


class CharityProjectCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: int = Field(..., gt=MIN_AMOUNT)


class CharityProjectUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: Optional[str] = Field(None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: Optional[int] = Field(None, gt=MIN_AMOUNT)


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

    full_amount: int = Field(..., gt=MIN_AMOUNT)
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
