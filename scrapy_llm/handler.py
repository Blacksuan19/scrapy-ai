from typing import Generic, Iterable, List, Type, TypeVar

import instructor
from litellm import completion
from scrapy import Request, signals
from scrapy.crawler import Crawler
from scrapy.http.response import Response
from scrapy.spiders import Spider
from scrapy.utils.log import logger
from scrapy.exceptions import NotConfigured

from scrapy_llm.config import LLM_EXTRACTED_DATA_KEY, LLM_RESPONSE_MODEL_KEY, LlmExtractorConfig
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
        response_model = request.meta.get(LLM_RESPONSE_MODEL_KEY) or self.config.response_model
        if not response_model:
            raise NotConfigured(
                """
                Response model not provided for LlmExtractorMiddleware.
                Please set LLM_RESPONSE_MODEL to class path in settings, define response_model in the spider, or provide response model object in Request meta.
                """
            )

        extracted_data = self.extract_item_data(
            response.text, response_model, request.url
        )

        if self.config.unwrap_nested:
            extracted_data = flatten_dict(extracted_data)

        request.meta[LLM_EXTRACTED_DATA_KEY] = extracted_data

        return response

    def spider_opened(self, spider: Spider) -> None:
        spider.logger.info("Spider opened: %s" % spider.name)

    def extract_item_data(
        self,
        raw_html: str,
        response_model: Type[T],
        url: str,
    ) -> List[LLMOutput]:
        """Extract data from the given HTML text using an LLM model."""

        cl = instructor.from_litellm(completion)

        system_message = f"{self.config.llm_system_message.format(url=url)} {self.config.llm_additional_system_message}"

        resp: List[response_model] = cl.chat.completions.create(
            model=self.config.llm_model,
            api_base=self.config.llm_api_base,
            custom_llm_provider="openai",
            temperature=self.config.llm_temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": process_html(
                        raw_html,
                        self.config.html_cleaner_ignore_links,
                        self.config.html_cleaner_ignore_images,
                    ),
                },
            ],
            # always return an iterable of the given type to simplify nested type cascading.
            response_model=Iterable[response_model],
        )

        items = [item.model_dump() for item in resp]

        return items
