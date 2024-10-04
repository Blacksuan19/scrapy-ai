import html2text
import pandas as pd

from scrapy_llm.types import CombinedLLMOutput, T


def process_html(
    html: str,
    ignore_links: bool = True,
    ignore_images: bool = True,
) -> str:
    """
    Process HTML to plain text using html2text.

    Args:
        html (str): The HTML to process.
        ignore_links (bool): Whether to ignore links. Defaults to True.
        ignore_images (bool): Whether to ignore images. Defaults to True.

    Returns:
        str: The processed plain text.
    """
    cleaner = html2text.HTML2Text()
    cleaner.ignore_links = ignore_links
    cleaner.ignore_images = ignore_images
    clean_content = cleaner.handle(html)
    return clean_content


def flatten_dict(items: T) -> CombinedLLMOutput:
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
