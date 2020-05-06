from django.shortcuts import render, redirect
from django.views import generic

import json
from pprint import pprint

from .forms import MetadataForm, SchemaForm, SchemaFormset

def widget_input_type(field):
    """This function takes a form field and extracts a field type."""
    try: # CharField ==> "text"
        input_type = field.field.widget.input_type
    except AttributeError: # Workaround for the fact that Textarea does not have an input type.
        input_type = 'textarea'
    return input_type

def make_metadata_fieldname(s):
    """Prepend a string to the metadata fieldname to distinguish it from possible schema
    fieldnames (which are going to also be put into the Avro schema)."""
    return "dataset" + s

def get_metadata_and_schema(request):
    template_name = 'store/generator.html'
    heading_message = 'Schema Generator'
    if request.method == 'GET':
        metadata_form = MetadataForm(request.GET or None)
        formset = SchemaFormset(request.GET or None)
    elif request.method == 'POST':
        avro_type_by_input_type = {"text": "string", "textarea": "string",
            "select": "string" # This is a ChoiceField, so technically
            # the value could be something other than a string.
            }
        metadata_form = MetadataForm(request.POST)
        formset = SchemaFormset(request.POST)
        if metadata_form.is_valid() and formset.is_valid():

            title = metadata_form.cleaned_data['_title']

            form_field_type_by_name = {f.name : widget_input_type(f) for f in metadata_form.visible_fields()}

            dataset_fields_list = []
            field_type = {"_title": "string", "_notes": "string"}
            for key, value in metadata_form.cleaned_data.items():
                if value:
                    if key in form_field_type_by_name.keys():
                        field_type = avro_type_by_input_type[form_field_type_by_name[key]]
                        dataset_fields_list.append({"name": make_metadata_fieldname(key), "type": field_type, "default": value})
                    else:
                        print(f"{key} is not a dataset metadata field.")


            schema_fields = []
            for k, sf in enumerate(formset):
                fieldname = sf.cleaned_data['fieldname']
                if fieldname in [make_metadata_fieldname(f.name) for f in metadata_form.visible_fields()]:
                    context = {'heading': f"Unable to add a data-table field with a fieldname ({fieldname}) that conflicts with the metadata fieldnames.",
                            'avro_schema': None,
                            'metadata_form': metadata_form,
                            'formset': formset}
                    return render(request, template_name, context)

                if fieldname != "":
                    fieldtype = sf.cleaned_data['fieldtype']
                    schema_fields.append({"name": fieldname, "type": fieldtype})

            avro_schema = {
               "type" : "record",
               "namespace" : "dataset_schemas+metadata",
               "name" : title,
               "fields" : dataset_fields_list + schema_fields
               }

            # Show the results.
            context = {
                    'heading': heading_message,
                    'avro_schema': json.dumps(avro_schema, indent=4)
                }

        else:
            context = {'heading': heading_message, #"Invalid form. Some mandatory field was probably left out. Try again!",
                    'avro_schema': None }
        context['metadata_form'] = MetadataForm(request.POST or None)
        context['formset'] = SchemaFormset(request.POST or None)

        return render(request, template_name, context)

    return render(request, template_name, {
        'metadata_form': metadata_form,
        'formset': formset,
        'heading': heading_message,
        'avro_schema': None
    })
