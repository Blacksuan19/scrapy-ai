import importlib
from dataclasses import dataclass
from typing import Optional, Type

from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured

from scrapy_llm.types import T


@dataclass
class LlmExtractorConfig:
    response_model: Type[T]
    unwrap_nested: bool = False
    llm_api_base: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4-turbo"
    llm_temperature: float = 0.0001
    llm_system_message: str = (
        "You are a data extraction expert, your role is to extract data from the given text according to the provided schema. make sure your output is a valid JSON object."
    )

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "LlmExtractorConfig":
        api_base: str = crawler.settings.get("LLM_API_BASE", cls.llm_api_base)
        system_message: str = crawler.settings.get(
            "LLM_SYSTEM_MESSAGE", cls.llm_system_message
        )
        model: str = crawler.settings.get("LLM_MODEL", cls.llm_model)
        model_tempature: float = crawler.settings.get(
            "LLM_MODEL_TEMPERATURE", cls.llm_temperature
        )
        response_model_path: str = crawler.settings.get("LLM_RESPONSE_MODEL", None)
        unwrap_nested: bool = crawler.settings.get(
            "LLM_UNWRAP_NESTED", cls.unwrap_nested
        )
        response_model: Optional[Type[T]] = getattr(
            crawler.spider, "response_model", None
        )

        if not response_model and response_model_path:
            module_path, class_name = response_model_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            response_model = getattr(module, class_name)
        elif not response_model:
            raise NotConfigured(
                "Response model not provided for LlmExtractorMiddleware, Please set LLM_RESPONSE_MODEL to class path in settings or define response_model in the spider."
            )

        return cls(
            response_model=response_model,
            llm_api_base=api_base,
            unwrap_nested=unwrap_nested,
            llm_model=model,
            llm_temperature=model_tempature,
            llm_system_message=system_message,
        )
