# Scrapy-LLM

LLM integration for scrapy as a middleware.

[![view - Documentation](https://img.shields.io/badge/PyPi-0.1.9-blue?style=for-the-badge)](https://pypi.org/project/scrapy-llm "view package on PyPi")
&nbsp;&nbsp;&nbsp;
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](# "Build with github actions")

## Installation

```bash
pip install scrapy-llm
```

## Usage

```python
# settings.py

# set the response model to use for extracting data to a pydantic model (required)
# or set it as an attribute on the spider class as response_model
LLM_RESPONSE_MODEL = 'scraper.models.ResponseModel'

# enable the middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy_llm.handler.LlmExtractorMiddleware': 543,
    ...
}
```

then access extracted data from the response object.

```python
# spider.py
def parse(self, response):
    extracted_data: Dict[str, Any] = response.request.meta.get('llm_extracted_data')
    ...
```

## Examples

the [examples](./examples/) directory contains a sample scrapy project that uses the middleware to extract capacity data from university websites.

to run the example project, export your openai api key as an environment variable, in addition to any other settings you want to change.

```bash
export OPENAI_API_KEY=<your-api-key>
```

then run the example project using the following command

```bash
cd examples
scrapy crawl generic -a urls_file=urls.csv

```

add more urls to the `urls.csv` file to extract data from more websites.

## Configuration

All aspects of the middleware can be configured using the `settings.py` file except the API key which should be set as the environment variable `OPENAI_API_KEY` according to the openai api documentation [here](https://beta.openai.com/docs/api-reference/authentication).

### `LLM_RESPONSE_MODEL`

- type: str
- required: True

the response model to use for extracting data from the web page text.

```python
RESPONSE_MODEL = 'scraper.models.ResponseModel'
```

this setting can also be set as an attribute on the spider class itself, in that case the class should be used directly instead of a string path to the class.

```python
class MySpider(scrapy.Spider):
    response_model = ResponseModel
    ...
```

### `LLM_UNWRAP_NESTED`

- type: bool
- required: False
- default: True

whether to unwrap nested models in the extracted data.

```python
LLM_UNWRAP_NESTED = True
```

for example if the following model is used

```python
class ContactInfo(BaseModel):
    phone: str

class Person(BaseModel):
    name: str
    contact_info: ContactInfo
```

the extracted data will be unwrapped to

```json
{
    "name": "John Doe",
    "phone": "1234567890"
}
```

without unwrapping the data will be

```json
{
    "name": "John Doe",
    "contact_info": {
        "phone": "1234567890"
    }
}
```

### `LLM_API_BASE`

- type: str
- required: False
- default: <https://api.openai.com/v1>

base url for the openai compatible api.

```python
LLM_API_BASE = 'https://api.openai.com/v1'
```

### `LLM_MODEL`

- type: str
- required: False
- default: "gpt-4-turbo"

the language model to use for extracting data from the web page text.

```python
LLM_MODEL = 'gpt-4-turbo'
```

### `LLM_MODEL_TEMPERATURE`

- type: float
- required: False
- default: 0.0001

the temperature to use for the language model.

```python
LLM_MODEL_TEMPERATURE = 0.0001
```

### `LLM_SYSTEM_MESSAGE`

- type: str
- required: False
- default: You are a data extraction expert, your role is to extract data from the given text according to the provided schema. make sure your output is a valid JSON object.

the system message to use for the language model.

```python
LLM_SYSTEM_MESSAGE = '...'
```

## Under the hood

Under the hood, `scrapy-llm` utilizes two libraries to facilitate data extraction from web page text. The first library is [Instructor](https://python.useinstructor.com/), which uses pydantic to define a schema for the extracted data. This schema is then used to validate the extracted data and ensure that it conforms to the desired structure. By defining a schema for the extracted data, Instructor provides a clear and consistent way to organize and process the extracted information.

The second library is LiteLLM, which enables seamless integration between instructor and any API compatible with the OpenAI API specification. LiteLLM allows using any language model as long as it is deployed on an API compatible with the OpenAI [API specification](https://platform.openai.com/docs/api-reference/introduction). This flexibility makes it easy to switch between different language models and experiment with different configurations to find the best model for a given task.

By combining the functionalities of Instructor and LiteLLM, `scrapy-llm` becomes a robust tool for extracting data from web page text. Whether it's scraping a single page or crawling an entire website, `scrapy-llm` offers a reliable and adaptable solution for all data extraction needs.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
