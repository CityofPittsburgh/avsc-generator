# avsc-generator
App for generating .avsc schemas for Data Rivers

This web app provides an HTML form that serves as a front end for creating
Avro schemas to represent dataset. The dataset fields come from the CKAN
metadata on [data.wprdc.org](https://data.wprdc.org).

### Setup

The repository is currently a Django app, which can be added to an existing Django 3.0.3 project by
changing to the Django project directory, cloning this repository into the directory

`git clone https://github.com/CityofPittsburgh/avsc-generator.git`

wiring up URLs by adding this Django app to the Django project's urls.py file

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generator/', include('avsc-generator.urls', namespace='generator') ), # Add a line like this.
]
```

and inserting the directory name that contains the app into the INSTALLED_APPS list in the settings.py
file:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'avsc-generator'
]
```

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

The python watchdog script finds these `time_field`s and the associated resource IDs, performs a SQL
query to find the earliest and latest timestamps in the corresponding column, and updates the
`temporal_coverage` field of the metadata to reflect these results. In this way, the `temporal_coverage`
field can actually represent the contents of the tables within the dataset (rather than the
intended coverage).
