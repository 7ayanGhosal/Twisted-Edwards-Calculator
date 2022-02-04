from django import forms
from django.core.exceptions import ValidationError

class adp_form(forms.Form):
    a = forms.IntegerField(min_value=2,label='a')
    d = forms.IntegerField(min_value=1,label='d')
    p = forms.IntegerField(min_value=3,label='p')

    def clean_d(self):
        a = self.cleaned_data['a']
        d = self.cleaned_data['d']
        if a == d:
            raise ValidationError("Values of a and d cannot be equal!")
        return d

class opt_form(forms.Form):
    opt_choices = (
    ('2', "Addition (+)"),
    ('3', "Subtraction (-)"),
    ('4', "Doubling (x2)"),
    ('5', "Scalar Multiplication (xScalar)"),
    )
    opt = forms.ChoiceField(choices = opt_choices)
    x1 = forms.IntegerField()
    y1 = forms.IntegerField()
    x2 = forms.IntegerField(required=False)
    y2 = forms.IntegerField(required=False)

    def clean_x2(self):
        opt = self.cleaned_data['opt']
        x2 = self.cleaned_data['x2']
        if (opt == '2' or opt == '3' or opt == '5') and not x2:
            raise ValidationError("Value required!")
        return x2
    
    def clean_x3(self):
        opt = self.cleaned_data['opt']
        x3 = self.cleaned_data['x3']
        if (opt == '2' or opt == '3') and not x3:
            raise ValidationError("Value required!")
        return x3