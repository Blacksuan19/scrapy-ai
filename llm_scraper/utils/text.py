import html2text
from gensim.parsing.preprocessing import (
    preprocess_string,
    remove_stopwords,
    split_alphanum,
    strip_multiple_whitespaces,
    strip_non_alphanum,
    strip_punctuation,
)


def process_html(html: str) -> str:
    """
    Process HTML to plain text.

    Args:
        html (str): The HTML to process.

    Returns:
        str: The processed plain text.
    """

    transforms = [
        strip_non_alphanum,
        split_alphanum,
        strip_multiple_whitespaces,
        strip_punctuation,
        remove_stopwords,
    ]

    cleaner = html2text.HTML2Text()
    cleaner.ignore_links = True
    cleaner.ignore_images = True
    clean_content = cleaner.handle(html)
    clean_content = preprocess_string(clean_content, filters=transforms)

    return " ".join(clean_content)
