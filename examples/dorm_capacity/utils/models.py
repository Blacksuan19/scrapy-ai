from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RoomType(str, Enum):
    """Available room types."""

    single = "single"
    double = "double"
    triple = "triple"
    quad = "quad"
    studio = "studio"
    suite = "suite"
    apartment = "apartment"
    shared = "shared"
    other = "other"


class CapacityInfo(BaseModel):
    """
    Model of capacity data extracted from the LLM model.
    everything is optional to prevent pydantic validation failure.
    """

    n_person: Optional[int] = Field(
        description="Total number of people the place can accommodate."
    )
    n_unit: Optional[int] = Field(description="Total number of units available if any.")
    n_building: Optional[int] = Field(
        description="Total number of buildings in the property."
    )
    n_floor: Optional[int] = Field(
        description="total number of floors in the building."
    )

    room_types: Optional[List[RoomType]] = Field(
        description="available room types, mention each type only once with a single word.",
        example=["single", "double"],
    )


class LLMDormItem(BaseModel):
    """
    Model of dorm data extracted from the LLM model.
    everything is optional to prevent pydantic validation failure.
    """

    name: str = Field(description="Name of the dorm")
    address: Optional[str] = Field(
        description="Physical address of the dorm or university including zip code and state."
    )
    telephone: Optional[str] = Field(
        description="Telephone number of the dorm or university."
    )
    email: Optional[str] = Field(description="Email address of the dorm or university")

    room_types: Optional[List[RoomType]] = Field(
        description="available room types, mention each type only once with a single word.",
        example=["single", "double"],
    )

    capacity: Optional[CapacityInfo] = Field(
        description="Capacity data of the dorm.",
        example={"n_person": 100, "n_unit": 50, "n_building": 5, "n_floor": 3},
    )
