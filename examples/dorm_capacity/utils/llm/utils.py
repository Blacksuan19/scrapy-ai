from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar

import pandas as pd
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


LLMOutput = Dict[str, Any]
CombinedLLMOutput = LLMOutput | List[LLMOutput]
LLMItemType = TypeVar("LLMItemType", CapacityInfo, LLMDormItem)


def flatten_dict(items: List[LLMOutput]) -> CombinedLLMOutput:
    """
    Flatten nested dicts in each item to attributes.

    Example:
    >>> items = [
        {
            "name": "John",
            "address": {"city": "New York", "state": "NY"},
            "contact": {"email": "test@test.com, "phone": "1234567890"}
        }
    ]

    >>> flatten_items(items) -> [
        {
            "name": "John",
            "city": "New York",
            "state": "NY",
            "email": "test@test.com",
            "phone": "1234567890"
        }
    ]
    """

    nested_keys, flat_items = set(), []

    # find all nested keys
    for item in items:
        for key, value in item.items():
            if isinstance(value, dict):
                nested_keys.add(key)

    # avoid messing up the original list
    if not nested_keys:
        return items.pop()

    for item in items:
        item_df = pd.DataFrame([item])
        for key in nested_keys:
            if key not in item_df.columns:
                continue
            item_df = pd.concat(
                [item_df, pd.DataFrame(item_df[key].tolist())], axis=1
            ).drop(key, axis=1)

            flat_items.append(item_df.to_dict(orient="records").pop())

    # single item
    if len(flat_items) == 1:
        return flat_items.pop()

    return flat_items
