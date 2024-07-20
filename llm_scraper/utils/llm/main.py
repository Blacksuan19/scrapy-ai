from os import environ
from typing import Iterable, List

import instructor
from litellm import completion

from llm_scraper.utils.llm.utils import CombinedLLMOutput, LLMItemType, flatten_dict


def extract_item_data(
    clean_html: str, response_model: LLMItemType
) -> CombinedLLMOutput:
    """Extract dorm data from the given HTML text using an LLM model."""

    print("Extracting dorm data from the given HTML text using mamba model")

    cl = instructor.from_litellm(completion)

    resp: List[response_model] = cl.chat.completions.create(
        model="gpt-4-turbo",
        api_base=environ.get("LLM_API_BASE"),
        custom_llm_provider="openai",  # api_base is an API based on openAI API spec.
        temperature=0.0001,  # very low temperature to prevent hallucinations.
        messages=[
            {
                "role": "system",
                "content": "Your role is to extract the dorm capacity data from the given text according to the provided schema. make sure your output is a valid JSON object.",
            },
            {"role": "user", "content": clean_html},
        ],
        # always return an iterable of the given type to simplify nested type cascading.
        response_model=Iterable[response_model],
    )

    items = [item.model_dump() for item in resp]

    return flatten_dict(items)
