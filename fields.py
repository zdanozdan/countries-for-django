#from django.db.models.fields import ChoiceField

from django import forms

class CountryField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        from countries import COUNTRIES
        #kwargs.setdefault('maxlength', 2)
        kwargs.setdefault('choices', COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "ChoiceField"
