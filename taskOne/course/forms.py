from unittest.loader import VALID_MODULE_NAME
from django.core.exceptions import ValidationError
from django import forms



def Validatordescription(value):
    if len(value) >= 10:
        return value
    else:
        raise ValidationError("Description Length Must Be More Than 10 Chars")


class  nameValidation(forms.Form):
    name = forms.CharField(min_length=3)
    

class  descriptionValidation(forms.Form):
    description = forms.CharField(validators=[Validatordescription])
