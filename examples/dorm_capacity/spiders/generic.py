from typing import Any, Dict, Iterable

import pandas as pd
import scrapy
from dorm_capacity.utils.models import LLMDormItem
from scrapy import Request
from scrapy.http.response.html import HtmlResponse


class GenericSpider(scrapy.Spider):
    """
    Generic spider for scraping generic dorm capacity data.

    Args:
        urls_file: csv file containing URLs to scrape.

    expected csv file format:

    ```csv\n
    url
    https://example.com
    https://example2.com
    ```
    """

    name = "generic"
    response_model = LLMDormItem

    def __init__(self, urls_file: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # urls_file is a csv file with a column named "url"
        url_df = pd.read_csv(urls_file, index_col=False)
        self.start_urls = url_df["url"].tolist()

    def start_requests(self) -> Iterable[Request]:
        """
        Start requests for each of `self.start_urls`.
        """
        for url in self.start_urls:
            yield Request(url=url)

    def parse(self, response: HtmlResponse) -> Dict[str, Any]:
        return response.request.meta.get("llm_extracted_data")
