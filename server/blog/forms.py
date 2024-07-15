from django import forms


class KeywordForm(forms.Form):
    name = forms.CharField(max_length=255, label='name')
   

class KeywordSearchForm(forms.Form):
    name = forms.CharField(max_length=255, label='name')
    country = forms.CharField(max_length=255, label='country')