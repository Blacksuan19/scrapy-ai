from typing import Any, Dict, List, TypeVar

from pydantic import BaseModel

LLMOutput = Dict[str, Any]
CombinedLLMOutput = LLMOutput | List[LLMOutput]

T = TypeVar("T", bound=BaseModel)
