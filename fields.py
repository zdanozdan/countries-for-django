from django.db import models

class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('maxlength', 2)
        kwargs.setdefault('choices', COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"
