from typing import Generic, Iterable, List, Type, TypeVar

import instructor
from litellm import completion
from scrapy import Request, signals
from scrapy.crawler import Crawler
from scrapy.http.response import Response
from scrapy.spiders import Spider

from scrapy_llm.config import LlmExtractorConfig
from scrapy_llm.types import LLMOutput, T
from scrapy_llm.utils import flatten_dict, process_html

LLMExtractor = TypeVar("LLMExtractor", bound="LlmExtractorMiddleware")


class LlmExtractorMiddleware(Generic[T]):
    def __init__(
        self,
        crawler: Crawler,
        config: LlmExtractorConfig,
    ):
        self.crawler = crawler
        self.config = config

    @classmethod
    def from_crawler(cls: Type[LLMExtractor], crawler: Crawler) -> LLMExtractor:
        config = LlmExtractorConfig.from_crawler(crawler)
        instance = cls(crawler, config)
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def process_response(
        self, request: Request, response: Response, spider: Spider
    ) -> Response:
        extracted_data = self.extract_item_data(
            response.text, self.config.response_model
        )

        if self.config.unwrap_nested:
            extracted_data = flatten_dict(extracted_data)

        request.meta["llm_extracted_data"] = extracted_data

        return response

    def spider_opened(self, spider: Spider) -> None:
        spider.logger.info("Spider opened: %s" % spider.name)

    def extract_item_data(
        self,
        raw_html: str,
        response_model: Type[T],
    ) -> List[LLMOutput]:
        """Extract dorm data from the given HTML text using an LLM model."""

        cl = instructor.from_litellm(completion)

        resp: List[response_model] = cl.chat.completions.create(
            model=self.config.llm_model,
            api_base=self.config.llm_api_base,
            custom_llm_provider="openai",
            temperature=self.config.llm_temperature,
            messages=[
                {
                    "role": "system",
                    "content": self.config.llm_system_message,
                },
                {"role": "user", "content": process_html(raw_html)},
            ],
            # always return an iterable of the given type to simplify nested type cascading.
            response_model=Iterable[response_model],
        )

        items = [item.model_dump() for item in resp]

        return items
