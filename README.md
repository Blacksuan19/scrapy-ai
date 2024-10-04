# Scrapy-LLM

LLM integration for Scrapy as a middleware. Extract any data from the web using your own predefined schema with your own preferred language model.

[![view - Documentation](https://img.shields.io/badge/PyPi-0.1.18-blue?style=for-the-badge)](https://pypi.org/project/scrapy-llm "view package on PyPi")
&nbsp;&nbsp;&nbsp;
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](# "Build with github actions")

## Features

- Extract data from web page text using a language model.
- Define a schema for the extracted data using pydantic models.
- Validate the extracted data against the defined schema.
- Seamlessly integrate with any API compatible with the OpenAI API specification.
- Use any language model deployed on an API compatible with the OpenAI API specification.

## Installation

```bash
pip install scrapy-llm
```

## Usage

The guide below assumes that a Scrapy project has already been set up. If not, follow the [official Scrapy tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) to create a new project.

Setup the middleware in the `settings.py` file and define the response model to use for extracting data from the web page text.

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
from scrapy_llm.config import LLM_EXTRACTED_DATA_KEY
from scraper.models import ResponseModel

class MySpider(scrapy.Spider):
    name = 'my_spider'
    response_model = ResponseModel # set the response model as an attribute on the spider class if not set in settings
    
    def parse(self, response):
        extracted_data = response.request.meta.get(LLM_EXTRACTED_DATA_KEY)
        ...
```

### Creating a response model

Response models are used to define the schema for the extracted data. The schema is used to validate the extracted data and ensure that it conforms to the desired structure. The response model should be a pydantic model with the desired fields and types. pydantic has support for many types including custom types like regex based types, emails, enums and more, for a full list of supported types check the [pydantic documentation](https://pydantic-docs.helpmanual.io/usage/types/).

In addition to the officially supported types there are other third-party libraries that add support for more types such as [pydantic-extra-types](https://docs.pydantic.dev/2.0/usage/types/extra_types/extra_types/) which adds support for phone numbers, credit card numbers, and more. alternatively, custom types can be created by subclassing the `pydantic.BaseModel` class.

when defining the response model, adding descriptions and examples for each field is recommended to improve the quality of the extracted data. instructor will use these descriptions to guide the language model in generating the output. it is also recommended to make fields that the model has a hard time extracting or are not always present optional, this will prevent the entire process from failing if a field is not extracted.

```python
# models.py
from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional

# create a custom pydantic type
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class ResponseModel(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(description="The age of the person")
    phone: Optional[PhoneNumber] = Field(
        description="The phone number of the person", example="123-456-7890"
    )
    email: Optional[EmailStr] = Field(description="The email of the person")
    address: Optional[Address] = Field(
        description="The address of the person",
        example={
            "street": "123 Main St",
            "city": "Anytown",
            "state": "NY",
            "zip_code": "12345",
        },
    )
```

### Using multiple response models

If you need to scrape multiple webpages with different schemas, you can define multiple response models and pass them directly to the middleware. Suppose you have the following models:

```python
# models.py
from pydantic import BaseModel, Field
from pydantic_string_url import HttpUrl
from typing import Optional

class ModelA(BaseModel):
    field1: str = Field(description="The first field")
    field2: int = Field(description="The second field")
    subpage_url: Optional[HttpUrl] = Field(description="The URL of the subpage. This will be a link to a page using ModelB as the response model.")

class ModelB(BaseModel):
    field3: str = Field(description="The third field")
    field4: float = Field(description="The fourth field")
```

You can then pass the appropriate model to the middleware based on the webpage you are scraping. For example:

```python
# spider.py
import scrapy

from scrapy.http.response.html import HtmlResponse
from scrapy_llm.config import LLM_EXTRACTED_DATA_KEY, LLM_RESPONSE_MODEL_KEY

from scraper.models import ModelA, ModelB

class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_url = 'https://example.com/model-a'

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_model_a, meta={LLM_RESPONSE_MODEL_KEY: ModelA})

    def parse_model_a(self, response: HtmlResponse):
        extracted_data = response.request.meta.get(LLM_EXTRACTED_DATA_KEY)
        if (len(extracted_data) > 0):
            yield extracted_data[0]
            subpage_url = extracted_data[0].subpage_url
            if subpage_url is not None:
                yield scrapy.Request(subpage_url, callback=self.parse_model_b, meta={LLM_RESPONSE_MODEL_KEY: ModelB})

    def parse_model_b(self, response: HtmlResponse):
        # handle the model b response here
```

You can still set the response model using the `LLM_RESPONSE_MODEL` setting if you want to, in which case that model will be used if no model is passed to the middleware.

## Examples

the [examples](./examples/) directory contains a sample Scrapy project that uses the middleware to extract capacity data from university websites.

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

when using an API that does not require an API key, the `OPENAI_API_KEY` environment variable can be set to any value.

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
