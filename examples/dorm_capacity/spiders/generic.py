from typing import Any, Dict, Iterable, List

import pandas as pd
import scrapy
from dorm_capacity.utils.llm.main import extract_item_data
from dorm_capacity.utils.llm.utils import LLMDormItem
from dorm_capacity.utils.text import process_html
from scrapy import Request
from scrapy.http.response.html import HtmlResponse

ResponseType = Dict[str, Any]


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
    urls: List[str] = []

    def __init__(self, urls_file: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # urls_file is a csv file with a column named "url"
        url_df = pd.read_csv(urls_file, index_col=False)
        self.start_urls = url_df["url"].tolist()

        print(f"Scraping {len(self.urls)} URLs")
        print(self.urls)

    def start_requests(self) -> Iterable[Request]:
        """
        Start requests for each of `self.start_urls`.
        """
        for url in self.start_urls:
            yield Request(url=url)

    def parse(self, response: HtmlResponse) -> ResponseType:
        return extract_item_data(
            process_html(response.text), response_model=LLMDormItem
        )
