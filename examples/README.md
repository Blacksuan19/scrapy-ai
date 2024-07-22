# Examples

the [dorm_capacity](./dorm_capacity) directory contains a sample scrapy project that uses the middleware to extract capacity data from university websites.

to run the example project, export your openai api key as an environment variable, in addition to any other settings you want to change.

```bash
export OPEN_AI_API_KEY=<your-api-key>
```

then run the example project using the following command

```bash
cd examples
scrapy crawl generic -a urls_file=urls.csv
```

## Extracted Data

The dorm capacity example project extracts data from urls given in `urls.csv` according to the below schema:

```python
class LLMDormItem(BaseModel):
    """
    Model of dorm data extracted from the LLM model.
    everything is optional to prevent pydantic validation failure.
    """

    name: str = Field(description="Name of the dorm")
    address: Optional[str] = Field(
        description="Physical address of the dorm or university including zip code and state."
    )
    telephone: Optional[str] = Field(
        description="Telephone number of the dorm or university."
    )
    email: Optional[str] = Field(description="Email address of the dorm or university")

    capacity: Optional[CapacityInfo] = Field(
        description="Capacity data of the dorm.",
        example={
            "n_person": 100,
            "n_unit": 50,
            "n_building": 5,
            "n_floor": 3,
            "room_types": ["single", "double"],
        },
    )
```

for full details of the data model see [models.py](./dorm_capacity/utils/models.py).

the extracted data is saved to a file with the spider name in the `results` folder. here is a snippet of the extracted data for the url <https://www.bgsu.edu/residence-life/housing-options/centennial-hall1.html>:

```json
{
    "name":"Centennial Hall",
    "address":"1101 E. Wooster St., Bowling Green, OH 43403-4003",
    "telephone":"419-372-4050",
    "email":"ivyem@bgsu.edu",
    "capacity":{
        "n_person":600,
        "n_unit":null,
        "n_building":1,
        "n_floor":null,
        "room_types":[
            "double",
            "single"
        ]
    }
}
```
