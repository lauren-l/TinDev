from django import forms
from django.core.validators import *

class RSignUpForm(forms.Form):
    first_name = forms.CharField(help_text="First Name" min_length=1, required=True, validators=[clean_name])
    last_name = forms.CharField(help_text="Last Name", min=1, required=True, validators=[clean_name])
    username = forms.CharField(help_text="Username (At least 4 characters)", min=4, required=True, validators=[validate_slug])
    password = forms.CharField(help_text="Password (At least 8 characters)", min=8, required=True, validators=[validate_slug])
    zip = forms.CharField(help_text="Zipcode", min=5, required=True, validators=[validate_slug])
    company = forms.TypedChoiceField(help_text="Company", required=True, validators=[validate_slug])
    
    def clean_name(self):
        data = self.cleaned_data['first_name']

        # Check for non alphabet chars
        if not data.isalpha():
            raise ValidationError('Invalid first name: nonalphabet characters')

        # Remember to always return the cleaned data.
        return data