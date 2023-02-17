from django import forms
from .models import *


class SpendingForm(forms.ModelForm):

    class Meta:
        model = spendings
        fields = ('date', 'category', 'amount', 'user')

