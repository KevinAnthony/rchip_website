from django import forms
import datetime

class AddForm(forms.Form):
    weight = forms.DecimalField()
    date = forms.DateField(initial=datetime.date.today)

