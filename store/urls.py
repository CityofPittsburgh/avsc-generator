from django.urls import re_path

from .views import (
    get_metadata_and_schema,
)

app_name = 'generator'

urlpatterns = [

    re_path(r'^', get_metadata_and_schema, name='get_metadata_and_schema'),

]
