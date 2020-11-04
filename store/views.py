from django.shortcuts import render, redirect
from django.views import generic

import re, json
from pprint import pprint

from .forms import MetadataForm, SchemaForm, SchemaFormset

def widget_input_type(field):
    """This function takes a form field and extracts a field type."""
    try: # CharField ==> "text"
        input_type = field.field.widget.input_type
    except AttributeError: # Workaround for the fact that Textarea does not have an input type.
        input_type = 'textarea'
    return input_type

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

            title = metadata_form.cleaned_data['title']

            form_field_type_by_name = {f.name : widget_input_type(f) for f in metadata_form.visible_fields()}

            avro_schema = {
               "name" : title.replace(' ', ''),
               "type" : "record",
               "namespace" : "com.acme.avro",
               }
            field_type = {"title": "string", "notes": "string"}
            for key, value in metadata_form.cleaned_data.items():
                if value:
                    if key in form_field_type_by_name.keys():
                        field_type = avro_type_by_input_type[form_field_type_by_name[key]]
                        if key in ['private']:
                            field_type = "boolean"
                        avro_schema[key] = value
                        #if field_type == 'boolean':
                        #    avro_schema[key] = (value == "True")
                        #else:
                        #    avro_schema[key] = value
                    else:
                        print(f"{key} is not a dataset metadata field.")


            schema_fields = []
            for k, sf in enumerate(formset):
                fieldname = sf.cleaned_data.get('fieldname', '')
                if fieldname != "":
                    fieldtype = sf.cleaned_data['fieldtype']
                    required = sf.cleaned_data['required']
                    example = sf.cleaned_data['example']
                    if len(example) == 0:
                        example = None
                    if required:
                        type_value = fieldtype
                    else:
                        type_value = ["null", fieldtype]

                    if example is not None:
                        schema_fields.append({"name": fieldname, "type": type_value, "example": example})
                    else:
                        schema_fields.append({"name": fieldname, "type": type_value})

            avro_schema["fields"] = schema_fields

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
    else: # Handle requests that are neither GET nor POST requests (like HEAD)
        metadata_form = MetadataForm()
        formset = SchemaFormset()

    return render(request, template_name, {
        'metadata_form': metadata_form,
        'formset': formset,
        'heading': heading_message,
        'avro_schema': None
    })
