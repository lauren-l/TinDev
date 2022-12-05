import datetime
from django import forms
from django.core.validators import *
from django.core.exceptions import ValidationError
from .models import *
from django.forms.widgets import *

# CONSTANTS
EDU_CHOICES =(
    ("1", "No formal education"),
    ("2", "Coding bootcamp or equivalent"),
    ("3", "Primary education"),
    ("4", "Secondary education or high school"),
    ("5", "Vocational qualification"),
    ("6", "Bachelor's degree"),
    ("7", "Master's degree"),
    ("8", "Doctorate or higher"),
    ("9", "GED")
)
YOE_CHOICES =(
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10") 
)

SKILL_CHOICES = (
    ("1", "Python"),
    ("2", "Tableau"),
    ("3", "SQL"),
    ("4", "Java"),
    ("5", "C++"),
    ("6", "C"),
    ("7", "Go"),
    ("8", "PHP"),
    ("9", "R"),
    ("10", "Swift"),
    ("11", "HTML"),
    ("12", "CSS"),
    ("13", "JavaScript"),
    ("14", "AWS"),
    ("15", "Bash"),
    ("16", "Perl"),
    ("17", "Azure"),
    ("18", "React.js"),
    ("19", "MySQL"),
    ("20", "Machine Learning"),
    ("21", "Vue.js"),
    ("22", "C#"),
    ("23", "Natual Language Processing"),
    ("24", "Docker")
)
# CUSTOM VALIDATORS
def clean_first_name(data):
    
    # Check for non alphabet chars
    if not data.isalpha():
        raise ValidationError('Invalid first/last name: nonalphabet characters')

    return data

def clean_last_name(data):
   
    # Check for non alphabet chars
    if not data.isalpha():
        raise ValidationError('Invalid first/last name: nonalphabet characters')

    return data

# recruiter signup form

class RSignUpForm(forms.Form):

    first_name = forms.CharField(max_length=50, required=True, validators=[clean_first_name, MaxLengthValidator(50)], label="First Name *")
    last_name = forms.CharField(max_length=50,required=True, validators=[clean_last_name, MaxLengthValidator(50)], label="Last Name *")
    username = forms.CharField(min_length=4, required=True, validators=[validate_slug, MaxLengthValidator(50)], label="Username *")
    password = forms.CharField(min_length=8, required=True, validators=[validate_slug, MaxLengthValidator(50)], widget=forms.PasswordInput, label="Password *")
    zip = forms.CharField(required=True, validators=[MinLengthValidator(5), MaxLengthValidator(5)], label="Zipcode *")
    company = forms.CharField(max_length=50, required=True, validators=[validate_slug, MaxLengthValidator(50)], label="Company *")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix


# recruiter signup form

class CSignUpForm(forms.Form):
    

    first_name = forms.CharField(max_length=50, required=True, validators=[clean_first_name, MaxLengthValidator(50)], label='First Name *')
    last_name = forms.CharField(max_length=50,required=True, validators=[clean_last_name, MaxLengthValidator(50)], label="Last Name *")
    username = forms.CharField(min_length=4, required=True, validators=[validate_slug, MaxLengthValidator(50)], label="Username *")
    password = forms.CharField(min_length=8, required=True, validators=[validate_slug, MaxLengthValidator(50)], widget=forms.PasswordInput, label="Password *")
    zip = forms.CharField(required=True, validators=[MinLengthValidator(5), MaxLengthValidator(5)], label="Zipcode *")

    bio = forms.CharField(max_length=500, required=False, validators=[MaxLengthValidator(500)], label="Bio")
    github = forms.URLField(max_length=50, required=False, validators=[URLValidator, MaxLengthValidator(50)], label="Github Link")
    yoe = forms.ChoiceField(choices = YOE_CHOICES, required=True, label="Years of Experience *")
    education = forms.ChoiceField(choices = EDU_CHOICES, required=False, label="Education")
    skills = forms.MultipleChoiceField(choices = SKILL_CHOICES, required=True, label="Skills")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
class OfferForm(forms.Form):
    salary =  forms.IntegerField(label="Yearly Salary")
    expirationDate = forms.DateTimeField(
        input_formats = ['%d-%m-%yT%H:%M'],
        initial=datetime.datetime.now,
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control input',
                'required':'required'},
            format='%d-%m-%yT%H:%M')
    )
    salary.widget.attrs.update({'class':'form-control input', 'required':'required'})
    