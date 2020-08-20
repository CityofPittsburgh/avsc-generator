from django import forms
from django.forms import formset_factory


def convert_to_choices_format(xs):
    return [(x, x) for x in xs]


class MetadataForm(forms.Form):
    LICENSE_ID_BY_TITLE = {"Creative Commons Attribution": "cc-by",
                           "Creative Commons Attribution Share-Alike": "cc-by-sa",
                           "Creative Commons CCZero": "cc-zero",
                           "Creative Commons Non-Commercial (Any)": "cc-nc",
                           "GNU Free Documentation License": "gfdl",
                           "License not specified": "notspecified",
                           "Open Data Commons Attribution License": "odc-by",
                           "Open Data Commons Open Database License (ODbL)": "odc-odbl",
                           "Open Data Commons Public Domain Dedication and License (PDDL)": "odc-pddl",
                           "Other (Attribution)": "other-at",
                           "Other (Non-Commercial)": "other-nc",
                           "Other (Not Open)": "other-closed",
                           "Other (Open)": "other-open",
                           "Other (Public Domain)": "other-pd",
                           "UK Open Government Licence (OGL)": "uk-ogl"}
    LICENSE_TITLES = ["Creative Commons Attribution",
                      "Creative Commons Attribution Share-Alike",
                      "Creative Commons CCZero",
                      "Creative Commons Non-Commercial (Any)",
                      "GNU Free Documentation License",
                      "License not specified",
                      "Open Data Commons Attribution License",
                      "Open Data Commons Open Database License (ODbL)",
                      "Open Data Commons Public Domain Dedication and License (PDDL)",
                      "Other (Attribution)",
                      "Other (Non-Commercial)",
                      "Other (Not Open)",
                      "Other (Open)",
                      "Other (Public Domain)",
                      "UK Open Government Licence (OGL)"]
    LICENSE_TITLE_CHOICES = convert_to_choices_format(LICENSE_TITLES)
    DEPARTMENTS = ["Department of City Planning", "Bureau of Animal Care &amp; Control; Department of Public Safety",
                   "Citiparks", "City Clerks Office", "City Controller", "City Council",
                   "Emergency Management Agency; Department of Public Safety",
                   "Emergency Medical Services; Department of Public Safety",
                   "Department of Finance", "Fire Bureau; Department of Public Safety",
                   "Department of Innovation &amp; Performance",
                   "Law Department", "Mayor's Office", "Department of Mobility and Infrastructure",
                   "Office of Municipal Investigations",
                   "Pension Office", "Department of Personnel and Civil Service Commission",
                   "Police Bureau; Department of Public Safety",
                   "Department of Public Safety", "Department of Public Works", "Office of Management and Budget",
                   "Department of Permits, Licenses, and Inspections", "External"]
    DEPARTMENT_CHOICES = convert_to_choices_format(DEPARTMENTS)
    DEPARTMENT_CHOICES[1] = ("Bureau of Animal Care &amp; Control; Department of Public Safety",
                             "Bureau of Animal Care & Control; Department of Public Safety")
    ACCESS_LEVEL_CHOICES = [(True, "Private"), (False, "Public")]
    GEOGRAPHIC_UNIT_CHOICES = [("", ""), ("Not Applicable", "N/A"), ("Latitude/Longitude", "Latitude/Longitude"),
                               ("Street Address", "Street Address"),
                               ("Intersection/Street Segment", "Intersection/Street Segment"),
                               ("Parcel (Block/Lot)", "Parcel (Block/Lot)"), ("Census Block", "Census Block"),
                               ("Census Block Group", "Census Block Group")] + convert_to_choices_format(
        ["Census Tract", "Zoning District",
         "Neighborhood", "Political District", "County", "Zip Code", "Municipal", "Raster", "Other"])
    DATA_FREQUENCY_CHOICES = convert_to_choices_format(["", "Not Updated (Historical Only)", "As Needed",
                                                        "Annually", "Bi-Annually", "Quarterly", "Bi-Monthly", "Monthly",
                                                        "Bi-Weekly", "Weekly", "Daily",
                                                        "Hourly", "Multiple Times per Hour", "Streaming (Real Time)"])

    title = forms.CharField(label='Dataset title (required)', max_length=100)
    # url = forms.CharField(label='Dataset title', max_length=50, required=False)
    notes = forms.CharField(label='Dataset description', widget=forms.Textarea, required=False)
    license_title = forms.ChoiceField(label='Dataset license (required)', required=True, choices=LICENSE_TITLE_CHOICES)
    organization = forms.ChoiceField(label='Publishing organization (hard-coded)', required=True,
                                     choices=convert_to_choices_format(['City of Pittsburgh', 'WRPDC', 'Other/external']))
    department = forms.ChoiceField(label='Department', required=False, choices=DEPARTMENT_CHOICES)
    private = forms.ChoiceField(label='Public/Private (required)', required=True, choices=ACCESS_LEVEL_CHOICES)
    access_level_comment = forms.CharField(label='Public access level comment', widget=forms.Textarea, required=False)
    temporal_coverage = forms.CharField(label='Temporal coverage (optional and may be overwritten automatically)',
                                        required=False, max_length=200)
    geographic_unit = forms.ChoiceField(label='Geographic unit', required=False, choices=GEOGRAPHIC_UNIT_CHOICES)
    data_notes = forms.CharField(label='Data notes', widget=forms.Textarea,
                                 required=False)  # Are there any concerns about overall data reliability? Are there any changes in data collection or methods that the user should be aware of? Are there any constraints with data accuracy? What levels of confidence with this dataset could the user reasonably assume?
    frequency_data_change = forms.ChoiceField(label="Frequency with which data changes (required)", required=True,
                                              choices=DATA_FREQUENCY_CHOICES)
    frequency_data_publishing = forms.ChoiceField(label="Frequency with which data is published (required)",
                                                  required=True, choices=DATA_FREQUENCY_CHOICES)
    data_steward_name = forms.CharField(label="Name of data steward (required)", required=True, max_length=100)
    data_steward_email = forms.CharField(label="Data steward's e-mail address (required)", required=True,
                                         max_length=100)


class SchemaForm(forms.Form):
    # CKAN field data types from
    #   https://docs.ckan.org/en/2.8/maintaining/datastore.html#valid-types
    TYPE_CHOICES = [('string', "String (string)"), ('int', "Integer (int)"), ('float', "Float (float)"),
                    ('bool', "Boolean (bool)"), ('bytes', "Bytes (bytes)")]
    fieldname = forms.CharField(label='Field name', max_length=40, required=False)
    fieldtype = forms.ChoiceField(label='Field type', choices=TYPE_CHOICES, required=False)
    required = forms.BooleanField(label='Required', required=False)
    example = forms.CharField(label='Example value', max_length=40, required=False)


SchemaFormset = formset_factory(SchemaForm)
