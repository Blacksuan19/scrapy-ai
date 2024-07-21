# Scrapy-LLM

LLM integration for scrapy as a middleware.

[![view - Documentation](https://img.shields.io/badge/PyPi-0.1.0-blue?style=for-the-badge)](https://pypi.org/project/scrapy-llm "view package on PyPi")
&nbsp;&nbsp;&nbsp;
<!-- [![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](https://redash.blacksuan19.dev/ "go to documentation") -->
<!-- &nbsp;&nbsp;&nbsp; -->
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](# "Build with github actions")

## Installation

```bash
pip install scrapy-llm
```

## Usage

```python
# settings.py
DOWNLOADER_MIDDLEWARES = {
    'scrapy_llm.handler.LlmExtractorMiddleware'
    ...
}
```
