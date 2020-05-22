# avsc-generator
App for generating .avsc schemas for Data Rivers

This web app provides an HTML form that serves as a front end for creating
Avro schemas to represent dataset. The dataset fields come from the CKAN
metadata on [data.wprdc.org](https://data.wprdc.org).

### Setup

The repository is a Django 3 project, which can be set up by cloning it to your machine:

`git clone https://github.com/CityofPittsburgh/avsc-generator.git`

Then change to the `avsc-generator` directory and run

`pip install -r requirements.txt`

to install the necessary requirements. This assumes that Python 3.6+ and pip are already installed. (A Python version of 3.6 or higher is required to support the use of f-strings.)

To test it, run

`python manage.py runserver`

and access the project by going to [http://127.0.0.1:8000/generator](http://127.0.0.1:8000/generator/) in a browser.

### Notes on the 'temporal_coverage' field

While the `temporal_coverage` field was initially only manually set by the people configuring the dataset,
some datasets (such as the 311 dataset) now have their temporal_coverage automatically set by a Python
script that periodically checks all datasets for `time_field` definitions. This dataset has a `time_field`
defined for one of its resources (the main 311 data). This definition is set in one of the list of dicts
in the `extras` metadata, like this:

```python
'extras': [{'key': 'time_field',
             'value': '{"76fda9d0-69be-4dd5-8108-0de7907fc5a4": '
                      '"CREATED_ON"}'}],
```

This can be read as follows: 1) There is at least one `time_field` defined for this dataset.
2) The `time_field`-defining dict has the form `{<resource_id_1>: <fieldname in resource_id_1 table
which is a parsable timestamp>, <resource_id_2>: ...}`.
3) Here it is just one resource which has a defined timestamp, and that timestamp can be found
in the `CREATED_ON` field.

The Python watchdog script finds these `time_field`s and the associated resource IDs, performs a SQL
query to find the earliest and latest timestamps in the corresponding column, and updates the
`temporal_coverage` field of the metadata to reflect these results. In this way, the `temporal_coverage`
field can actually represent the contents of the tables within the dataset (rather than the
intended coverage).
