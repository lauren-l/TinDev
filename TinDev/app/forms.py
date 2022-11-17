from django import forms
from django.core.validators import *

class RSignUpForm(forms.Form):
    first_name = forms.CharField(help_text="First Name" min_length=1, required=True, validators=[validate_slug])
    last_name = forms.CharField(help_text="Last Name", min=1, required=True, validators=[validate_slug])
    username = forms.CharField(help_text="Username (At least 4 characters)", min=4, required=True, validators=[validate_slug])
    pwd = forms.CharField(help_text="Password (At least 8 characters)", min=8, required=True, validators=[validate_slug])
    zipcode = forms.CharField(help_text="Zipcode", min=5, required=True, validators=[validate_slug])
    company = forms.TypedChoiceField(help_text="Company", required=True, validators=[validate_slug])
    
    def clean_first_name(self):
        data = self.cleaned_data['first_name']s

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data